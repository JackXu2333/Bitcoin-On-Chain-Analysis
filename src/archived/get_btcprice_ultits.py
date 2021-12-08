import pandas as pd
import calendar
import yfinance as yf
import time

if __name__ == "__main__":
    # we set which pair we want to retrieve data for
    btcusd = pd.read_csv("../data/Bittrex_BTCUSD_1h.csv", header=0)


