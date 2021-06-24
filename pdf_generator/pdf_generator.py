from fpdf import FPDF
import datetime as dt
from calculation.calculations import *
from graph_creator.graph_creator import *

WIDTH = 190
HEIGHT = 297


def create_report(top_5, bottom_5):
    print("TOP 5: ", top_5)
    print("BOTTOM 5: ", bottom_5)
    pdf = FPDF()
    cover_page(pdf)
    list_page(pdf, "Top 5", top_5)
    for company in top_5:
        company_pages(pdf, company)
    list_page(pdf, "Bottom 5", bottom_5)
    for company in bottom_5:
        company_pages(pdf, company)
    pdf.output("DailyStockReport.pdf", 'F')


def cover_page(pdf: FPDF):
    date = dt.date.today()
    pdf.set_font('Arial', "B", 75)
    pdf.add_page()
    pdf.ln(100)
    pdf.cell(w=0, txt="Daily Stock", align='C')
    pdf.ln(30)
    pdf.cell(w=0, txt="Report", align='C')
    pdf.ln(40)
    pdf.set_font('Arial', "B", 30)
    pdf.cell(83)
    pdf.cell(w=25, txt=f"{date.strftime('%d.%m.%Y')}", align='C')


def list_page(pdf: FPDF, text: str, company_list):
    pdf.set_font('Arial', "B", 75)
    pdf.add_page()
    pdf.ln(30)
    pdf.cell(w=0, txt=f"{text}", align='C')
    pdf.ln(30)
    pdf.set_font('Arial', "", 20)
    for i in range(5):
        pdf.ln(17)
        pdf.cell(w=30)
        if 'longName' in company_list[i].info.keys():
            pdf.cell(w=0, txt=f"{i + 1}. {company_list[i].info['longName']}")
        else:
            pdf.cell(w=0, txt=f"{i + 1}. {company_list[i].info['symbol']}")


def company_pages(pdf: FPDF, company):
    summary_page(pdf, company.info)
    financial_pages(pdf, company)


def summary_page(pdf, company_info):
    pdf.add_page()
    pdf.set_font('Arial', 'B', 25)
    pdf.ln(10)
    if 'longName' in company_info.keys():
        pdf.cell(w=0, txt=f"{company_info['longName']}", align='C')
    else:
        pdf.cell(w=0, txt=f"{company_info['symbol']}", align='C')
    pdf.set_font('Arial', 'B', 20)
    pdf.ln(10)
    pdf.cell(w=WIDTH / 2, txt=f"{price(company_info)}$", align='R')
    pdf.set_font('Arial', '', 15)
    pdf.cell(w=0, txt=f"{price_change(company_info)}$ {price_change_percentage(company_info)}")
    pdf.ln(10)
    pdf.cell(w=0, txt=f"Sector: {company_info['sector']}", align='C')
    pdf.ln(10)
    valuation_table(pdf, company_info)
    pdf.ln(12)
    stock_price_history_table(pdf, company_info)
    pdf.ln(12)
    set_price_chart(pdf, company_info['symbol'])
    pdf.ln(5)
    set_obv_chart(pdf, company_info['symbol'])


def financial_pages(pdf, company):
    pdf.add_page()
    pdf.set_font('Arial', '', 20)
    pdf.cell(w=0, txt="Financials")
    pdf.ln(15)
    income_statement_page(company, pdf)
    balance_sheet_page(company, pdf)
    cash_flow_page(company, pdf)


