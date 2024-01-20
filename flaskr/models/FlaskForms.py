from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import Email, DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    email = EmailField(validators=[Email(),DataRequired(),Length(max=40)])
    lozinka = PasswordField(validators=[DataRequired(),Length(max=40)])
    submit = SubmitField(label='Uloguj se')

class RegisterForm(FlaskForm):
    ime=StringField(validators=[Length(min=2, max=20), DataRequired()])
    prezime=StringField(validators=[Length(min=2, max=20), DataRequired()])
    adresa=StringField(validators=[DataRequired(),Length(min=3, max=40)])
    grad=StringField(validators=[DataRequired(),Length(min=2, max=20)])
    drzava = StringField(validators=[DataRequired(),Length(min=4, max=20)])
    telefon = StringField(validators=[DataRequired(),Length(min=8, max=10)])
    email = EmailField(validators=[Email(),DataRequired(),Length(max=40)])
    lozinka = PasswordField(validators=[DataRequired(),Length(min=8,max=40)])
    lozinka_confirm = PasswordField(validators=[DataRequired(),Length(min=8,max=40), EqualTo('lozinka', message='Lozinke se ne poklapaju!')])
    submit = SubmitField(label='Otvori nalog')

class ModifyForm(FlaskForm):
    ime=StringField(validators=[Length(min=2, max=20)])
    prezime=StringField(validators=[Length(min=2, max=20)])
    adresa=StringField(validators=[Length(min=3, max=40)])
    grad=StringField(validators=[Length(min=2, max=20)])
    drzava = StringField(validators=[Length(min=4, max=20)])
    telefon = StringField(validators=[Length(min=8, max=10)])
    email = EmailField(validators=[Email(),Length(max=40)])
    lozinka = PasswordField(validators=[Length(min=8,max=40)])
    lozinkapotvrde = PasswordField(validators=[Length(min=8,max=40)])
    submit = SubmitField(label='Izmeni nalog')