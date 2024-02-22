from os import abort

from flask import Flask, render_template, redirect, make_response, request
from data import db_session
from data.admins import Admin
from data.developers import Developer
from data.teachers import Teacher
from data.users import User
from data.classes import Classs
from data.predmet import Predmet
from forms.admin import RegisterFormAdmin
from forms.classs import RegisterFormClass
from forms.teacher import RegisterFormTeacher
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
db_sess = db_session.global_init('db/Dbase.db')
us = 'None'
nameUs = ""
userUs = None
classsId = 0


def main():
    app.run()


@app.route("/")
def index():
    return render_template("index.html", us=us, nameUs=nameUs)


@app.route("/admin")
def admin():
    try:
        db_sess = db_session.create_session()
        a = []
        for i in db_sess.query(Classs).filter(Classs.adminId == userUs.id):
            a.append([i.id, i.name])
        db_sess = db_session.create_session()
        b = []
        for i in db_sess.query(Teacher).filter(Teacher.adminId == userUs.id):
            b.append([i.id, i.name])
        return render_template("admin.html", us=us, nameUs=nameUs, news=a, newss=b)
    except Exception:
        return redirect("/")


@app.route("/developer")
def developer():
    if userUs:
        db_sess = db_session.create_session()
        a = []
        for i in db_sess.query(Admin).all():
            a.append([i.id, i.surname, i.name, i.school])

        return render_template("developer.html", news=a, us=us, nameUs=nameUs)
    else:
        return redirect("/")


@app.route("/teacher")
def teacher():
    if userUs:
        return render_template("teacher.html", us=us, nameUs=nameUs)
    else:
        return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global us, nameUs, userUs
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                us = 'user'
                nameUs = user.name
                userUs = user
                return redirect("/")
        else:
            teacher = db_sess.query(Teacher).filter(Teacher.login == form.login.data).first()
            if teacher:
                if teacher.check_password(form.password.data):
                    login_user(teacher, remember=form.remember_me.data)
                    us = 'teacher'
                    nameUs = teacher.name
                    userUs = teacher
                    return redirect("/teacher")
            else:
                admin = db_sess.query(Admin).filter(Admin.login == form.login.data).first()
                if admin:
                    if admin.check_password(form.password.data):
                        login_user(admin, remember=form.remember_me.data)
                        us = 'admin'
                        nameUs = admin.name
                        userUs = admin
                        return redirect("/admin")
                else:
                    developer = db_sess.query(Developer).filter(Developer.login == form.login.data).first()
                    if developer:
                        if developer.check_password(form.password.data):
                            login_user(developer, remember=form.remember_me.data)
                            us = 'developer'
                            nameUs = developer.login
                            userUs = developer
                            return redirect("/developer")
            us = "None"
            userUs = None
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form, us=us, nameUs=nameUs)
    return render_template('login.html', title='Авторизация', form=form, us=us, nameUs=nameUs)


@app.route('/logout')
def logout():
    global us, nameUs, userUs
    us = "None"
    nameUs = ""
    userUs = None
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first() \
                or db_sess.query(Teacher).filter(Teacher.login == form.login.data).first() \
                or db_sess.query(Admin).filter(Admin.login == form.login.data).first() \
                or db_sess.query(Developer).filter(Developer.login == form.login.data).first():
            return render_template('register.html', title='Новый ученик',
                                   form=form,
                                   message="Такой логин уже есть", us=us, nameUs=nameUs)
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            login=form.login.data,
            email=form.email.data,
            classId=classsId
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect(f'/newClass/{user.classId}')
    return render_template('register.html', title='Новый ученик', form=form, us=us, nameUs=nameUs)


@app.route('/newAdmin', methods=['GET', 'POST'])
def new_admin():
    form = RegisterFormAdmin()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first() \
                or db_sess.query(Teacher).filter(Teacher.login == form.login.data).first() \
                or db_sess.query(Admin).filter(Admin.login == form.login.data).first() \
                or db_sess.query(Developer).filter(Developer.login == form.login.data).first():
            return render_template('registerAdmin.html', title='Новый админ',
                                   form=form,
                                   message="Такой логин уже есть", us=us, nameUs=nameUs)
        admin = Admin(
            surname=form.surname.data,
            name=form.name.data,
            school=form.school.data,
            login=form.login.data,
            email=form.email.data
        )
        admin.set_password(form.password.data)
        db_sess.add(admin)
        db_sess.commit()
        return redirect('/developer')
    return render_template('registerAdmin.html', title='Новый админ', form=form, us=us, nameUs=nameUs)