def valuation_table(pdf: FPDF, company):
    pdf.set_font('Arial', '', 14)
    pdf.cell(w=0, h=10, txt="Valuation metrics & dividends")
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    pdf.cell(w=WIDTH / 6, h=10, txt="Market Cap: ", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f'{market_cap(company)}', align='R')
    pdf.cell(10)
    pdf.cell(w=WIDTH / 6, h=10, txt="Trailing P/E:", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f'{price_earnings_ratio(company)}', align='R')
    pdf.cell(10)
    pdf.cell(w=WIDTH / 6, h=10, txt="Forward P/E:", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f'{forward_pe(company)}', align='R')
    pdf.ln(10)
    pdf.cell(w=WIDTH / 6, h=10, txt="PEG(5y exp):", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f'{peg_ratio(company)}', align='R')
    pdf.cell(10)
    pdf.cell(w=WIDTH / 6, h=10, txt="Price to sales:", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f'{price_to_sales(company)}', align='R')
    pdf.cell(10)
    pdf.cell(w=WIDTH / 6, h=10, txt="Price to book:", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f'{price_book_ratio(company)}', align='R')
    pdf.ln(10)
    pdf.cell(w=WIDTH / 6, h=10, txt="Dividend Rate:", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f'{dividend_rate(company)}', align='R')
    pdf.cell(10)
    pdf.cell(w=WIDTH / 6, h=10, txt="Dividend yield:", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f'{dividend_yield(company)}', align='R')
    pdf.cell(10)
    pdf.cell(w=WIDTH / 6, h=10, txt="Payout ratio:", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f'{payout_ratio(company)}', align='R')


def stock_price_history_table(pdf, company):
    pdf.set_font('Arial', '', 14)
    pdf.cell(w=0, h=10, txt="Stock price history")
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    pdf.cell(w=WIDTH / 6, h=10, txt="Previous Close: ", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f"{previous_close(company)}$", align='R')
    pdf.cell(10)
    pdf.cell(w=WIDTH / 6, h=10, txt="Open:", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f"{market_open(company)}$", align='R')
    pdf.cell(10)
    pdf.cell(w=WIDTH / 6, h=10, txt="Day high:", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f"{day_high(company)}$", align='R')
    pdf.ln(10)
    pdf.cell(w=WIDTH / 6, h=10, txt="Day low:", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f"{day_low(company)}$", align='R')
    pdf.cell(10)
    pdf.cell(w=WIDTH / 6, h=10, txt="50 day average:", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f"{fifty_day_average(company)}$", align='R')
    pdf.cell(10)
    pdf.cell(w=WIDTH / 6, h=10, txt="200 day average:", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f"{two_hundred_day_average(company)}$", align='R')
    pdf.ln(10)
    pdf.cell(w=WIDTH / 6, h=10, txt="52 week high:", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f"{fifty_two_week_high(company)}$", align='R')
    pdf.cell(10)
    pdf.cell(w=WIDTH / 6, h=10, txt="52 week low:", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f"{fifty_two_week_low(company)}$", align='R')
    pdf.cell(10)
    pdf.cell(w=WIDTH / 6, h=10, txt="52 week change:", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f"{fifty_two_week_change(company)}", align='R')


def income_statement_page(company, pdf):
    pdf.set_font('Arial', '', 16)
    pdf.cell(w=0, txt="Income statement")
    pdf.ln(12)
    income_statement_table(pdf, company)
    income_statement_graphs(pdf, company)


def balance_sheet_page(company, pdf):
    pdf.set_font('Arial', '', 16)
    pdf.add_page()
    pdf.cell(w=0, txt="Balance sheet")
    pdf.ln(12)
    balance_sheet_table(pdf, company)
    balance_sheet_graphs(pdf, company)


def cash_flow_page(company, pdf):
    pdf.set_font('Arial', '', 16)
    pdf.add_page()
    pdf.cell(w=0, txt="Cash flow")
    pdf.ln(12)
    cash_flow_table(pdf, company)
    cash_flow_graphs(pdf, company)


