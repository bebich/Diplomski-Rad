import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def send_email(top_5, bottom_5, receivers):
    # body = "Summary of todays report:\n"
    # body += "\nTop 5 stocks:\n"
    # body = append_list(body, top_5)
    # body += "\nBottom 5 stocks:\n"
    # body = append_list(body, bottom_5)
    #
    sender = "dipl.stock.analyzer@gmail.com"
    password = "Diplomski1234"
    #
    # message = MIMEMultipart()
    # message['From'] = sender
    # message['To'] = receiver
    # message['Subject'] = "Daily stock report"
    # message.attach(MIMEText(body, 'plain'))
    #
    # pdf_name = "DailyStockReport.pdf"
    #
    # binary_pdf = open(pdf_name, 'rb')
    # payload = MIMEBase('application', 'octate-stream', Name=pdf_name)
    # payload.set_payload(binary_pdf.read())
    #
    # encoders.encode_base64(payload)
    #
    # payload.add_header('Content-Decomposition', 'attachment', filename=pdf_name)
    # message.attach(payload)
    #
    # text = message.as_string()

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=sender, password=password)
        connection.sendmail(sender, "bebek.filip@gmail.com", "Text")


def append_list(body, stock_list):
    for i in range(len(stock_list)):
        if 'longName' in stock_list[i].info.keys():
            body += f"{i+1}." + stock_list[i].info["longName"] + "\n"
        else:
            body += f"{i + 1}." + stock_list[i].info["symbol"] + "\n"
    return body