import pandas as pd
import yfinance as yf
import os, glob

table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = table[0]
sp500_list = df[['Symbol', 'Security']].values.tolist()
MAX_API_CALLS = 1800


def create_folders():
    if not os.path.exists('stocks_data'):
        os.makedirs('stocks_data')
    if not os.path.exists('stocks_obv'):
        os.makedirs('stocks_obv')
    if not os.path.exists('graphs'):
        os.makedirs('graphs')


def delete_graphs():
    files = glob.glob("graphs")
    for f in files:
        os.remove(f)


def get_sp500_data():
    for ticker in sp500_list:
        stock_ticker = yf.Ticker(ticker[0])
        stock_data = stock_ticker.history(period="1y")
        stock_data.to_csv("stocks_data\\" + ticker[0] + ".csv")
        print("Done for ticker %s" % ticker[0])


def rank_stocks_by_volume():
    volume_ratio_df = pd.DataFrame()
    for ticker in sp500_list:
        if not os.path.exists("stocks_data\\" + ticker[0] + ".csv"):
            continue
        stock_pd = pd.read_csv("stocks_data\\" + ticker[0] + ".csv")
        stock_90d = stock_pd.tail(90)
        if len(stock_90d) == 0:
            continue
        volume_sum = 0
        for index, row in stock_90d.iterrows():
            volume_sum += row["Volume"]
        volume_avg = volume_sum / 90
        ratio = stock_90d["Volume"].iat[-1] / volume_avg
        volume_ratio_df = volume_ratio_df.append({"Ticker": ticker[0], "Name": ticker[1], "Volume Ratio": ratio},
                                                 ignore_index=True)
    return volume_ratio_df.sort_values(by="Volume Ratio", ascending=False)


def get_top_10():
    top_10_tickers = []
    sorted_stocks = rank_stocks_by_volume()
    top_10 = sorted_stocks.head(10)
    for index, row in top_10.iterrows():
        top_10_tickers.append(yf.Ticker(row["Ticker"]))
    return top_10_tickers


def get_bottom_10():
    bottom_10_tickers = []
    sorted_stocks = rank_stocks_by_volume()
    bottom_10 = sorted_stocks.tail(10)
    bottom_10 = bottom_10.sort_values(by="Volume Ratio", ascending=True)
    for index, row in bottom_10.iterrows():
        bottom_10_tickers.append(yf.Ticker(row["Ticker"]))
    return bottom_10_tickers


def calculate_obv(stock_pd: pd.DataFrame, ticker: str):
    stock_90d = stock_pd.tail(90)
    volume_sum = 0
    prev_price = float("inf")
    obv_df = pd.DataFrame()
    for index, row in stock_90d.iterrows():
        price = row["Close"]
        volume = row["Volume"]
        if index == stock_90d.index.values[0] or price > prev_price:
            volume_sum += volume
        elif price < prev_price:
            volume_sum -= volume
        obv_df = obv_df.append({"Date": row["Date"], "OBV": volume_sum}, ignore_index=True)
        prev_price = price
    obv_df.to_csv("stocks_obv\\" + ticker + ".csv")
    print("Done obv for: ", ticker)
