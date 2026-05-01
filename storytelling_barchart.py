import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np

# ingesting the cleaned data
df = pd.read_csv("data/interim/master_cleaned.csv") 
df["date"] = pd.to_datetime(df["date"])

# Isolate the data from gold
gold_path = glob.glob("data/interim/Download Data*.csv")[0]
gold = pd.read_csv(gold_path)
gold.columns = gold.columns.str.strip()
gold["Close"] = gold["Close"].astype(str).str.replace(',', '', regex=False).astype(float)

# Because i dont know exactly what the column name variations are, i am going to be working with a if and else statement to make sure that the date column is properly converted.
if "Date" in gold.columns:
    gold["date"] = pd.to_datetime(gold["Date"])
else:
    gold["date"] = pd.to_datetime(gold["date"])

# -- Note that LLM helped me with getting the right syntax for calculating the the daily percentage (line 30-34)
# On this chapter i am going to get the right calculation.
results = []

# process speculative and "standard" crypto assets
for coin in df["coin_id"].unique(): # Loops through each unique coin_id
    cdf = df[df["coin_id"] == coin].sort_values("date").copy()
    # Calculate daily percentage change
    cdf["daily_return"] = cdf["price"].pct_change() * 100
    # Calculate standard deviation of these returns
    volatility = cdf["daily_return"].std()
    results.append({"Asset": coin, "Volatility": volatility})

# Process traditional asset (Gold)
gdf = gold.sort_values("date").copy()
gdf["daily_return"] = gdf["Close"].pct_change() * 100
g_volatility = gdf["daily_return"].std()
results.append({"Asset": "gold", "Volatility": g_volatility})
