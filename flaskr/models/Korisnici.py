import flask_login
from flaskr import db

class Korisnici(db.Model, flask_login.UserMixin):
    id = db.Column(db.Integer(), primary_key=True, unique = True)
    ime = db.Column(db.String(length=20), nullable = False)
    prezime = db.Column(db.String(length=20), nullable = False)
    adresa = db.Column(db.String(length=40), nullable = False)
    grad = db.Column(db.String(length=20), nullable = False)
    drzava = db.Column(db.String(length=20), nullable = False)
    telefon = db.Column(db.String(length=10), nullable = False)
    email = db.Column(db.String(length=40), nullable = False, unique=True)
    lozinka = db.Column(db.String(length=40), nullable=False)
    def is_authencticated(self):
        return True
