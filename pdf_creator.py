from fpdf import FPDF

from calculating_obv import get_top_10, get_bottom_10
from calculations import *
from graph_creator import *

WIDTH = 190
HEIGHT = 297


def create_report():
    top_10 = get_top_10()
    bottom_10 = get_bottom_10()
    pdf = FPDF()
    cover_page(pdf)
    list_page(pdf, "Top 10", top_10)
    company_pages(pdf, top_10[0])
    list_page(pdf, "Bottom 10", bottom_10)
    pdf.output("DailyStockReport.pdf", 'F')


def cover_page(pdf: FPDF):
    pdf.set_font('Arial', "B", 75)
    pdf.add_page()
    pdf.ln(100)
    pdf.cell(82)
    pdf.cell(w=25, txt="Daily Stock", align='C')
    pdf.ln(30)
    pdf.cell(81)
    pdf.cell(w=25, txt="Report", align='C')
    pdf.ln(40)
    pdf.set_font('Arial', "B", 30)
    pdf.cell(83)
    pdf.cell(w=25, txt="1.1.2021", align='C')


def list_page(pdf: FPDF, text: str, company_list):
    pdf.set_font('Arial', "B", 75)
    pdf.add_page()
    pdf.ln(30)
    pdf.cell(w=85)
    pdf.cell(w=25, txt=f"{text}", align='C')
    pdf.ln(30)
    pdf.set_font('Arial', "", 20)
    for i in range(10):
        pdf.ln(17)
        pdf.cell(w=30)
        pdf.cell(w=0, txt=f"{i + 1}. {company_list[i].info['longName']}")


def company_pages(pdf: FPDF, company):
    summary_page(pdf, company.info)
    financial_pages(pdf, company)


def summary_page(pdf, company):
    pdf.add_page()
    pdf.set_font('Arial', 'B', 25)
    pdf.ln(10)
    pdf.cell(w=0, txt=f"{company['longName']}", align='C')
    pdf.set_font('Arial', 'B', 20)
    pdf.ln(10)
    pdf.cell(w=WIDTH / 2, txt=f"{price(company)}$", align='R')
    pdf.set_font('Arial', '', 15)
    pdf.cell(w=0, txt=f"{price_change(company)}$ {price_change_percentage(company)}")
    pdf.ln(15)
    valuation_table(pdf, company)
    pdf.ln(12)
    stock_price_history_table(pdf, company)
    pdf.ln(12)
    set_price_chart(pdf, company['symbol'])
    pdf.ln(5)
    set_obv_chart(pdf, company['symbol'])


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
    pdf.cell(w=0, h=10, txt="Valuation metrics")
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
    pdf.cell(w=WIDTH / 6, h=10, txt="PEG (5 yr expected):", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f'{peg_ratio(company)}', align='R')
    pdf.cell(10)
    pdf.cell(w=WIDTH / 6, h=10, txt="Price to sales:", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f'{price_to_sales(company)}', align='R')
    pdf.cell(10)
    pdf.cell(w=WIDTH / 6, h=10, txt="Price to book:", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f'{price_book_ratio(company)}', align='R')
    pdf.ln(10)
    pdf.cell(w=WIDTH / 6, h=10, txt="Dividend Rate:", align='L')
    pdf.cell(w=WIDTH / 6 - 10, h=10, txt=f'{dividend_rate(company)}$', align='R')
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


def cash_flow_page(company, pdf):
    pdf.set_font('Arial', '', 16)
    pdf.add_page()
    pdf.cell(w=0, txt="Cash flow")
    pdf.ln(12)
    cash_flow_table(pdf, company)


def balance_sheet_page(company, pdf):
    pdf.set_font('Arial', '', 16)
    pdf.add_page()
    pdf.cell(w=0, txt="Balance sheet")
    pdf.ln(12)
    balance_sheet_table(pdf, company)


def income_statement_page(company, pdf):
    pdf.set_font('Arial', '', 16)
    pdf.cell(w=0, txt="Income statement")
    pdf.ln(12)
    income_statement_table(pdf, company)