def income_statement_table(pdf: FPDF, company):
    earnings_df = company.earnings
    years = earnings_df.index
    financials_df = company.financials.transpose()
    table_header(pdf, years)
    table_row(pdf, earnings_df[::-1], get_value, "Revenue", "Revenue", years)
    table_row(pdf, calculate_growth(earnings_df, years, "Revenue")[::-1], get_value_percentage, "Growth", "Revenue growth", years)
    table_row(pdf, financials_df, get_value, "Cost Of Revenue", "Cost of revenue", years)
    table_row(pdf, financials_df, get_value, "Gross Profit", "Gross Profit", years)
    table_row_subtract(pdf, financials_df, get_value_subtract, "Total Operating Expenses", "Cost Of Revenue",
                       "Operating Expense", years)
    table_row(pdf, financials_df, get_value, "Total Operating Expenses", "Total expenses", years)
    table_row(pdf, earnings_df[::-1], get_value, "Earnings", "Net Income", years)
    table_row(pdf, calculate_growth(earnings_df, years, "Earnings")[::-1], get_value_percentage, "Growth", "Net Income growth", years)
    table_row(pdf, financials_df, get_value, "Ebit", "EBIT", years)


def balance_sheet_table(pdf, company):
    years = company.earnings.index
    balance_sheet_df = company.balance_sheet.transpose()
    table_header(pdf, years)
    table_row(pdf, balance_sheet_df, get_value, "Total Assets", "Total assets", years)
    table_row(pdf, balance_sheet_df, get_value, "Total Current Assets", "  Total current assets", years)
    table_row(pdf, balance_sheet_df, get_value, "Cash", "    Cash", years)
    table_row(pdf, balance_sheet_df, get_value, "Short Term Investments", "    Short term investments", years)
    table_row_subtract_three(pdf, balance_sheet_df, get_value_subtract_three, "Total Current Assets", "Cash",
                             "Short Term Investment", "    Other current assets", years)
    table_row_subtract(pdf, balance_sheet_df, get_value_subtract, "Total Assets", "Total Current Assets",
                       "  Total non current assets", years)
    table_row(pdf, balance_sheet_df, get_value, "Total Liab", "Total liabilities", years)
    table_row(pdf, balance_sheet_df, get_value, "Total Current Liabilities", "  Total current liabilities", years)
    table_row_subtract(pdf, balance_sheet_df, get_value_subtract, "Total Liab", "Total Current Liabilities",
                       "  Total non current liabilities", years)
    table_row(pdf, balance_sheet_df, get_value, "Long Term Debt", "    Long Term Debt", years)
    table_row_subtract(pdf, balance_sheet_df, get_value_subtract, "Total Assets", "Total Liab", "Total equity", years)
    table_row(pdf, balance_sheet_df, get_value, "Total Stockholder Equity", "  Shareholders' equity", years)
    table_row(pdf, balance_sheet_df, get_value, "Retained Earnings", "    Retained Earnings", years)


def cash_flow_table(pdf, company):
    years = company.earnings.index
    cash_flow_df = company.cashflow.transpose()
    table_header(pdf, years)
    table_row(pdf, cash_flow_df, get_value, "Total Cash From Operating Activities", "Operating cash flow", years)
    table_row(pdf, cash_flow_df, get_value, "Total Cashflows From Investing Activities", "Investing cash flow", years)
    table_row(pdf, cash_flow_df, get_value, "Total Cash From Financing Activities", "Financing cash flow", years)
    table_row(pdf, cash_flow_df, get_value, "Change In Cash", "Change in cash", years)
    table_row(pdf, cash_flow_df, get_value, "Issuance Of Stock", "Issuance of stock ", years)
    table_row(pdf, cash_flow_df, get_value, "Repurchase Of Stock", "Repurchase of stock", years)


def table_header(pdf, years):
    pdf.cell(w=70, txt="")
    pdf.set_font('Arial', '', 12)
    for i in range(len(years) - 1, -1, -1):
        pdf.cell(w=25, txt=f"{years[i]}", align="C")
        pdf.cell(w=5, txt="")
    pdf.ln(10)


def table_row(pdf: FPDF, df, method, field, row_name, years):
    pdf.set_font('Arial', '', 12)
    pdf.cell(w=70, txt=f"{row_name}")
    pdf.set_font('Arial', '', 10)
    for i in range(len(years)):
        pdf.cell(w=25, txt=f"{method(df, field, i)}", align="C")
        pdf.cell(w=5, txt="")
    pdf.ln(8)


