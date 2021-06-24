from model.database_config import db
from model.subscriber import Subscriber


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