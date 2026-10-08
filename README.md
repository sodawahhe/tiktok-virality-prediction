# TikTok Video Virality Prediction

> Predicting which short-form videos will go viral from engagement metrics and content metadata: an end-to-end classification pipeline in R, framed around the commercial decisions of creators, brands and multi-channel networks (MCNs).

Individual project for *Foundations of Data Science* at Monash University Malaysia (Mar-May 2026), graded 91% (High Distinction).

## Business Problem

Short-form video platforms produce enormous content volumes, yet only a small fraction achieves viral reach. This project builds a data-driven framework to predict virality, defined as the **top 10% of engagement rate** ((likes + comments + shares) / views) within each content category, so that the same model output can support three different decisions:

| Stakeholder | Decision supported |
|---|---|
| Content creators | Optimise posting strategy and content format for reach |
| Brands | Allocate influencer-marketing budgets to high-virality-potential creators |
| MCNs | Identify and recruit promising creators early |

## Approach

- **Target:** binary classification, viral (top 10% engagement rate per category) vs. non-viral
- **Features:** video duration, hashtag count and content, audio track metadata, posting time, content category, historical creator engagement
- **Models:** Logistic Regression, Decision Tree, Random Forest
- **Evaluation:** precision, recall, F1-score and ROC-AUC, compared across content categories

## Key Findings

1. **Video duration and hashtag strategy** were the strongest predictors of virality across most content categories.
2. **Audio track selection** was significantly associated with engagement rate, suggesting trending sounds amplify reach.
3. **Commercial framing matters:** mapping predictions to creator, brand and MCN use cases showed that one model output serves fundamentally different decision processes for each stakeholder.

## Tech Stack

| Tool | Purpose |
|---|---|
| R | Data wrangling, modelling, analysis |
| tidyverse | Data manipulation and visualisation |
| caret / randomForest | Model training |
| ggplot2 | Exploratory analysis and result visualisation |
| R Markdown | Reproducible technical report |

## Status

R scripts, figures and the technical report are being added to this repository.

## Author

Xiaowei Xu | Master of Data Science, Monash University Malaysia
