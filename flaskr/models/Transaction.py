from flaskr import db
from datetime import datetime

class Transaction(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable = False)
    coin_name = db.Column(db.String(), db.ForeignKey('coin.name'), nullable = False)
    korisnik_id = db.Column(db.Integer(), db.ForeignKey('korisnici.id'), nullable = False)
    date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    amount = db.Column(db.Float(), nullable=False)
    price = db.Column(db.Float(), nullable = False)