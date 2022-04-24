from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    email = EmailField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField("Подтвердите пароль", validators=[DataRequired()])
    submit = SubmitField('Применить')