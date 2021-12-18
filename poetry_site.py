import os
from flask import Flask,g, flash, url_for, redirect,request,abort
from flask.helpers import make_response
from flask.templating import render_template
# from flask_login.utils import login_required, login_user, current_user,
from forms import LoginForm, RegistrationForm, WritingsForm
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3 as sq
from poetryDataBase import poetryDataBase
from flask_login import LoginManager, current_user, logout_user, login_user, login_required
from UserLogin import UserLogin

DATABASE = 'poetry_data.db'
DEBUG = True
SECRET_KEY = 'bfeea3444f39619e23dda3b554bac228deb124466cbe5c75'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE = os.path.join(app.root_path, "poetry_data.db")))
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024 # 4mb

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"

@login_manager.user_loader
def load_user(user_id):
    print("load user")
    return UserLogin().fromDB(user_id,dBase)

def connect_db():
    conn = sq.connect(app.config["DATABASE"])
    conn.row_factory = sq.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource("poetry_db.sql", mode = "r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db

dBase = None
@app.before_request # подключаемся к базе данных перед каждым запросом
def before_request():
    global dBase
    db = get_db()
    dBase = poetryDataBase(db)

@app.route("/")
def main():
    return render_template("main.html",menu = dBase.getMenu(), title = "ONEGIN'S", current_user = current_user)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = dBase.getUserByEmail(form.email.data)
        if user and check_password_hash(user['passw'], form.passw.data):
            user_login = UserLogin().create(user)
            rm = form.remember.data
            login_user(user_login, remember = rm)
            return redirect(request.args.get("next") or url_for('profile'))
        flash("Неверная пара логин/пароль", "error")
    return render_template("login.html", menu = dBase.getMenu(), title = "Авторизация", form = form, current_user = current_user)

@app.route("/registration", methods = ["POST", "GET"])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash = generate_password_hash(form.passw.data)
        res = dBase.addUser(form.login.data, form.email.data, hash)
        if res:  
            #flash("Вы успешно зарегистрировались", "success")
            # UserLogin().create(dBase.getUserByEmail(form.email.data))
            return redirect(url_for("profile"))
        else:
            flash("Ошибка регистрации пользователя", "error")
    return render_template("registration.html", title = "Регистрация", menu = dBase.getMenu(), form = form, current_user = current_user)

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", menu = dBase.getMenu(), title = "Profile page", writings = dBase.getWritingsAnnounce(current_user.get_id()))

@app.route("/add_writing", methods = ['POST','GET'])
@login_required
def addWriting():
    form = WritingsForm()
    print("нажали")
    if form.validate_on_submit():
        print('валиден')
        res = dBase.add_writing(form.title.data, form.writing.data, current_user.get_id())
        if not res:
            flash("Ошибка добавления записи","error")
        else:
            flash("Запись успешна добавлена","success")
    else:
        flash("Запись не валидна","error")
    return render_template("add_writing.html", menu = dBase.getMenu(), title = "Добавление записи", form = form)

@app.route("/writing/<writing_url>")
@login_required
def showWriting(writing_url):
    title, writing = dBase.getWriting(writing_url)
    if not title:
        abort(404)
    return render_template('writing.html', menu = dBase.getMenu(), title = title, writing = writing)

@app.route("/userava")
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ""
    h = make_response(img)
    h.headers["Content-Type"] = 'image/png'
    return h

@app.route('/upload',methods = ["POST", "GET"])
@login_required
def upload():
    if request.method == "POST":
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = dBase.updateUserAvatar(img, current_user.get_id())
                if not res:
                    flash("Ошибка обновления аватара", "error")
                flash("Аватар обновлен", "success")
            except FileNotFoundError as e:
                flash("Ошибка чтения файла", "error")
        else:
            flash("Ошибка обновления аватара", "error")
    return redirect(url_for("profile"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for("login"))

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()

if __name__ == "__main__":
    app.run(debug=True)


