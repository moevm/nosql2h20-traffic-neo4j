from neomodel import db


def connect(url):
    db.set_connection(url)
