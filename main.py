from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from calculating_obv import *
import smtplib
import threading
from pdf_creator import create_report

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Subscriber(db.Model):
    __tablename__ = "subscribers"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)


db.create_all()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        email = request.form["email"]
        try:
            subscriber = Subscriber(email=email)
            db.session.add(subscriber)
            db.session.commit()
            return redirect("/")
        except:
            return "Failed"
    else:
        return render_template('index.html')

@app.route('/email')
def send_email():
    sorted_stocks = rank_stocks_by_volume()
    top_10 = sorted_stocks.head(10)
    bottom_10 = sorted_stocks.tail(10)
    bottom_10 = bottom_10.sort_values(by="Volume Ratio", ascending=True)

    msg = "Subject: Top 10 and Bottom 10 stocks! \n" \
          "Top 10 stocks are: \n"

    for i in range(len(top_10)):
        msg += str(i+1) + ". " + top_10["Ticker"].iloc[i] + "\n"

    msg += "\nBottom 10 stocks are: \n"

    for i in range(len(bottom_10)):
        msg += str(i+1) + ". " + bottom_10["Ticker"].iloc[i] + "\n"

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user="pythonudemy14@gmail.com", password="pythonudemy97")
        connection.sendmail(from_addr="pythonudemy14@gmail.com", to_addrs="pythonudemy14@gmail.com", msg=msg)

    return render_template("index.html")


def method():
    print("Starting Thread")
    # get_sp500_data()
    # top_10 = get_top_10()
    # bottom_10 = get_bottom_10()
    # for stock in top_10:
    #     ticker = stock.info['symbol']
    #     stock_pd = pd.read_csv("stocks_data\\" + ticker + ".csv")
    #     calculate_obv(stock_pd, ticker)
    # for stock in bottom_10:
    #     ticker = stock.info['symbol']
    #     stock_pd = pd.read_csv("stocks_data\\" + ticker + ".csv")
    #     calculate_obv(stock_pd, ticker)
    create_report()
    # delete_graphs()
    print("Ending Thread")


if __name__ == '__main__':
    thread = threading.Thread(target=method)
    thread.start()
    app.run(debug=True, use_reloader=False)
