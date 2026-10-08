# Stream TikTok-10M from HuggingFace and keep rows in a chosen year range.
# All actual cleaning is done in R afterwards. This script only saves a
# raw year-filtered selected-column CSV.
import argparse
from datetime import datetime, timezone
import pandas as pd
from datasets import load_dataset

KEEP = [
    "id", "create_time", "collected_time", "stats_time",
    "desc", "duration", "vq_score",
    "digg_count", "comment_count", "play_count", "share_count", "collect_count",
    "is_ad", "official_item", "original_item",
    "duet_enabled", "stitch_enabled", "share_enabled",
    "item_comment_status",
    "user_id", "user_verified", "user_tt_seller",
    "challenges",
    "music_id", "music_title", "music_author_name",
    "music_duration", "music_original",
    "poi_name", "city", "address", "poi_category",
    "poi_tt_type_name_super", "country_code",
]

ap = argparse.ArgumentParser()
ap.add_argument("--year_start", type=int, default=2023)
ap.add_argument("--year_end", type=int, default=2025)
ap.add_argument("--target_rows", type=int, default=200000)
ap.add_argument("--max_stream_rows", type=int, default=3000000)
args = ap.parse_args()

print("year range", args.year_start, "-", args.year_end)
print("target", args.target_rows, "rows")
print("started", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

ds = load_dataset("The-data-company/TikTok-10M", split="train", streaming=True)

rows = []
seen = 0
kept = 0
yc = {}
lo, hi = args.year_start, args.year_end

for row in ds:
    seen += 1
    ts = row.get("create_time")
    if ts is None:
        continue
    try:
        yr = datetime.fromtimestamp(int(ts), tz=timezone.utc).year
    except:
        continue
    if not (lo <= yr <= hi):
        continue

    rows.append({c: row.get(c) for c in KEEP if c in row})
    kept += 1
    yc[yr] = yc.get(yr, 0) + 1

    if kept % 10000 == 0:
        print(" ", seen, "streamed |", kept, "kept")

    if kept >= args.target_rows:
        print("target reached at", seen)
        break
    if seen >= args.max_stream_rows:
        print("hit max_stream_rows, kept", kept)
        break

df = pd.DataFrame(rows)

print("\nyear breakdown of collected sample:")
for y in sorted(yc):
    print(f"  {y}: {yc[y]} ({yc[y]/kept*100:.1f}%)")

out = "tiktok10m_filtered_raw.csv"
df.to_csv(out, index=False)
print(f"\nsaved {out}: {len(df)} rows, {len(df.columns)} cols")
print("next: open the Rmd file in R and run the appendix to clean this CSV")
