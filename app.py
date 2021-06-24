import time
import schedule
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from calculation.calculating_obv import *
from pdf_generator.pdf_generator import create_report
from email_generator.email_generator import send_email
import threading


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Subscriber(db.Model):
    __tablename__ = "subscribers"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)


def initialize_db():
    db.create_all()


def get_subscriber(email: str):
    return db.session.query(Subscriber).filter_by(email=email).first()


def save_subscriber(email: str):
    subscriber = Subscriber(email=email)
    db.session.add(subscriber)
    db.session.commit()


def delete_subscriber(subscriber: Subscriber):
    db.session.delete(subscriber)
    db.session.commit()


def get_all_subscribers():
    return Subscriber.query.all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        email_form = request.form["email"]
        try:
            existing_sub = get_subscriber(email_form)
            if existing_sub is None:
                save_subscriber(email_form)

            return render_template('message_page.html', type=1)
        except:
            return render_template('message_page.html', type=3)
    else:
        return render_template('index.html')


@app.route("/unsubscribe", methods=['GET', 'POST'])
def unsubscribe():
    if request.method == "POST":
        email_form = request.form["email"]
        try:
            existing_sub = get_subscriber(email_form)
            if existing_sub is not None:
                delete_subscriber(existing_sub)
            return render_template('message_page.html', type=2)
        except:
            return render_template('message_page.html', type=3)
    else:
        return render_template('unsubscribe.html')


def job():
    print("Creating report started")
    create_folders()
    get_data()
    top_5 = get_top_5()
    bottom_5 = get_bottom_5()
    calculate_stocks_obv(top_5)
    calculate_stocks_obv(bottom_5)
    create_report(top_5, bottom_5)
    subscribers = get_all_subscribers()
    send_email(top_5, bottom_5, subscribers)
    delete_folders()
    print("Report created")


def method():
    print("Starting Thread")
    while True:
        schedule.run_pending()
        time.sleep(60)

    print("Ending Thread")


schedule.every().monday.at("00:00").do(job)
schedule.every().tuesday.at("00:00").do(job)
schedule.every().wednesday.at("00:00").do(job)
schedule.every().thursday.at("16:15").do(job)
schedule.every().friday.at("00:00").do(job)

if __name__ == '__main__':
    initialize_db()
    thread = threading.Thread(target=method)
    thread.start()
    app.run()
