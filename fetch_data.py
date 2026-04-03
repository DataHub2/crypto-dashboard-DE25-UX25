""""
Fetching Data from CoinGecko API.

- The data that is getting collected is historical data, (the last 5 years).
- The data then gets stored as a csv file.
"""
import requests
import pandas as pd
import time
from pathlib import Path 

import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("COINGECKO_API_KEY")

# Config --> 
BASE_URL = "https://api.coingecko.com/api/v3"
 
COINS = {
    "bitcoin":        "Bitcoin",
    "official-trump": "Official Trump (TRUMP)",
    "dogwifcoin":     "Dogwifhat (WIF)",
    "floki":          "FLOKI",
}

# At first i will 
DAYS = "365" 

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Fetching the data.
def fetch_coin(coin_id: str) -> pd.DataFrame:
    """fetch daily price/volume/mcap history for a coin."""
    url = f"{BASE_URL}/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": DAYS,
        "interval": "daily",
    }
    resp = requests.get(url, params={**params, "x_cg_demo_api_key": API_KEY}, timeout=15)
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

# Main function to loop through coins and save data.
def main():
    all_frames = []
 
    for coin_id, display_name in COINS.items():
        print(f"Hämtar {display_name}...", end=" ", flush=True)
        try:
            df = fetch_coin(coin_id)
            # Saving individual coin data
            out_path = OUTPUT_DIR / f"{coin_id}.csv"
            df.to_csv(out_path, index=False)
            print(f"✓  {len(df)} rader → {out_path}")
            all_frames.append(df)
        except Exception as e:
            print(f"✗  FEL: {e}")
 
        # Taking in acount rate limit (30 req/min)
        time.sleep(2)
 
    # Save  masterfilee
    if all_frames:
        master = pd.concat(all_frames, ignore_index=True)
        master_path = Path("data/master.csv")
        master.to_csv(master_path, index=False)
        print(f"\n✓ Masterfil sparad → {master_path}  ({len(master)} rader totalt)")
        print("\nKolumner i master.csv:")
        print(master.dtypes)
        print("\nDatumspann per coin:")
        summary = master.groupby("coin_id")["date"].agg(["min", "max", "count"])
        summary.columns = ["från", "till", "antal_dagar"]
        print(summary)
 
 
if __name__ == "__main__":
    main()
 






