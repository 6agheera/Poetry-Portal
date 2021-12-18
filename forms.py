from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo



class LoginForm(FlaskForm):
    email = StringField("Email: ", validators = [Email(message="Введите корректный email адрес")])
    passw = PasswordField("Пароль ", validators=[DataRequired("Введите пароль"), Length(min = 6, max = 20, message="Необходимо ввести пароль длиной от 6 до 20 символов")])
    remember = BooleanField("Запомнить", default = False)
    submit = SubmitField("Войти")

class RegistrationForm(FlaskForm):
    login = StringField("Логин: ", validators=[Length(min = 4, max = 20, message = "Необходимо вписать логин длиной от 4 до 20 символов")])
    email = StringField("Email: ", validators = [Email(message="Введите корректный email адрес")])
    passw = PasswordField("Пароль: ", validators=[DataRequired(message="Введите пароль"), Length(min = 6, max = 20, message="Необходимо ввести пароль длиной от 6 до 20 символов")])
    passw2 = PasswordField("Повторите пароль: ", validators=[DataRequired(message="Повторите пароль"), EqualTo("passw", message = "Пароли не совпадают")])
    submit = SubmitField("Зарегистрироваться")    

class WritingsForm(FlaskForm):
    title = StringField(validators=[DataRequired(message = "Впишите название записи")])
    writing = TextAreaField( validators=[DataRequired(message="Запись пустая")])
    submit = SubmitField("Добавить запись")    