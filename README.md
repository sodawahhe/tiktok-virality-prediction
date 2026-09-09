# TikTok Video Virality Prediction Framework

Predicting which short-form videos will go viral on TikTok using engagement metrics and content metadata - a machine learning framework built for the Foundations of Data Science course (FIT5145) at Monash University Malaysia.

## Problem Statement

Short-form video platforms generate massive content volumes, yet only a fraction achieves viral reach. This project builds a data-driven framework to predict video virality, defined as the **top 10% of engagement rate** (likes + comments + shares / views) within each content category. The framework addresses three stakeholder groups:

- **Content Creators** - optimise posting strategy and content format for maximum reach
- - **Brands** - allocate influencer marketing budgets to high-virality-potential creators
  - - **Multi-Channel Networks (MCNs)** - identify and recruit promising creators early
   
    - ## Data & Methodology
   
    - - **Target variable**: Binary classification - viral (top 10% engagement rate per category) vs. non-viral
      - - **Features engineered from**: video duration, hashtag count and content, audio track metadata, posting time, content category, historical creator engagement
        - - **Models applied**: Logistic Regression, Decision Tree, Random Forest classification
          - - **Evaluation**: Precision, Recall, F1-score, ROC-AUC across content categories
           
            - ## Tech Stack
           
            - | Tool | Purpose |
            - |------|---------|
            - | R | Data wrangling, modelling, analysis |
            - | tidyverse | Data manipulation and visualisation |
            - | caret / randomForest | Machine learning model training |
            - | ggplot2 | Exploratory data analysis and result visualisation |
            - | R Markdown | Reproducible technical report |
           
            - ## Key Findings
           
            - 1. **Video duration and hashtag strategy** emerged as the strongest predictors of virality across most content categories
              2. 2. **Audio track selection** showed significant association with engagement rate, suggesting trending sounds amplify reach
                 3. 3. **The commercial framing** - mapping predictions to creator, brand, and MCN use cases - demonstrated that the same model output serves fundamentally different decision-making processes for each stakeholder
                   
                    4. ## Project Structure
                   
                    5. ```
                       tiktok-virality-prediction/
                       |-- README.md
                       |-- src/                  # R scripts for data cleaning, EDA, and modelling
                       |-- data/                 # Data files (or data source documentation)
                       |-- report/               # Technical report PDF
                       |-- figures/              # Key visualisations and charts
                       ```

                       ## About This Project

                       This was an individual project for FIT5145 Foundations of Data Science at Monash University Malaysia (Mar-May 2026). The project received a grade of **91% (High Distinction)**.

                       **Author**: Xiaowei Xu | Master of Data Science, Monash University Malaysia

                       > Note: R source code and technical report will be uploaded shortly. The project emphasises the business case framing as much as the technical modelling.
