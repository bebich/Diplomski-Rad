import pandas as df
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def price_chart(ticker: str):
    price_df = df.read_csv("stocks_data\\" + ticker + ".csv", parse_dates=True, index_col=0)
    price_df["Close"].tail(90).plot(figsize=(15, 5))
    plt.title("Close Price", fontsize=24)
    plt.yticks(fontsize=12)
    plt.ylabel("Price ($)", fontsize=18)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
    plt.xticks(fontsize=12)
    plt.xlabel("Date", fontsize=18)
    plt.grid('minor')
    plt.plot()
    plt.savefig("graphs\\" + ticker + "_price_chart.png")
    plt.close()


def obv_chart(ticker: str):
    obv_df = df.read_csv("stocks_obv\\" + ticker + ".csv", parse_dates=True, index_col=1)
    obv_df["OBV"].plot(figsize=(15, 5))
    plt.title("OBV", fontsize=24)
    plt.yticks(fontsize=12)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
    plt.xticks(fontsize=12)
    plt.xlabel("Date", fontsize=18)
    plt.grid('minor')
    plt.plot()
    plt.savefig("graphs\\" + ticker + "_obv_chart.png")
    plt.close()
