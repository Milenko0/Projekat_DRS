from flaskr import app
from flask import render_template, request, redirect, url_for
import flask_login
from flaskr.models.Korisnici import Korisnici

#flask login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def user_loader(id):
    return Korisnici.query.get(int(id))

#Dolazak na pocetnu
@app.route('/', methods=['GET'])
@app.route('/auth/login', methods=['GET'])
def homepage():
    return render_template('auth/login.html')

#Login
@app.route('/', methods=['POST'])  
@app.route("/auth/login", methods=['POST'])
def login():
    email = request.form.get('email')
    if(email == "" or email.isspace()):
        return redirect(url_for('login'))
    
    password = request.form.get('password')
    if(password == "" or password.isspace()):
        return redirect(url_for('login'))
    u = Korisnici.query.filter_by(email=email).first()
    if (u.lozinka!=password or not u):
        return redirect(url_for('login'))
    flask_login.login_user(u)
    return redirect(url_for('portfolio'))

#Portfolio nakon login-a
@app.route('/portfolio', methods=['GET','POST'])
@flask_login.login_required
def portfolio():
    return render_template('portfolio.html')    
        
