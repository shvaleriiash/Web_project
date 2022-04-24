from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SelectField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    price = StringField('Цена', validators=[DataRequired()])
    image = FileField(validators=[DataRequired()])
    category = SelectField('Категория', choices=[], validators=[DataRequired()])
    description = TextAreaField("Описание", validators=[DataRequired()])
    count = StringField('Количество', validators=[DataRequired()])
    submit = SubmitField('Создать товар')