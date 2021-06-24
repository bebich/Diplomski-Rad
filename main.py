import time
import schedule
from flask import render_template, request
from model.database_service import *
from calculation.calculating_obv import *
from pdf_generator.pdf_generator import create_report
from email_generator.email_generator import send_email
import threading
from app import app


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