def table_row_subtract(pdf: FPDF, df, method, field1, field2, row_name, years):
    pdf.set_font('Arial', '', 12)
    pdf.cell(w=70, txt=f"{row_name}")
    pdf.set_font('Arial', '', 10)
    for i in range(len(years)):
        pdf.cell(w=25, txt=f"{method(df, field1, field2, i)}", align="C")
        pdf.cell(w=5, txt="")
    pdf.ln(8)


def table_row_subtract_three(pdf: FPDF, df, method, field1, field2, field3, row_name, years):
    pdf.set_font('Arial', '', 12)
    pdf.cell(w=70, txt=f"{row_name}")
    pdf.set_font('Arial', '', 10)
    for i in range(len(years)):
        pdf.cell(w=25, txt=f"{method(df, field1, field2, field3, i)}", align="C")
        pdf.cell(w=5, txt="")
    pdf.ln(8)


def income_statement_graphs(pdf, company):
    revenue_growth_graph(pdf, company)
    earnings_growth_graph(pdf, company)


def balance_sheet_graphs(pdf, company):
    equity_to_liabilities_graph(pdf, company)
    current_assets_to_current_liabilities_graph(pdf, company)
    total_assets_ratio_graph(pdf, company)
    total_liabilities_ratio_graph(pdf, company)


def cash_flow_graphs(pdf, company):
    operating_cash_flow_graph(pdf, company)


def revenue_growth_graph(pdf, company):
    earnings_df = company.earnings
    years = earnings_df.index
    growth_df = calculate_growth(earnings_df, years, "Revenue")
    set_revenue_growth_chart(pdf, growth_df, company.info['symbol'])


def earnings_growth_graph(pdf, company):
    earnings_df = company.earnings
    years = earnings_df.index
    growth_df = calculate_growth(earnings_df, years, "Earnings")
    set_earnings_growth_chart(pdf, growth_df, company.info['symbol'])


def equity_to_liabilities_graph(pdf, company):
    balance_sheet_df = company.balance_sheet.transpose()
    years = company.earnings.index
    graph_df = pd.DataFrame()
    for i in range(0, len(years)):
        total_equity = balance_sheet_df.iloc[i]["Total Assets"] - balance_sheet_df.iloc[i]["Total Liab"]
        graph_df = graph_df.append(
                {"Liabilities": balance_sheet_df.iloc[i]["Total Liab"], "Equity": total_equity},
                ignore_index=True)

    set_equity_to_liabilities_chart(pdf, graph_df, company.info['symbol'], years)


def total_assets_ratio_graph(pdf, company):
    balance_sheet_df = company.balance_sheet.transpose()
    years = company.earnings.index
    graph_df = calculate_perc_ratio_df(balance_sheet_df, years, "Total Assets", "Total Non Current Assets", "Total Current Assets")

    set_total_assets_ratio_chart(pdf, graph_df, company.info['symbol'], years)


def total_liabilities_ratio_graph(pdf, company):
    balance_sheet_df = company.balance_sheet.transpose()
    years = company.earnings.index
    graph_df = calculate_perc_ratio_df(balance_sheet_df, years, "Total Liab", "Total Non Current Liabilities", "Total Current Liabilities")

    set_total_liabilities_ratio_chart(pdf, graph_df, company.info['symbol'], years)


def current_assets_to_current_liabilities_graph(pdf, company):
    balance_sheet_df = company.balance_sheet.transpose()
    years = company.earnings.index
    graph_df = create_graph_df(balance_sheet_df, years, "Total Current Assets", "Total Current Liabilities")

    set_current_assets_to_current_liabilities_chart(pdf, graph_df, company.info['symbol'], years)


def operating_cash_flow_graph(pdf, company):
    cash_flow_df = company.cashflow.transpose()
    years = company.earnings.index

    set_operating_cash_flow_chart(pdf, cash_flow_df, company.info['symbol'], years)


