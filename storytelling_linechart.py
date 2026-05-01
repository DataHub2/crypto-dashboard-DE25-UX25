import pandas as pd
import matplotlib.pyplot as plt
import glob

# Reading in crypto Data.
df = pd.read_csv("data/interim/master_cleaned.csv")
df["date"] = pd.to_datetime(df["date"])

# Isolating the trump coin data.
trump = df[df["coin_id"] == "official-trump"][["date","price"]].copy()
trump["Asset"]="TRUMP Coin"




