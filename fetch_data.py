""""
Fetching Data from CoinGecko API.

- The data that is getting collected is historical data, (the last 5 years).
- The data then gets stored as a csv file.
"""
import requests
import pandas as pd
import time
from pathlib import Path 

BASE_URL = "https://api.coingecko.com/api/v3"
 
COINS = {
    "bitcoin":        "Bitcoin",
    "official-trump": "Official Trump (TRUMP)",
    "dogwifcoin":     "Dogwifhat (WIF)",
    "floki":          "FLOKI",
}

# At first i will 
DAYS = 1825 # 365 * 5 = 5 years 

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def fetch_coin(coin_id: str) -> pd.DataFrame:
    """fetch daily price/volume/mcap history for a coin."""
    url = f"{BASE_URL}/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": DAYS,
        "interval": "daily",
    }
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    raw = resp.json()
 
    df_price = pd.DataFrame(raw["prices"],         columns=["timestamp", "price"])
    df_vol   = pd.DataFrame(raw["total_volumes"],  columns=["timestamp", "volume"])
    df_mcap  = pd.DataFrame(raw["market_caps"],    columns=["timestamp", "market_cap"])
 
    df = df_price \
        .merge(df_vol,  on="timestamp") \
        .merge(df_mcap, on="timestamp")
 
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms").dt.date
    df["coin_id"] = coin_id
    df = df.drop(columns=["timestamp"])
    df = df[["date", "coin_id", "price", "volume", "market_cap"]]
    df = df.sort_values("date").reset_index(drop=True)
 
    # calculating daily percentage change 
    df["pct_change_24h"] = df["price"].pct_change() * 100
 
    return df






