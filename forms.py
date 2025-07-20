from flask_wtf import FlaskForm
from wtforms import DateField, FileField, FloatField
from wtforms.fields.simple import StringField,PasswordField,SubmitField
from wtforms import RadioField
from wtforms import SelectField
from wtforms.validators import DataRequired, length , equal_to


class RegisterForm(FlaskForm):

    username = StringField("შეიყვანეთ Username", validators=[DataRequired()])
    password = PasswordField("შეიყვანეთ Password", validators=[DataRequired(), length(min=8, max=30)])
    repeat_password = PasswordField("გაიმეორეთ Password", validators=[DataRequired(), equal_to("password")])

    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField("შეიყვანეთ Username", validators=[DataRequired()])
    password = PasswordField("შეიყვანეთ Password", validators=[DataRequired(), length(min=8, max=30)])

    submit = SubmitField("Login")

class ProductForm(FlaskForm):
    img = FileField("ატვირთე პროდუქტის ფოტო")
    name = StringField("პროდუქტის სახელი")
    price = FloatField("პროდუქტის ფასი")

    submit = SubmitField("პროდუქტის შექმნა")
