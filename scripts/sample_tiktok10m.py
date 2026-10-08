"""
sample_tiktok10m.py
====================
Downloads a 100,000-row sample from The-data-company/TikTok-10M on Hugging Face
using streaming mode (no full 9.78 GB download needed), then cleans and saves
a CSV ready for R / Python analysis.

Requirements (install once):
    pip install datasets pandas pyarrow

Usage:
    python sample_tiktok10m.py

Output files:
    tiktok10m_sample_raw.csv       -- 100k rows, all 55 columns
    tiktok10m_sample_cleaned.csv   -- cleaned, engineered features (~40 cols)

Author: Xiaowei Xu | Monash University Malaysia
"""

import pandas as pd
import numpy as np
from datetime import datetime

SAMPLE_N = 100_000          # rows to collect via streaming
RANDOM_SEED = 42
OUTPUT_RAW     = "tiktok10m_sample_raw.csv"
OUTPUT_CLEANED = "tiktok10m_sample_cleaned.csv"

# ── Columns to KEEP (drop avatar URLs, share_cover, music URLs etc.) ──────
KEEP_COLS = [
    "id", "create_time", "collected_time", "stats_time",
    "desc",                        # video caption
    "duration",                    # seconds
    "vq_score",                    # video quality score
    "digg_count",                  # likes
    "comment_count",
    "play_count",                  # views
    "share_count",
    "collect_count",               # saves/bookmarks
    "is_ad",
    "official_item",
    "original_item",
    "duet_enabled", "stitch_enabled", "share_enabled",
    "item_comment_status",
    "user_id", "user_verified", "user_tt_seller",
    "challenges",                  # hashtags (JSON array as string)
    "music_id", "music_title", "music_author_name",
    "music_duration", "music_original",
    "poi_name", "city", "address",
    "poi_category",
    "poi_tt_type_name_super",
    "country_code",
    "url",
]


# ─────────────────────────────────────────────────────────────────
# STEP 1  Download via streaming
# ─────────────────────────────────────────────────────────────────
def download_sample() -> pd.DataFrame:
    from datasets import load_dataset

    print(f"[1/4] Streaming TikTok-10M — collecting {SAMPLE_N:,} rows …")
    ds = load_dataset(
        "The-data-company/TikTok-10M",
        split="train",
        streaming=True
    )

    rows = []
    np.random.seed(RANDOM_SEED)
    for i, row in enumerate(ds):
        if len(rows) >= SAMPLE_N:
            break
        rows.append({col: row.get(col) for col in KEEP_COLS if col in row})

    df = pd.DataFrame(rows)
    print(f"    → Downloaded {len(df):,} rows, {len(df.columns)} columns")
    df.to_csv(OUTPUT_RAW, index=False)
    print(f"    → Saved raw sample: {OUTPUT_RAW}")
    return df


# ─────────────────────────────────────────────────────────────────
# STEP 2  Clean
# ─────────────────────────────────────────────────────────────────
def clean(df: pd.DataFrame) -> pd.DataFrame:
    print("[2/4] Cleaning …")
    before = len(df)

    # 2a. Ensure numeric dtypes
    num_cols = ["digg_count","comment_count","play_count","share_count",
                "collect_count","duration","vq_score","music_duration"]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 2b. Drop rows with missing core engagement metrics
    core = ["play_count","digg_count","comment_count","share_count","duration"]
    before_drop = len(df)
    df = df.dropna(subset=core)
    print(f"    → Dropped {before_drop - len(df):,} rows missing core metrics")

    # 2c. Remove zero-view rows (can't compute engagement rate)
    df = df[df["play_count"] > 0]

    # 2d. IQR-based outlier removal on play_count (3×IQR fence)
    Q1, Q3 = df["play_count"].quantile([0.25, 0.75])
    IQR = Q3 - Q1
    fence_lo, fence_hi = Q1 - 3*IQR, Q3 + 3*IQR
    n_outliers = ((df["play_count"] < fence_lo) | (df["play_count"] > fence_hi)).sum()
    df = df[(df["play_count"] >= fence_lo) & (df["play_count"] <= fence_hi)]
    print(f"    → Removed {n_outliers:,} outliers (3×IQR fence on play_count)")

    # 2e. Deduplicate on video id
    before_dedup = len(df)
    df = df.drop_duplicates(subset=["id"])
    print(f"    → Removed {before_dedup - len(df):,} duplicates")

    # 2f. Boolean string → bool
    bool_cols = ["is_ad","official_item","original_item","duet_enabled",
                 "stitch_enabled","share_enabled","user_verified","user_tt_seller","music_original"]
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].map({"t": True, "f": False, True: True, False: False})

    print(f"    → Remaining rows: {len(df):,} (dropped {before - len(df):,} total)")
    return df


