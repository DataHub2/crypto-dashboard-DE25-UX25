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

