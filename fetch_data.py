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