# ─────────────────────────────────────────────────────────────────
# STEP 3  Feature engineering
# ─────────────────────────────────────────────────────────────────
def engineer(df: pd.DataFrame) -> pd.DataFrame:
    print("[3/4] Feature engineering …")

    # Engagement rate (normalised)
    df["engagement_rate"] = (
        df["digg_count"] + df["comment_count"] + df["share_count"]
    ) / df["play_count"]

    # Viral label: top 10% engagement rate
    cut90 = df["engagement_rate"].quantile(0.90)
    df["viral"] = (df["engagement_rate"] >= cut90).astype(int)
    print(f"    → Virality cut-point (90th pct): {cut90:.4f} | viral count: {df['viral'].sum():,}")

    # Duration bin
    df["dur_bin"] = pd.cut(
        df["duration"],
        bins=[0, 15, 30, 45, 60, 9999],
        labels=["≤15s","16-30s","31-45s","46-60s",">60s"],
        include_lowest=True
    )

    # Timestamp features
    df["create_dt"] = pd.to_datetime(df["create_time"], unit="s", errors="coerce")
    df["post_hour"]    = df["create_dt"].dt.hour
    df["post_weekday"] = df["create_dt"].dt.dayofweek   # 0=Mon
    df["post_month"]   = df["create_dt"].dt.month

    # Is-weekend flag
    df["is_weekend"] = df["post_weekday"].isin([5, 6]).astype(int)

    # Hashtag count (challenges column is JSON array string)
    import re, ast
    def count_tags(val):
        if pd.isna(val) or val in ("", "[]"):
            return 0
        try:
            return len(ast.literal_eval(val))
        except Exception:
            return len(re.findall(r'"[^"]+"', str(val)))

    if "challenges" in df.columns:
        df["hashtag_count"] = df["challenges"].apply(count_tags)

    # Caption length
    if "desc" in df.columns:
        df["caption_length"] = df["desc"].fillna("").str.len()
        df["caption_word_count"] = df["desc"].fillna("").str.split().str.len()

    # Music original (bool already)
    # vq_score bin
    if "vq_score" in df.columns:
        df["vq_bin"] = pd.cut(df["vq_score"].fillna(df["vq_score"].median()),
                               bins=[0,50,60,70,100],
                               labels=["low","medium","high","premium"],
                               include_lowest=True)

    return df


# ─────────────────────────────────────────────────────────────────
# STEP 4  Save
# ─────────────────────────────────────────────────────────────────
def save(df: pd.DataFrame):
    # Drop columns we no longer need for modelling
    drop_final = ["url", "create_dt", "create_time", "music_id"]
    df = df.drop(columns=[c for c in drop_final if c in df.columns])

    df.to_csv(OUTPUT_CLEANED, index=False)
    size_mb = df.to_csv(index=False).encode().__len__() / 1024 / 1024
    print(f"[4/4] Saved cleaned file: {OUTPUT_CLEANED}")
    print(f"      Rows: {len(df):,}  |  Columns: {len(df.columns)}  |  Size: {size_mb:.1f} MB")
    print("\n=== Final column list ===")
    for col in df.columns:
        print(f"  {col}")


# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("TikTok-10M Sampling & Cleaning Pipeline")
    print(f"Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    df_raw     = download_sample()
    df_cleaned = clean(df_raw)
    df_eng     = engineer(df_cleaned)
    save(df_eng)

    print("\n✅  Done. Load the cleaned file in R with:")
    print(f"    tt <- read_csv('{OUTPUT_CLEANED}')")