def calculate_growth(dataframe, years, field):
    growth_df = df.DataFrame()
    for i in range(0, len(years)):
        if i != 0:
            percentage = calculate_percentage_growth(dataframe, field, i)
            growth_df = growth_df.append(
                {"Years": years[i], f"{field}": dataframe.iloc[i][field], "Growth": percentage},
                ignore_index=True)
        else:
            growth_df = growth_df.append(
                {"Years": years[i], f"{field}": dataframe.iloc[i][field], "Growth": 0},
                ignore_index=True)
    return growth_df


def calculate_perc_ratio_df(balance_sheet_df, years, total_field, non_current_field, current_field):
    graph_df = pd.DataFrame()
    for i in range(0, len(years)):
        total_non_current = balance_sheet_df.iloc[i][total_field] - \
                                   balance_sheet_df.iloc[i][current_field]
        current_perc = format_percentage(
            balance_sheet_df.iloc[i][current_field] / balance_sheet_df.iloc[i][total_field])
        non_current_perc = format_percentage(total_non_current / balance_sheet_df.iloc[i][total_field])
        graph_df = graph_df.append(
            {f"{non_current_field}": non_current_perc,
             f"{current_field}": current_perc},
            ignore_index=True)
    return graph_df


def create_graph_df(dataframe, years, field1, field2):
    graph_df = pd.DataFrame()
    for i in range(0, len(years)):
        graph_df = graph_df.append(
            {f"{field1}": dataframe.iloc[i][field1],
             f"{field2}": dataframe.iloc[i][field2]},
            ignore_index=True)
    return graph_df


def set_price_chart(pdf, ticker):
    price_chart(ticker)
    pdf.image("graphs\\" + ticker + "_price_chart.png", w=WIDTH, h=68)


def set_obv_chart(pdf, ticker):
    obv_chart(ticker)
    pdf.image("graphs\\" + ticker + "_obv_chart.png", w=WIDTH, h=68)


def set_revenue_growth_chart(pdf, dataframe, ticker):
    revenue_growth_chart(dataframe, ticker)
    pdf.image("graphs\\" + ticker + "_revenue_growth_chart.png", x=25, y=115, w=WIDTH - 40, h=85)


def set_earnings_growth_chart(pdf, dataframe, ticker):
    earnings_growth_chart(dataframe, ticker)
    pdf.image("graphs\\" + ticker + "_earnings_growth_chart.png", x=25, y=205, w=WIDTH - 40, h=85)


def set_equity_to_liabilities_chart(pdf, dataframe, ticker, years):
    equity_to_liabilities_chart(dataframe, ticker, years)
    pdf.image("graphs\\" + ticker + "_equity_to_liabilities_chart.png", x=5, y=135, w=WIDTH/2, h=70)


def set_current_assets_to_current_liabilities_chart(pdf, dataframe, ticker, years):
    current_assets_to_current_liabilities_chart(dataframe, ticker, years)
    pdf.image("graphs\\" + ticker + "_current_assets_to_current_liabilities_chart.png", x=105, y=135, w=WIDTH/2, h=70)


def set_total_assets_ratio_chart(pdf, dataframe, ticker, years):
    total_assets_ratio_chart(dataframe, ticker, years)
    pdf.image("graphs\\" + ticker + "_total_assets_ratio_chart.png", x=5, y=205, w=WIDTH/2, h=70)


def set_total_liabilities_ratio_chart(pdf, dataframe, ticker, years):
    total_liabilities_ratio_chart(dataframe, ticker, years)
    pdf.image("graphs\\" + ticker + "_total_liabilities_ratio_chart.png", x=105, y=205, w=WIDTH/2, h=70)


def set_operating_cash_flow_chart(pdf, dataframe, ticker, years):
    operating_cash_flow_chart(dataframe, ticker, years)
    pdf.image("graphs\\" + ticker + "_operating_cash_flow_chart.png", x=25, y=75, w=WIDTH - 20, h=95)




