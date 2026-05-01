import pandas as pd
import matplotlib.pyplot as plt
import glob

# Reading in crypto Data.
df = pd.read_csv("data/interim/master_cleaned.csv")
df["date"] = pd.to_datetime(df["date"])

# Isolating the trump coin data.
trump = df[df["coin_id"] == "official-trump"][["date","price"]].copy()
trump["Asset"]="TRUMP Coin"

# Read gold data
gold = pd.read_csv(glob.glob("data/interim/Download Data*.csv")[0])
gold.columns = gold.columns.str.strip() 
gold["Close"] = gold["Close"].astype(str).str.replace(",", "", regex=False).astype(float)
gold["date"] = pd.to_datetime(gold["Date"] if "Date" in gold.columns else gold["date"])

gold = gold[["date", "Close"]].rename(columns={"Close": "price"})
gold["Asset"] = "Gold"






