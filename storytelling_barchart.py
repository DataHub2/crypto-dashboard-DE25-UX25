import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np

# ingesting the cleaned data
df = pd.read_csv("data/interim/master_cleaned.csv")
df["date"] = pd.to_datetime(df["date"])
