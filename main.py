from flask import Flask, render_template, redirect, make_response, request
from data import db_session
from data.admins import Admin
from data.developers import Developer
from data.teachers import Teacher
from data.users import User
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

db_sess = db_session.global_init('db/Dbase.db')


def main():
    app.run()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/developer")
def developer():
    return render_template("developer.html")


@app.route("/teacher")
def teacher():
    return render_template("teacher.html")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")

        teacher = db_sess.query(Teacher).filter(Teacher.login == form.login.data).first()
        if teacher and teacher.check_password(form.password.data):
            login_user(teacher, remember=form.remember_me.data)
            return redirect("/teacher")

        admin = db_sess.query(Admin).filter(Admin.login == form.login.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin, remember=form.remember_me.data)
            return redirect("/admin")

        developer = db_sess.query(Developer).filter(Developer.login == form.login.data).first()
        if developer and developer.check_password(form.password.data):
            login_user(developer, remember=form.remember_me.data)
            return redirect("/developer")

        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            login=form.login.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