def income_statement_table(pdf: FPDF, company):
    earnings_df = company.earnings
    years = earnings_df.index
    financials_df = company.financials.transpose()
    pdf.set_font('Arial', '', 14)
    table_header(pdf, years)
    table_row(pdf, earnings_df, get_value, "Revenue", "Revenue", years)
    table_row(pdf, financials_df, get_value, "Cost Of Revenue", "Cost of revenue", years)
    table_row(pdf, financials_df, get_value, "Gross Profit", "Gross Profit", years)
    table_row_subtract(pdf, financials_df, get_value_subtract, "Total Operating Expenses", "Cost Of Revenue",
                       "Operating Expense", years)
    table_row(pdf, financials_df, get_value, "Total Operating Expenses", "Total operating expense", years)
    table_row(pdf, earnings_df, get_value, "Earnings", "Net Income", years)
    table_row(pdf, financials_df, get_value, "Ebit", "EBIT", years)


def balance_sheet_table(pdf, company):
    years = company.earnings.index
    balance_sheet_df = company.balance_sheet.transpose()
    pdf.set_font('Arial', '', 14)
    table_header(pdf, years)
    table_row(pdf, balance_sheet_df, get_value, "Total Assets", "Total assets", years)
    table_row(pdf, balance_sheet_df, get_value, "Total Current Assets", "  Total current assets", years)
    table_row(pdf, balance_sheet_df, get_value, "Cash", "    Cash", years)
    table_row(pdf, balance_sheet_df, get_value, "Short Term Investment", "    Short term investments", years)
    table_row_subtract_three(pdf, balance_sheet_df, get_value_subtract_three, "Total Current Assets", "Cash",
                             "Short Term Investment", "    Other current assets",  years)
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
    pdf.set_font('Arial', '', 14)
    table_header(pdf, years)
    table_row(pdf, cash_flow_df, get_value, "Total Cash From Operating Activities", "Operating cash flow", years)
    table_row(pdf, cash_flow_df, get_value, "Total Cashflows From Investing Activities", "Investing cash flow", years)
    table_row(pdf, cash_flow_df, get_value, "Total Cash From Financing Activities", "Financing cash flow", years)
    table_row(pdf, cash_flow_df, get_value, "Change In Cash", "Change in cash", years)
    table_row(pdf, cash_flow_df, get_value, "Issuance Of Stock", "Issuance of stock ", years)
    table_row(pdf, cash_flow_df, get_value, "Repurchase Of Stock", "Repurchase of stock", years)


def table_header(pdf, years):
    pdf.cell(w=70, txt="")
    for i in range(len(years) - 1, -1, -1):
        pdf.cell(w=25, txt=f"{years[i]}", align="C")
        pdf.cell(w=5, txt="")
    pdf.ln(10)


def table_row(pdf: FPDF, df, method, field, row_name, years):
    pdf.cell(w=70, txt=f"{row_name}")
    for i in range(len(years)):
        pdf.cell(w=25, txt=f"{method(df, field, i)}", align="C")
        pdf.cell(w=5, txt="")
    pdf.ln(10)


def table_row_subtract(pdf:FPDF, df, method, field1, field2, row_name, years):
    pdf.cell(w=70, txt=f"{row_name}")
    for i in range(len(years)):
        pdf.cell(w=25, txt=f"{method(df, field1, field2, i)}", align="C")
        pdf.cell(w=5, txt="")
    pdf.ln(10)


def table_row_subtract_three(pdf:FPDF, df, method, field1, field2, field3, row_name, years):
    pdf.cell(w=70, txt=f"{row_name}")
    for i in range(len(years)):
        pdf.cell(w=25, txt=f"{method(df, field1, field2, field3, i)}", align="C")
        pdf.cell(w=5, txt="")
    pdf.ln(10)


def set_price_chart(pdf, ticker):
    price_chart(ticker)
    pdf.image("graphs\\" + ticker + "_price_chart.png", w=WIDTH, h=68)


def set_obv_chart(pdf, ticker):
    obv_chart(ticker)
    pdf.image("graphs\\" + ticker + "_obv_chart.png", w=WIDTH, h=68)






