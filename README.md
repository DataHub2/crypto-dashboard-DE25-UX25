# About Our Product: Crypto Dashboard

Crypto Dashboard is an analytics project focused on turning crypto market data into clear, decision-ready insights using Power BI.
The project covers data ingestion, transformation, semantic modeling, and storytelling so trends and risks can be understood quickly.

## Project Overview

This repository builds a small end-to-end analytics pipeline for selected coins:

- Bitcoin (`bitcoin`)
- Official Trump (`official-trump`)
- Dogwifhat (`dogwifcoin`)
- FLOKI (`floki`)

Data is fetched from the CoinGecko API, standardized into analysis-ready tables, and prepared for Power BI reporting.
The cleaned dataset supports trend analysis, volatility tracking, and comparative storytelling across assets.

## Data Pipeline

1. **Ingestion (`fetch_data.py`)**
- Pulls historical daily market data (price, volume, market cap) from CoinGecko.
- Stores one CSV per coin in `data/raw/`.
- Builds a combined file in `data/master.csv`.

2. **Transformation (`transform.py`)**
- Cleans and types the master dataset.
- Recalculates daily return by coin.
- Creates rolling indicators:
  - `price_7d_ma`
  - `volume_7d_ma`
- Saves curated output to `data/interim/master_cleaned.csv`.

3. **Exploration (.ipynb folders)**
- Validates data quality and coverage.
- Supports analysis before Power BI modeling.

4. **Reporting & Storytelling (Power BI)**
- Uses the cleaned dataset for semantic modeling and report creation.
- Enables KPI tracking, trend narratives, and coin-to-coin comparisons.


## Suggested Semantic Model (Power BI)

- **Fact table:** daily coin metrics from `master_cleaned.csv`
- **Dimensions:**
  - Date
  - Coin
- **Core measures:**
  - Average price
  - Total volume
  - Average daily return (%)
  - Market cap trend

## Repository Structure

crypto-dashboard-DE25-UX25/
├── README.md                        # Project overview, setup, and workflow
├── pyproject.toml                   # Project dependencies and metadata
├── uv.lock                          # Locked dependency versions
├── main.py                          # Minimal entry script (placeholder)
├── fetch_data.py                    # API ingestion: raw + master CSV outputs
├── transform.py                     # Data cleaning and feature engineering
├── data/
│   ├── raw/                         # Per-coin raw CSV files
│   ├── master.csv                   # Combined raw dataset
│   └── interim/
│       └── master_cleaned.csv       # Cleaned dataset for analytics/Power BI
└── EDA/
    └── EDA.ipynb                    # Exploratory analysis notebook