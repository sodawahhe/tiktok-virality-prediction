# TikTok Video Virality Prediction

> Feasibility study and proposed machine-learning framework for predicting which short-form videos go viral on TikTok. Data cleaning, virality labelling and exploratory analysis in R, framed around creator, brand and MCN decisions.

Individual project for *Foundations of Data Science* at Monash University Malaysia (Mar-May 2026), graded 91% (High Distinction).

**Scope:** this repository documents the data work (cleaning, label definition, EDA) and the proposed modelling approach. The classification models described below are the *proposed* design; they have not been trained or evaluated.

## Business Problem

Short-form video platforms produce enormous content volumes, yet only a small fraction achieves viral reach. The project defines virality as the **top 10% of engagement rate**, (likes + comments + shares) / views, and asks whether it can be predicted early enough to support three decisions:

| Stakeholder | Decision supported |
|---|---|
| Content creators | Optimise posting strategy and content format for reach |
| Brands | Allocate influencer-marketing budgets to high-virality-potential creators |
| MCNs | Identify and recruit promising creators early |

## Data

| Source | Size | Role |
|---|---|---|
| Kaggle TikTok engagement dataset | 19,382 rows, 12 columns | Prototype dataset for cleaning and EDA |
| HuggingFace TikTok-10M | 10M rows, 55 columns, 9.78 GB Parquet | Full-scale source with audio, geolocation, hashtag and posting-time fields; sampled to 100k rows via streaming |

## Cleaning and Labelling

- 298 rows (1.54%) were missing every engagement metric at once, which points to records not yet indexed at collection time rather than random gaps, so they were dropped as a block (19,084 rows retained).
- No zero-view rows, no outliers under a 3x IQR fence, and no duplicate video IDs were found.
- Engagement rate replaces raw view count as the target, because views favour large verified accounts.
- The top-10% cut-point is an engagement rate of 0.636, giving roughly a 10:1 class imbalance.

## Key Findings (EDA)

1. **Claim videos engage more than opinion videos:** median engagement rate 0.394 vs 0.259 (t-test, p < 0.001).
2. **Visibility ceiling:** verified accounts get more views but a lower engagement rate, which is why the target is normalised by views.
3. **Strong collinearity among engagement counts** (likes vs views r = 0.80, shares vs views r = 0.67), which favours tree-based models over linear ones.
4. **Duration alone is a weak predictor:** only about a 4.9% difference in median engagement rate across duration bins, versus about 49% for claim status. This supports combining content, creator and contextual features.

## Proposed Modelling Framework (not yet implemented)

Logistic Regression as a baseline, then Random Forest, then XGBoost with `scale_pos_weight` for the class imbalance, with SHAP for interpretation. Planned evaluation: precision, recall, F1 and ROC-AUC. TikTok-10M would add the music/audio, posting-time and geolocation features the demo dataset lacks.

## Tech Stack

| Tool | Purpose |
|---|---|
| R (tidyverse, ggplot2, corrplot, knitr) | Cleaning, feature engineering, EDA, reproducible report |
| Python (HuggingFace datasets) | Streaming a 100k-row sample from TikTok-10M |

## Status

R scripts, figures and the technical report are being added to this repository.

## Author

Xiaowei Xu | Master of Data Science, Monash University Malaysia
