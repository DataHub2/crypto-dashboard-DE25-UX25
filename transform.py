import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/master.csv")
OUT_DIR = Path("data/interim")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def transform_data() -> pd.DataFrame:
    # Read the raw master file
    df = pd.read_csv(RAW_PATH)

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Rename the column to something more accurate
    if "pct_change_24h" in df.columns:
        df = df.rename(columns={"pct_change_24h": "daily_return_pct"})

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Make sure numeric columns are numeric
    numeric_cols = ["price", "volume", "market_cap", "daily_return_pct"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Sort by coin and date
    df = df.sort_values(["coin_id", "date"]).reset_index(drop=True)

    # Recalculate daily return percentage per coin
    df["daily_return_pct"] = df.groupby("coin_id")["price"].pct_change() * 100

    # 7-day moving average for price
    df["price_7d_ma"] = (
        df.groupby("coin_id")["price"]
        .transform(lambda s: s.rolling(7).mean())
    )

    # 7-day moving average for volume
    df["volume_7d_ma"] = (
        df.groupby("coin_id")["volume"]
        .transform(lambda s: s.rolling(7).mean())
    )

    return df

def main():
    df = transform_data()

    out_path = OUT_DIR / "master_cleaned.csv"
    df.to_csv(out_path, index=False)

    print(f"Cleaned data saved to {out_path}")
    print("\nFirst 5 rows:")
    print(df.head())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

if __name__ == "__main__":
    main()