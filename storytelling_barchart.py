import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np


"""
This script is for the barchart for storytelling of the volitility for the choosen assets.
The goal with this is to make the barchart is to follow the the principels of data storytelling so that we end up with a a result that mirrors my goal with. the visuals.

"""

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
gold_volatility = gdf["daily_return"].std()
results.append({"Asset": "gold", "Volatility": gold_volatility})

# DataFrame for plotting
df_plot = pd.DataFrame(results) 

# Nname mapping for better visualization, So that the names show up readble fo the customer, and to make sure that we dont get the name directly from my dataset.
name_map = {
    "dogwifcoin": "Dogwifhat",
    "floki": "Floki",
    "official-trump": "TRUMP Coin",
    "bitcoin": "Bitcoin",
    "gold": "Gold"
}
df_plot["Asset"] = df_plot["Asset"].map(name_map)

# (largest volatility) sits at the top
df_plot = df_plot.sort_values("Volatility", ascending=True).reset_index(drop=True)

# Colors we will be working with, yes kokchun i got the inspiration from you!

BG_COLOR = '#E5E7E8'
BAR_GRAY = '#AEB0B2'
BAR_HIGHLIGHT = '#2A4354'
TEXT_COLOR = '#333333'

fig, ax = plt.subplots(figsize=(10, 6.5))
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

# Identify stable assets and highlighting them
highlight_assets = ['Bitcoin', 'Gold']
colors = [BAR_HIGHLIGHT if asset in highlight_assets else BAR_GRAY for asset in df_plot['Asset']]

#  bar plotting on the horizontal axis, and we are using the colors list to set the color of each bar based on whether it's a stable asset or not.
bars = ax.barh(df_plot['Asset'], df_plot['Volatility'], color=colors, height=0.6, zorder=3)

#structural framing to maximize Data-Ink Ratio
for spine in ax.spines.values():
    spine.set_visible(False) # Remove all spines for a cleaner look on the visuals. 




