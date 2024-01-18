from flaskr import app, db
from flask import render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user
from flaskr.models.Korisnici import Korisnici
from flaskr.models.FlaskForms import LoginForm, RegisterForm, ModifyForm
from flaskr.models.Coin import Coin
from flaskr.models.crypto import Crypto
from flaskr.models.Transaction import Transaction
from multiprocessing import Queue, Process
from datetime import datetime

import email_validator
#flask login

crypt = Crypto()
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
        return redirect(url_for('store'))
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

@app.route('/store', methods=['GET','POST'])
def store():
        
        coins = Coin.query.all()
        cryptos = crypt.get_top_25()
        for coin in coins:
            for crypto in cryptos:
                if crypto['name'] == coin.name:
                    coin.current_value = crypto['quote']['USD']['price']
                    db.session.add(coin)
        db.session.commit()        
        if not coins:
            for crypto in cryptos:
                crypto['quote']['USD']['price'] = '$ ' + "{:.2f}".format(crypto['quote']['USD']['price'])
                new_coin = Coin(name=crypto['name'], symbol=crypto['symbol'],current_value=float(crypto['quote']['USD']['price'].replace('$','')))
                db.session.add(new_coin)
            db.session.commit()
        if request.method == 'GET':
            return render_template('store.html', cryptos=cryptos, coins=coins)
        
        selected_coin = request.form.get('selected_coin')
        amount = request.form.get('amount')
        result_queue = Queue()
        p = Process(target=buy_coin, args=(selected_coin, amount, current_user.id, result_queue))
        p.start()   
        p.join() 
        flash(result_queue.get())
        return redirect(url_for('store'))  
#Portfolio nakon login-a
@app.route('/portfolio', methods=['GET','POST'])
@login_required
def portfolio():
    return render_template('portfolio.html')    

def buy_coin(selected_coin, amount, current_user_id, result_queue):
    with app.app_context():  
        korisnik = Korisnici.query.filter_by(id=current_user_id).first()  
        coin = Coin.query.filter_by(symbol=selected_coin).first()
        if coin is not None:
            bought_amount = float(amount) / float(coin.current_value)
            new_transaction = Transaction(coin_name = selected_coin, korisnik_id = current_user_id,date=datetime.now(), amount = bought_amount, price = amount)
        if float(amount) <= korisnik.novac:
            korisnik.novac -= float(amount)
            db.session.add(new_transaction)
            db.session.commit()
            result_queue.put('Transakcija uspesna')
            return
        else:
            result_queue.put('Nemate dovoljno novca za zeljenu kupovinu')
            return
        
@app.route('/modifyProfile', methods=['GET','POST'])
@login_required
def modify():
    form = ModifyForm()
    if form.is_submitted() is False:
        return render_template('modifyProfile.html', form=form)
    ime = form.ime.data
    prezime = form.prezime.data
    adresa = form.adresa.data
    grad = form.grad.data
    drzava = form.drzava.data
    telefon = form.telefon.data
    lozinka = form.lozinka.data
    lozinkapotvrde = form.lozinkapotvrde.data
    izmena = Korisnici.query.filter_by(id=current_user.id).first()
    if (ime != "" and not ime.isspace()):
            izmena.ime = ime
    if (prezime != "" and not prezime.isspace()):
            izmena.prezime = prezime
    if (adresa != "" and not adresa.isspace()):
            izmena.adresa = adresa
    if (grad != "" and not grad.isspace()):
            izmena.grad = grad
    if (drzava != "" and not drzava.isspace()):
            izmena.drzava = drzava
    if(telefon != "" and not telefon.isspace()):
            izmena.telefon = telefon
    if(lozinka == lozinkapotvrde and lozinka != "" and not lozinka.isspace() and 
                lozinkapotvrde != "" and not lozinkapotvrde.isspace()):
            izmena.lozinka = lozinka
    db.session.commit()
    return redirect(url_for('store'))
    