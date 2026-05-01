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

# put both "assets" together
combined = pd.concat([trump, gold], ignore_index=True).dropna(subset=["date", "price"])
combined = combined.sort_values(["Asset", "date"])

# Use same time period for both
start_date = max(
    combined[combined["Asset"] == "TRUMP Coin"]["date"].min(),
    combined[combined["Asset"] == "Gold"]["date"].min()
)

end_date = min(
    combined[combined["Asset"] == "TRUMP Coin"]["date"].max(),
    combined[combined["Asset"] == "Gold"]["date"].max()
)

combined = combined[(combined["date"] >= start_date) & (combined["date"] <= end_date)].copy()

# Make both start at 100, this is a way for me to able to compare the assets from a stable and fair perspektiv.
combined["Performance Index"] = combined.groupby("Asset")["price"].transform(
    lambda x: (x / x.iloc[0]) * 100
)

gold_df = combined[combined["Asset"] == "Gold"]
trump_df = combined[combined["Asset"] == "TRUMP Coin"]


# Colors, added gold color to match "Gold" and red color to match "TRUMP Coin"
# Note i got help with the colors and figure design from the LLM, i wanted to make sure that the colors are not to bright and also that they match the assets that they represent.
BG, TEXT, SUB, GRID = "#E5E7E8", "#222222", "#555555", "#D0D0D0"
GOLD, TRUMP = "#8A5E13", "#A30F18"

fig, ax = plt.subplots(figsize=(18, 10))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

# Lines
ax.plot(gold_df["date"], gold_df["Performance Index"], color=GOLD, linewidth=3)
ax.plot(trump_df["date"], trump_df["Performance Index"], color=TRUMP, linewidth=3)
ax.axhline(100, color="#999999", linestyle="--", linewidth=1.2)

# Clean style
for spine in ax.spines.values():
    spine.set_visible(False)

ax.yaxis.grid(True, color=GRID)
ax.xaxis.grid(False)
ax.tick_params(length=0, labelsize=12, colors=TEXT)

ax.set_ylim(20, 185)
ax.set_xlim(combined["date"].min() - pd.Timedelta(days=20),
            combined["date"].max() + pd.Timedelta(days=80))

ax.set_xlabel("DATE", fontweight="bold", labelpad=15, color=TEXT)

# Title and text
fig.suptitle(
    "Gold holds value while TRUMP Coin falls after early speculation",
    x=0.08, y=0.93, ha="left",
    fontsize=22, fontweight="bold", color=TEXT
)

fig.text(
    0.08, 0.865,
    "Both assets start at 100, so it is easier to compare them.\n"
    "Gold moves up more slowly and steadily.\n"
    "TRUMP Coin rises quickly in the beginning, but then drops a lot.",
    fontsize=12, color=SUB, ha="left", va="top",
    linespacing=1.35, style="italic"
)

# Legend
fig.text(0.08, 0.775, "━ Gold", fontsize=15, color=GOLD, fontweight="bold")
fig.text(0.18, 0.775, "━ TRUMP Coin", fontsize=15, color=TRUMP, fontweight="bold")









