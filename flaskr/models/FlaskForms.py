from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, Length

class LoginForm(FlaskForm):
    email = EmailField(validators=[Email(),DataRequired(),Length(max=40)])
    lozinka = PasswordField(validators=[DataRequired(),Length(max=40)])
    submit = SubmitField(label='Uloguj se')