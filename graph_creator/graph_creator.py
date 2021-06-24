import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter


def formatter(x, pos):
    if abs(x) > 100000000:
        return billions(x, pos)
    else:
        return millions(x, pos)


def millions(x, pos):
    return '%.2fM' % (x * 1e-6)


def billions(x, pos):
    return '%.2fB' % (x * 1e-9)


format_func = FuncFormatter(formatter)


def price_chart(ticker: str):
    price_df = pd.read_csv("stocks_data\\" + ticker + ".csv", parse_dates=True, index_col=0)
    price_df["Close"].tail(90).plot(figsize=(15, 5))
    plt.title("Close Price", fontsize=24)
    plt.yticks(fontsize=12)
    plt.ylabel("Price ($)", fontsize=18)
    plt.xlabel("")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
    plt.xticks(fontsize=12)
    plt.grid('minor')

    plt.savefig("graphs\\" + ticker + "_price_chart.png")
    plt.close()


def obv_chart(ticker: str):
    obv_df = pd.read_csv("stocks_obv\\" + ticker + ".csv", parse_dates=True, index_col=1)
    obv_df["OBV"].plot(figsize=(15, 5))
    plt.title("OBV", fontsize=24)
    plt.yticks(fontsize=12)
    plt.gca().yaxis.set_major_formatter(format_func)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
    plt.xticks(fontsize=12)
    plt.xlabel("")
    plt.grid('minor')

    plt.savefig("graphs\\" + ticker + "_obv_chart.png")
    plt.close()


def revenue_growth_chart(dataframe: pd.DataFrame, ticker):
    print(ticker)
    x_axis = [int(x) for x in dataframe["Years"]]

    plt.title("Revenue growth last 3 years", fontsize=24)
    ax = dataframe["Revenue"].plot(kind='bar', figsize=(9, 5), legend=True)
    ax.yaxis.set_major_formatter(formatter)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    ax2 = dataframe["Growth"].plot(secondary_y=True, color="red", legend=True)
    ax2.set_xticklabels(x_axis)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.ylabel("Percentage (%)", fontsize=18)

    plt.savefig("graphs\\" + ticker + "_revenue_growth_chart.png")
    plt.close()


def earnings_growth_chart(dataframe: pd.DataFrame, ticker):
    x_axis = [int(x) for x in dataframe["Years"]]

    plt.title("Earnings growth last 3 years", fontsize=24)
    ax = dataframe["Earnings"].plot(kind='bar', figsize=(9, 5), legend=True)
    ax.yaxis.set_major_formatter(format_func)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    ax2 = dataframe["Growth"].plot(secondary_y=True, color='red', legend=True)
    ax2.set_xticklabels(x_axis)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.ylabel("Percentage (%)", fontsize=18)

    plt.savefig("graphs\\" + ticker + "_earnings_growth_chart.png")
    plt.close()


def equity_to_liabilities_chart(dataframe, ticker, years):
    ax = dataframe.plot.bar(figsize=(7, 4), rot=0, fontsize=12)
    plt.title("Equity to liabilities", fontsize=22)
    ax.set_xticklabels(years)
    ax.yaxis.set_major_formatter(format_func)

    plt.savefig("graphs\\" + ticker + "_equity_to_liabilities_chart.png")
    plt.close()


def current_assets_to_current_liabilities_chart(dataframe, ticker, years):
    ax = dataframe.plot.bar(figsize=(7, 4), rot=0, fontsize=12)
    plt.title("Current assets to current liabilities", fontsize=22)
    ax.set_xticklabels(years)
    ax.yaxis.set_major_formatter(format_func)

    plt.savefig("graphs\\" + ticker + "_current_assets_to_current_liabilities_chart.png")
    plt.close()


def total_assets_ratio_chart(dataframe, ticker, years):
    ax = dataframe.plot.bar(figsize=(7, 4), stacked=True, rot=0, fontsize=12)
    plt.title("Total assets ratio", fontsize=22)
    plt.ylabel("Percentage (%)", fontsize=18)
    ax.set_xticklabels(years)
    for c in ax.containers:
        ax.bar_label(c, label_type='center')

    plt.savefig("graphs\\" + ticker + "_total_assets_ratio_chart.png")
    plt.close()


def total_liabilities_ratio_chart(dataframe, ticker, years):
    ax = dataframe.plot.bar(figsize=(7, 4), stacked=True, rot=0, fontsize=12)
    plt.title("Total liabilities ratio", fontsize=22)
    plt.ylabel("Percentage (%)", fontsize=18)
    ax.set_xticklabels(years)
    for c in ax.containers:
        ax.bar_label(c, label_type='center')

    plt.savefig("graphs\\" + ticker + "_total_liabilities_ratio_chart.png")
    plt.close()


def operating_cash_flow_chart(dataframe, ticker, years):
    ax = dataframe["Total Cash From Operating Activities"].plot.bar(figsize=(10, 6), rot=0, fontsize=12)
    plt.title("Operating cash flow", fontsize=22)
    ax.set_xticklabels(years)
    ax.yaxis.set_major_formatter(format_func)

    plt.savefig("graphs\\" + ticker + "_operating_cash_flow_chart.png")
    plt.close()
