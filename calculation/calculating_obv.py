import pandas as pd
import yfinance as yf
import os
import shutil


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


def delete_folders():
    shutil.rmtree('stocks_data')
    shutil.rmtree('stocks_obv')
    shutil.rmtree('graphs')


def get_sp500_data():
    for stock in sp500_list:
        stock_ticker = yf.Ticker(stock[0])
        stock_data = stock_ticker.history(period="4m")
        stock_data.to_csv("stocks_data\\" + stock[0] + ".csv")
        print("Done for ticker %s" % stock[0])


def rank_stocks_by_volume():
    volume_ratio_df = pd.DataFrame()
    for stock in sp500_list:
        if not os.path.exists("stocks_data\\" + stock[0] + ".csv"):
            continue
        stock_pd = pd.read_csv("stocks_data\\" + stock[0] + ".csv")
        if len(stock_pd) > 90:
            stock_90d = stock_pd.tail(90)
        else:
            stock_90d = stock_pd
        if len(stock_90d) == 0:
            continue
        volume_sum = 0
        for index, row in stock_90d.iterrows():
            volume_sum += row["Volume"]
        volume_avg = volume_sum / len(stock_90d)
        ratio = stock_90d["Volume"].iat[-1] / volume_avg
        volume_ratio_df = volume_ratio_df.append({"Ticker": stock[0], "Name": stock[1], "Volume Ratio": ratio},
                                                 ignore_index=True)
    return volume_ratio_df.sort_values(by="Volume Ratio", ascending=False)


def get_top_5():
    top_5_tickers = []
    sorted_stocks = rank_stocks_by_volume()

    for index, row in sorted_stocks.iterrows():
        if len(top_5_tickers) == 5:
            break
        ticker = yf.Ticker(row["Ticker"])
        if ticker.financials.empty or ticker.balance_sheet.empty or ticker.cashflow.empty or ticker.earnings.empty:
            continue
        else:
            top_5_tickers.append(yf.Ticker(row["Ticker"]))
    return top_5_tickers


def get_bottom_5():
    bottom_5_tickers = []
    sorted_stocks = rank_stocks_by_volume()
    sorted_stocks = sorted_stocks.sort_values(by="Volume Ratio", ascending=True)
    for index, row in sorted_stocks.iterrows():
        if len(bottom_5_tickers) == 5:
            break
        ticker = yf.Ticker(row["Ticker"])
        if ticker.financials.empty or ticker.balance_sheet.empty or ticker.cashflow.empty:
            continue
        else:
            bottom_5_tickers.append(yf.Ticker(row["Ticker"]))
    return bottom_5_tickers


def calculate_obv(stock_df: pd.DataFrame, ticker: str):
    stock_90d = stock_df.tail(90)
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


def get_data():
    create_folders()
    get_sp500_data()


def calculate_stocks_obv(stock_list: []):
    for stock in stock_list:
        symbol = stock.info["symbol"]
        stock_pd = pd.read_csv("stocks_data\\" + symbol + ".csv")
        calculate_obv(stock_pd, symbol)