@app.route('/newTeacher', methods=['GET', 'POST'])
def new_teacher():
    try:
        form = RegisterFormTeacher()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.login == form.login.data).first() \
                    or db_sess.query(Teacher).filter(Teacher.login == form.login.data).first() \
                    or db_sess.query(Admin).filter(Admin.login == form.login.data).first() \
                    or db_sess.query(Developer).filter(Developer.login == form.login.data).first():
                return render_template('registerAdmin.html', title='Новый учитель',
                                       form=form,
                                       message="Такой логин уже есть", us=us, nameUs=nameUs)
            teacher = Teacher(
                surname=form.surname.data,
                name=form.name.data,
                login=form.login.data,
                email=form.email.data,
                adminId=userUs.id
            )
            teacher.set_password(form.password.data)
            db_sess.add(teacher)
            db_sess.commit()
            return redirect('/admin')
        return render_template('registerTeacher.html', title='Новый учитель', form=form, us=us, nameUs=nameUs)
    except Exception:
        return redirect("/")


@app.route('/newClass', methods=['GET', 'POST'])
def new_class():
    try:
        form = RegisterFormClass()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            classs = Classs(
                name=form.name.data,
                adminId=userUs.id
            )
            db_sess.add(classs)
            db_sess.commit()
            return redirect('/admin')
        return render_template('registerClass.html', title='Новый класс', form=form, us=us, nameUs=nameUs)
    except Exception:
        return redirect("/")


@app.route('/newTeacher/<int:id>', methods=['GET', 'POST'])
def edit_teacher(id):
    form = RegisterFormTeacher()
    if request.method == "GET":
        db_sess = db_session.create_session()
        teacher = db_sess.query(Teacher).filter(Teacher.id == id).first()
        if teacher:
            form.surname.data = teacher.surname
            form.name.data = teacher.name
            form.login.data = teacher.login
            form.email.data = teacher.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        teacher = db_sess.query(Teacher).filter(Teacher.id == id).first()
        if teacher:
            teacher.surname = form.surname.data
            teacher.name = form.name.data
            teacher.login = form.login.data
            teacher.email = form.email.data
            teacher.set_password(form.password.data)
            db_sess.commit()
            return redirect('/admin')
        else:
            abort(404)
    return render_template('registerTeacher.html',
                           title='Редактирование учителя',
                           form=form, us=us, nameUs=nameUs)


@app.route('/newUser/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    form = RegisterForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()
        if user:
            form.surname.data = user.surname
            form.name.data = user.name
            form.login.data = user.login
            form.email.data = user.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()
        if user:
            user.surname = form.surname.data
            user.name = form.name.data
            user.login = form.login.data
            user.email = form.email.data
            user.set_password(form.password.data)
            db_sess.commit()
            return redirect(f'/newClass/{user.classId}')
        else:
            abort(404)
    return render_template('register.html',
                           title='Редактирование ученика',
                           form=form, us=us, nameUs=nameUs)


@app.route('/newClass/<int:id>', methods=['GET', 'POST'])
def edit_class(id):
    global classsId
    db_sess = db_session.create_session()
    a = []
    for i in db_sess.query(User).filter(User.classId == id):
        a.append([i.id, i.surname, i.name])
    classsId = id
    return render_template('classs.html',
                           title='Редактирование класса',
                           news=a, us=us, nameUs=nameUs)


@app.route('/class_delete/<int:id>', methods=['GET', 'POST'])
def class_delete(id):
    db_sess = db_session.create_session()
    classs = db_sess.query(Classs).filter(Classs.id == id).first()
    if admin:
        db_sess.delete(classs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/admin')


@app.route('/teacher_delete/<int:id>', methods=['GET', 'POST'])
def teacher_delete(id):
    db_sess = db_session.create_session()
    teacher = db_sess.query(Teacher).filter(Teacher.id == id).first()
    if admin:
        db_sess.delete(teacher)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/admin')


@app.route('/user_delete/<int:id>', methods=['GET', 'POST'])
def user_delete(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    if user:
        db_sess.delete(user)
        db_sess.commit()
    else:
        abort(404)
    return redirect(f'/newClass/{user.classId}')


@app.route('/admin_delete/<int:id>', methods=['GET', 'POST'])
def admin_delete(id):
    db_sess = db_session.create_session()
    admin = db_sess.query(Admin).filter(Admin.id == id).first()
    if admin:
        db_sess.delete(admin)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/developer')


if __name__ == '__main__':
    main()
