from flaskr import app, db
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required
from flaskr.models.Korisnici import Korisnici
from flaskr.models.FlaskForms import LoginForm, RegisterForm

#flask login
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def user_loader(id):
    return Korisnici.query.get(int(id))

#login (homepage)
@app.route('/', methods=['GET','POST'])  
@app.route("/auth/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        lozinka = form.lozinka.data
        if(email == "" or email.isspace()
           or  lozinka == "" or lozinka.isspace()):
            return redirect(url_for('login'))
        u = Korisnici.query.filter_by(email=email).first()
        
        if (not u or u.lozinka!=lozinka):
            return redirect(url_for('login'))
        login_user(u)
        return redirect(url_for('portfolio'))
    return render_template('auth/login.html',form=form)

#register
@app.route('/auth/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        ime = form.ime.data
        prezime = form.prezime.data
        adresa = form.adresa.data
        grad = form.grad.data
        drzava = form.drzava.data
        telefon = form.telefon.data
        email = form.email.data
        lozinka = form.lozinka.data
        if (ime == "" or ime.isspace()
            or prezime == "" or prezime.isspace()
            or adresa == "" or adresa.isspace()
            or grad == "" or grad.isspace()
            or drzava == "" or drzava.isspace()
            or telefon == "" or telefon.isspace()
            or email == "" or email.isspace()
            or lozinka == "" or lozinka.isspace()):
            return redirect(url_for('register'))
        u = Korisnici(ime=ime, prezime= prezime, adresa=adresa, grad=grad, drzava=drzava, telefon=telefon, email=email, lozinka=lozinka)
        db.session.add(u)
        db.session.commit()
        login_user(u)
        return redirect(url_for('portfolio'))
    return render_template('auth/register.html', form=form)

    

#Portfolio nakon login-a
@app.route('/portfolio', methods=['GET','POST'])
@login_required
def portfolio():
    return render_template('portfolio.html')    
        
