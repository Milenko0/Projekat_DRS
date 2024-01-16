from flaskr import app
from flask import render_template, request, redirect, url_for
import flask_login
from flaskr.models.Korisnici import Korisnici
from flaskr.models.FlaskForms import LoginForm

#flask login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def user_loader(id):
    return Korisnici.query.get(int(id))


@app.route('/', methods=['GET','POST'])  
@app.route("/auth/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        lozinka = form.lozinka.data
        print(email)
        if(email == "" or email.isspace()
           or  lozinka == "" or lozinka.isspace()):
            return redirect(url_for('login'))
        u = Korisnici.query.filter_by(email=email).first()
        
        if (not u or u.lozinka!=lozinka):
            return redirect(url_for('login'))
        flask_login.login_user(u)
        return redirect(url_for('portfolio'))
    return render_template('auth/login.html',form=form)

#register
@app.route('/auth/register', methods=['GET','POST'])
def register():
    return render_template('auth/register.html')

    

#Portfolio nakon login-a
@app.route('/portfolio', methods=['GET','POST'])
@flask_login.login_required
def portfolio():
    return render_template('portfolio.html')    
        
