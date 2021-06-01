import pandas as df

def price_earnings_ratio(info):
    market_price = info['regularMarketPrice']
    trailing_eps = info['trailingEps']
    if trailing_eps is None or trailing_eps < 0:
        return "N/A"
    else:
        return format_two_decimals(market_price / trailing_eps)


def price_book_ratio(info):
    if info['priceToBook'] is None:
        return "N/A"
    else:
        return format_two_decimals(info['priceToBook'])


def price_change_percentage(info):
    market_price = info['regularMarketPrice']
    close = info['previousClose']
    if market_price is None or close is None:
        return "N/A"
    else:
        return format_two_decimals((market_price - close) / close) + "%"


def market_cap(info):
    return format_millions_billions(info['marketCap'])


def forward_pe(info):
    if info["forwardPE"] is None:
        return "N/A"
    else:
        return format_two_decimals(info["forwardPE"])


def peg_ratio(info):
    if info["pegRatio"] is None:
        return "N/A"
    else:
        return format_two_decimals(info["pegRatio"])


def price_to_sales(info):
    if info["priceToSalesTrailing12Months"] is None:
        return "N/A"
    else:
        return format_two_decimals(info["priceToSalesTrailing12Months"])


def dividend_rate(info):
    if info["dividendRate"] is None:
        return "N/A"
    else:
        return format_two_decimals(info["dividendRate"])


def dividend_yield(info):
    if info["dividendYield"] is None:
        return "N/A"
    else:
        return format_percentage(info["dividendYield"])


def payout_ratio(info):
    if info["payoutRatio"] is None:
        return "N/A"
    else:
        return format_percentage(info["payoutRatio"])


def price(info):
    if info["regularMarketPrice"] is None:
        return "N/A"
    else:
        return format_two_decimals(info["regularMarketPrice"])


def price_change(info):
    regular_price = info["regularMarketPrice"]
    close = info["previousClose"]
    if regular_price is None or close is None:
        return "N/A"
    else:
        return format_two_decimals(regular_price - close)


def previous_close(info):
    if info["regularMarketPreviousClose"] is None:
        return "N/A"
    else:
        return format_two_decimals(info["regularMarketPreviousClose"])


def market_open(info):
    if info["regularMarketOpen"] is None:
        return "N/A"
    else:
        return format_two_decimals(info["regularMarketOpen"])


def day_high(info):
    if info["regularMarketDayHigh"] is None:
        return "N/A"
    else:
        return format_two_decimals(info["regularMarketDayHigh"])


def day_low(info):
    if info["regularMarketDayLow"] is None:
        return "N/A"
    else:
        return format_two_decimals(info["regularMarketDayLow"])


def fifty_day_average(info):
    if info["fiftyDayAverage"] is None:
        return "N/A"
    else:
        return format_two_decimals(info["fiftyDayAverage"])


def two_hundred_day_average(info):
    if info["twoHundredDayAverage"] is None:
        return "N/A"
    else:
        return format_two_decimals(info["twoHundredDayAverage"])


def fifty_two_week_high(info):
    if info["fiftyTwoWeekHigh"] is None:
        return "N/A"
    else:
        return format_two_decimals(info["fiftyTwoWeekHigh"])


def fifty_two_week_low(info):
    if info["fiftyTwoWeekLow"] is None:
        return "N/A"
    else:
        return format_two_decimals(info["fiftyTwoWeekLow"])


def fifty_two_week_change(info):
    if info["52WeekChange"] is None:
        return "N/A"
    else:
        return format_change(format_two_decimals(info["52WeekChange"] * 100)) + "%"


def get_value(ticker: df.DataFrame, field, index):
    if field in ticker.columns:
        return format_millions_billions(ticker.iloc[index][field])
    else:
        return "-"


def get_value_subtract(ticker: df.DataFrame, field1, field2, index):
    if field1 and field2 in ticker.columns:
        return format_millions_billions(ticker.iloc[index][field1]-ticker.iloc[index][field2])
    else:
        return "-"


def get_value_subtract_three(ticker: df.DataFrame, field1, field2, field3, index):
    if field1 and field2 and field3 in ticker.columns:
        return format_millions_billions(ticker.iloc[index][field1]-ticker.iloc[index][field2] - ticker.iloc[index][field3])
    elif field1 and field2 in ticker.columns:
        return format_millions_billions(ticker.iloc[index][field1] - ticker.iloc[index][field2])
    elif field1 and field3 in ticker.columns:
        return format_millions_billions(ticker.iloc[index][field1] - ticker.iloc[index][field3])
    elif field1 in ticker.columns:
        return format_millions_billions(ticker.iloc[index][field1])
    else:
        return "-"


def format_two_decimals(number):
    return "{:.2f}".format(number)


def format_three_decimals(number):
    return "{:.3f}".format(number)


def format_percentage(percentage):
    return "{:.2f}".format(percentage * 100) + "%"


def format_millions_billions(number: int):
    if number > 1000000000:
        return str(format_three_decimals(number / 1000000000)) + "B"
    else:
        return str(format_three_decimals(number / 1000000)) + "M"


def format_change(change):
    if float(change) >= 0:
        return "+" + str(change)
    else:
        return "-" + str(change)
