# Probe TikTok-10M to see how videos are spread across years before deciding the filter range.
import argparse
from datetime import datetime, timezone
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datasets import load_dataset

ap = argparse.ArgumentParser()
ap.add_argument("--n_probe", type=int, default=50000)
args = ap.parse_args()

n = args.n_probe
print("probing", n, "rows")

ds = load_dataset("The-data-company/TikTok-10M", split="train", streaming=True)

years = []
for i, row in enumerate(ds):
    if i >= n:
        break
    ts = row.get("create_time")
    if ts:
        try:
            y = datetime.fromtimestamp(int(ts), tz=timezone.utc).year
            years.append(y)
        except:
            pass
    if (i+1) % 10000 == 0:
        print("  ", i+1, "done")

df = pd.DataFrame({"year": years})
dist = df["year"].value_counts().sort_index()
dist.to_csv("year_distribution.csv", header=["count"])

print("\nyear distribution:")
for y, c in dist.items():
    pct = c / len(df) * 100
    print(f"  {y}: {c}  ({pct:.1f}%)")

plt.figure(figsize=(9,5))
plt.bar(dist.index.astype(str), dist.values, color="#4878CF")
for i, v in enumerate(dist.values):
    plt.text(i, v + dist.max()*0.01, str(v), ha="center", fontsize=9)
plt.title(f"TikTok-10M year distribution (probe of {n} rows)")
plt.xlabel("year")
plt.ylabel("count")
plt.tight_layout()
plt.savefig("year_distribution.png", dpi=120)

print("\nsaved year_distribution.csv and year_distribution.png")
print("next: run sample_tiktok10m_filtered.py with year_start/year_end")
