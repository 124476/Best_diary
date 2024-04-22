import os
from base64 import encode, decode
from os import abort

from flask import Flask, render_template, redirect, make_response, request
from flask_restful import abort, Api

from cryptography.fernet import Fernet
import teachers_api
import tems_api
import user_api
import users_resource
import teachers_resource
from data import db_session
from data.admins import Admin
from data.developers import Developer
from data.homeWork import HomeWork
from data.tems import Tems
from data.evaluations import Evaluation
from data.teachers import Teacher
from data.users import User
from data.classes import Classs
from data.predmet import Predmet
from data.predmetAndTeacher import PredmetAndTeacher
from forms.admin import RegisterFormAdmin
from forms.classs import RegisterFormClass
from forms.homeWork import RegisterFormHomeWork
from forms.loginBack import LoginLoginBack
from forms.passwordBack import LoginPasswordBack
from forms.predmet import RegisterFormEvaluation
from forms.teacher import RegisterFormTeacher
from forms.teacherAdmin import RegisterFormTeacherAdmin
from forms.teacherClass import RegisterFormTeacherClass
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user

from string import ascii_letters, digits

alphabet_list = ascii_letters + digits
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from forms.userAdmin import RegisterFormUserAdmin

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

db_sess = db_session.global_init('db/Dbase.db')

# для списка объектов
api.add_resource(users_resource.UsersListResource, '/api/v2/users')
api.add_resource(teachers_resource.TeachersListResource, '/api/v2/teachers')

# для одного объекта
api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:users_id>')
api.add_resource(teachers_resource.TeachersResource,
                 '/api/v2/teachers/<int:teachers_id>')

app.register_blueprint(user_api.blueprint)
app.register_blueprint(teachers_api.blueprint)
app.register_blueprint(tems_api.blueprint)


@app.route("/")
def index():
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        if us == 'user':
            return redirect("/user")
        elif us == 'teacher':
            return redirect("/teacher")
        elif us == 'admin':
            return redirect("/admin")
        elif us == 'developer':
            return redirect("/developer")

    db_sess = db_session.create_session()
    a = []
    for i in db_sess.query(Tems):
        a.append([i.name, i.text.split('\\n')])
    db_sess.close()
    return render_template("index.html", us="None", listTems=a, bg='img')


@app.route("/admin")
def admin():
    coc = request.cookies.get("coc", 0)
    if coc:
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        nameUs = f'Здравствуйте {userUs.name} {userUs.surname}'
        us = coc.split(';')[1]
        a = []
        for i in db_sess.query(Classs).filter(Classs.adminId == userUs.id):
            a.append([i.id, i.name])
        b = []
        for i in db_sess.query(Teacher).filter(Teacher.adminId == userUs.id):
            b.append([i.id, i.name, i.surname])
        db_sess.close()
        return render_template("admin.html", us=us, nameUs=nameUs, news=a,
                               newss=b, bg='img')
    else:
        return redirect("/")


@app.route("/allUsers")
def allUsers():
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        nameUs = f'Здравствуйте {userUs.name} {userUs.surname}'
        db_sess = db_session.create_session()
        a = []
        for i in db_sess.query(User):
            a.append([i.id, i.surname, i.name])
        db_sess.close()
        return render_template('allUsers.html',
                               title='Ученики',
                               news=a, us=us, nameUs=nameUs, bg='img')
    else:
        return redirect("/")


@app.route("/registerHomeWork/<int:pred>/<int:clas>", methods=['GET', 'POST'])
def registerHomeWork(pred, clas):
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        nameUs = f'Здравствуйте {userUs.name} {userUs.surname}'
        db_sess = db_session.create_session()
        userUs = db_sess.query(Teacher).filter(
            Teacher.id == int(coc.split(';')[0])).first()
        form = RegisterFormHomeWork()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            homeWork = db_sess.query(HomeWork).filter(
                HomeWork.classId == clas).filter(
                HomeWork.predmetId == pred).filter(
                HomeWork.teacherId == userUs.id).first()
            if homeWork:
                db_sess.delete(homeWork)

            homeWork = HomeWork(
                predmetId=pred,
                classId=clas,
                teacherId=userUs.id,
                textDz=form.textDz.data
            )

            db_sess.add(homeWork)
            db_sess.commit()
            db_sess.close()
            return redirect(f'/teacher')
        db_sess.close()
        return render_template('registerHomeWork.html', title='Домашняя работа',
                               form=form, us=us, nameUs=nameUs)
    return redirect('/')


@app.route("/homeWork/<string:predmetName>")
def homeWork(predmetName):
    coc = request.cookies.get("coc", 0)
    if coc:
        userId = int(coc.split(';')[0])
        us = coc.split(';')[1]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        nameUs = f'Здравствуйте {userUs.name} {userUs.surname}'
        db_sess = db_session.create_session()
        a = []
        d = db_sess.query(Predmet)
        for i in d:
            if i.name == predmetName:
                pred = i.id
        for i in db_sess.query(HomeWork).filter(HomeWork.predmetId == pred) \
                .filter(HomeWork.classId == db_sess.query(User).filter(User.id == userId)[0].classId):
            a.append([db_sess.query(Predmet).filter(Predmet.id == pred)[0].name, i.textDz.split('\n')])
        if not a:
            a = [[db_sess.query(Predmet).filter(Predmet.id == pred)[0].name, ['Ничего не задали']]]

        res = make_response(
            render_template("homeWork.html", us=us, nameUs=nameUs, news=a))
        db_sess.close()
        return res
    else:
        return redirect('/')


@app.route("/classes/<int:id>")
def classes(id):
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        nameUs = f'Здравствуйте {userUs.name} {userUs.surname}'
        db_sess = db_session.create_session()
        a = []
        for i in db_sess.query(User).filter(User.classId == id):
            a.append([i.id, i.surname, i.name])

        db_sess.close()
        res = make_response(
            render_template("classes.html", us=us, nameUs=nameUs, news=a, bg='img'))
        res.set_cookie('coc',
                       coc.split(';')[0] + ';' + coc.split(';')[1] + ';' +
                       coc.split(';')[2] + ';' + str(id),
                       max_age=60 * 60 * 24 * 7)
        return res
    else:
        return redirect('/')


@app.route("/allTeachers")
def allTeachers():
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        nameUs = f'Здравствуйте {userUs.name} {userUs.surname}'
        db_sess = db_session.create_session()
        a = []
        for i in db_sess.query(Teacher):
            a.append([i.id, i.surname, i.name])
        db_sess.close()
        return render_template("allTeachers.html", us=us, nameUs=nameUs,
                               news=a, bg='img')
    else:
        return redirect("/")


@app.route("/allTeachersAdmin")
def allTeachersAdmin():
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        nameUs = f'Здравствуйте {userUs.name} {userUs.surname}'
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        a = []
        for i in db_sess.query(Teacher).filter(Teacher.adminId == userUs.id):
            a.append([i.id, i.surname, i.name])
        db_sess.close()
        return render_template("allTeachersAdmin.html", us=us, nameUs=nameUs,
                               news=a, bg='img')
    else:
        return redirect("/")


@app.route("/developer")
def developer():
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        nameUs = f'Здравствуйте {userUs.name} {userUs.surname}'
        a = []
        for i in db_sess.query(Admin).all():
            a.append([i.id, i.surname, i.name, i.school])

        db_sess.close()
        return render_template("developer.html", news=a, us=us, nameUs=nameUs,
                               bg='img')
    else:
        return redirect("/")


@app.route("/teacher")
def teacher():
    coc = request.cookies.get("coc", 0)
    if coc:
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        nameUs = f'Здравствуйте {userUs.name} {userUs.surname}'
        a = []
        for i in db_sess.query(PredmetAndTeacher).filter(
                PredmetAndTeacher.idTeacher == userUs.id):
            classs = db_sess.query(Classs).filter(
                Classs.id == i.idClass).first()
            predmet = db_sess.query(Predmet).filter(
                Predmet.id == i.idPredmet).first()
            a.append([classs.id, classs.name, predmet.name, predmet.id])
        db_sess.close()
        return render_template("teacher.html", news=a, nameUs=nameUs, bg='img')
    else:
        return redirect("/")


@app.route("/user", methods=['GET', 'POST'])
def user():
    if request.form.get("edit"):
        return redirect(f"/homeWork/{request.form.get('edit')}")
    coc = request.cookies.get("coc", 0)
    if coc:
        db_sess = db_session.create_session()
        userUs = db_sess.query(User).filter(
            User.id == int(coc.split(';')[0])).first()
        us = coc.split(';')[1]
        headings = ["Предмет", "Средний балл"]
        a = []

        mx = 0
        for i in db_sess.query(Predmet):
            evalutions = db_sess.query(Evaluation).filter(
                Evaluation.idUser == userUs.id).filter(
                Evaluation.idPredmet == i.id)
            p = 0
            for _ in evalutions:
                p += 1
            if mx < p:
                mx = p

        for i in range(mx, 0, -1):
            headings.insert(1, str(i))

        kk = 0

        for i in db_sess.query(Predmet).order_by(Predmet.name):
            kk += 1
            evalutions = db_sess.query(Evaluation).filter(
                Evaluation.idUser == userUs.id).filter(
                Evaluation.idPredmet == i.id)

            b = ['' for i in range(len(headings))]
            b[0] = i.name
            sm = 0
            k = 0
            if evalutions:
                for j in evalutions:
                    sm += j.type
                    k += 1
                    b[headings.index(str(k))] = j.type
                if k != 0:
                    b[-1] = str((sm / k * 100) // 1 / 100)
                else:
                    b[-1] = '-'
            else:
                b[-1] = '-'
            a.append(b)

        db_sess.close()
        return render_template("user.html", headings=headings, data=a, us=us,
                               bg='img')
    else:
        return redirect("/")


@app.route("/predmet/<int:id>/<int:pred>")
def predmet(id, pred):
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Teacher).filter(
            Teacher.id == int(coc.split(';')[0])).first()
        evalutions = db_sess.query(Evaluation).filter(
            Evaluation.idUser == id).filter(
            Evaluation.idTeacher == userUs.id).filter(
            Evaluation.idPredmet == pred)

        a = []
        for i in evalutions:
            a.append([i.id, i.name, i.type])

        classs = db_sess.query(Classs).filter(
            Classs.id == db_sess.query(User).filter(
                User.id == id).first().classId).first()
        db_sess.close()
        return render_template("predmet.html", news=a, userr=id, predmett=pred,
                               us=us, classs=classs.id)
    else:
        return redirect("/")


@app.route("/teacher_class/<int:id>/<int:pred>", methods=['GET', 'POST'])
def teacher_class(id, pred):
    if request.form.get("edit"):
        return redirect(f"/predmet/{request.form.get('edit')}/{pred}")
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        headings = ["№", "Ученик", "Средний балл", '']
        db_sess = db_session.create_session()
        userUs = db_sess.query(Teacher).filter(
            Teacher.id == int(coc.split(';')[0])).first()
        a = []
        for i in db_sess.query(User).filter(User.classId == id):
            evalutions = db_sess.query(Evaluation).filter(
                Evaluation.idUser == i.id).filter(
                Evaluation.idTeacher == userUs.id).filter(
                Evaluation.idPredmet == pred)

            for j in evalutions:
                if j.name not in headings:
                    headings.insert(2, j.name)

        kk = 0
        for i in db_sess.query(User).filter(User.classId == id):
            kk += 1
            evalutions = db_sess.query(Evaluation).filter(
                Evaluation.idUser == i.id).filter(
                Evaluation.idTeacher == userUs.id).filter(
                Evaluation.idPredmet == pred)

            b = ['' for i in range(len(headings))]
            b[0] = str(kk)
            b[1] = i.surname + ' ' + i.name
            sm = 0
            k = 0
            if evalutions:
                for j in evalutions:
                    b[headings.index(j.name)] = j.type
                    sm += j.type
                    k += 1
                if k != 0:
                    b[-2] = str((sm / k * 100) // 1 / 100)
                else:
                    b[-2] = '-'
            else:
                b[-2] = '-'
            b[-1] = i.id
            a.append(b)
        dz = db_sess.query(HomeWork).filter(HomeWork.classId == id).filter(HomeWork.teacherId == userUs.id).filter(
            HomeWork.predmetId == pred).first()
        if dz:
            textDz = dz.textDz
        else:
            textDz = ""

        db_sess.close()
        return render_template("teacher_class.html", headings=headings, data=a,
                               us=us, pred=pred, clas=id, textDz=textDz.split('\n'))
    else:
        return redirect("/")


@app.route('/newEvaluation/<int:id>/<int:pred>', methods=['GET', 'POST'])
def new_evaluation(id, pred):
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        nameUs = f'Здравствуйте {userUs.name} {userUs.surname}'
        db_sess = db_session.create_session()
        userUs = db_sess.query(Teacher).filter(
            Teacher.id == int(coc.split(';')[0])).first()
        form = RegisterFormEvaluation()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            eva = db_sess.query(Evaluation).filter(
                Evaluation.name == form.name.data).filter(
                Evaluation.idUser == id).filter(
                Evaluation.idPredmet == pred).first()
            if eva:
                db_sess.close()
                return render_template('registerEvaluation.html',
                                       title='Новая оценка',
                                       form=form,
                                       message="За такое событие оценка стоит!",
                                       us=us, nameUs=nameUs)

            eva = Evaluation(
                idUser=id,
                idPredmet=pred,
                type=form.type.data,
                name=form.name.data,
                idTeacher=userUs.id
            )

            db_sess.add(eva)
            db_sess.commit()

            classs = db_sess.query(Classs).filter(
                Classs.id == db_sess.query(User).filter(
                    User.id == id).first().classId).first()
            db_sess.close()
            return redirect(f'/teacher_class/{classs.id}/{pred}')
        db_sess.close()
        return render_template('registerEvaluation.html', title='Новая оценка',
                               form=form, us=us, nameUs=nameUs)
    return redirect('/')


@app.route('/predmet_delete/<int:id>/<int:userr>', methods=['GET', 'POST'])
def predmet_delete(id, userr):
    db_sess = db_session.create_session()
    eva = db_sess.query(Evaluation).filter(Evaluation.id == id).first()
    pred = eva.idPredmet
    if predmet:
        db_sess.delete(eva)
        db_sess.commit()
    else:
        abort(404)
    classs = db_sess.query(Classs).filter(
        Classs.id == db_sess.query(User).filter(
            User.id == userr).first().classId).first()
    db_sess.close()
    return redirect(f'/teacher_class/{classs.id}/{pred}')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    id = db_sess.query(User).get(user_id)
    db_sess.close()
    return id


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.login == form.login.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                res = make_response(redirect("/user"))
                res.set_cookie('coc', str(user.id) + ';' + 'user' + ';' + str(
                    user.name),
                               max_age=60 * 60 * 24 * 7)
                db_sess.close()
                return res
        else:
            teacher = db_sess.query(Teacher).filter(
                Teacher.login == form.login.data).first()
            if teacher:
                if teacher.check_password(form.password.data):
                    login_user(teacher, remember=form.remember_me.data)
                    res = make_response(redirect("/teacher"))
                    res.set_cookie('coc',
                                   str(teacher.id) + ';' + 'teacher' + ';' + str(
                                       teacher.name),
                                   max_age=60 * 60 * 24 * 7)
                    db_sess.close()
                    return res
            else:
                admin = db_sess.query(Admin).filter(
                    Admin.login == form.login.data).first()
                if admin:
                    if admin.check_password(form.password.data):
                        login_user(admin, remember=form.remember_me.data)
                        res = make_response(redirect("/admin"))
                        res.set_cookie('coc',
                                       str(admin.id) + ';' + 'admin' + ';' + str(
                                           admin.name),
                                       max_age=60 * 60 * 24 * 7)
                        db_sess.close()
                        return res
                else:
                    developer = db_sess.query(Developer).filter(
                        Developer.login == form.login.data).first()
                    if developer:
                        if developer.check_password(form.password.data):
                            login_user(developer,
                                       remember=form.remember_me.data)
                            res = make_response(redirect("/developer"))
                            res.set_cookie('coc',
                                           str(developer.id) + ';' + 'developer' + ';' + str(
                                               developer.login),
                                           max_age=60 * 60 * 24 * 7)
                            db_sess.close()
                            return res
            db_sess.close()
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form, us="None")
    return render_template('login.html', title='Авторизация', form=form)


def send_email(emailOther, text):
    # Заполните эти поля вашими данными
    sender_email = "bestdiaryrussian@gmail.com"  # gmail почта, к которой привязан пароль приложения
    receiver_email = emailOther  # кому
    password = "scnx oqpv qwxh ipwx"  # пароль приложения (в gmail получил в разделе безопасность - пароль приложений)
    subject = "Восстановление пароля"
    body = text  # текст сообщения

    # Создание объекта сообщения
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Добавление тела письма
    message.attach(MIMEText(body, 'plain'))

    # Создание объекта сессии SMTP
    session = smtplib.SMTP('smtp.gmail.com', 587)  # Укажите здесь свой SMTP сервер
    session.starttls()  # Активация шифрования
    session.login(sender_email, password)  # Авторизация на сервере

    # Отправка сообщения
    session.sendmail(sender_email, receiver_email, message.as_string())
    session.quit()


def caesar_code(text, shift):
    shift_text = ''

    for c in text:
        if c not in alphabet_list:
            shift_text += c
            continue

        i = (alphabet_list.index(c) + shift) % len(alphabet_list)
        shift_text += alphabet_list[i]

    return shift_text


@app.route('/password', methods=['GET', 'POST'])
def passwordBack():
    form = LoginPasswordBack()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.login == form.login.data).first()
        if user:
            txt = str(user.id) + ";;;" + "user"
            encoded = caesar_code(txt, shift=125)

            send_email(user.email, "Для восстановления доступа перейдите по ссылке: \n "
                                   "http://127.00.1:5000/returnPassword/" + str(encoded))
            db_sess.close()
            return redirect("/passwordTest")
        else:
            teacher = db_sess.query(Teacher).filter(
                Teacher.login == form.login.data).first()
            if teacher:
                txt = str(teacher.id) + ";;;" + "teacher"
                encoded = caesar_code(txt, shift=13)

                send_email(teacher.email, "Для восстановления доступа перейдите по ссылке: \n "
                                          "http://127.00.1:5000/returnPassword/" + str(encoded))
                db_sess.close()
                return redirect("/passwordTest")
            else:
                admin = db_sess.query(Admin).filter(
                    Admin.login == form.login.data).first()
                if admin:
                    txt = str(admin.id) + ";;;" + "admin"
                    encoded = caesar_code(txt, shift=13)

                    send_email(admin.email, "Для восстановления доступа перейдите по ссылке: \n "
                                            "http://127.00.1:5000/returnPassword/" + str(encoded))
                    db_sess.close()
                    return redirect("/passwordTest")
            db_sess.close()
            return render_template('password.html',
                                   message="Неправильный логин", form=form)
    return render_template('password.html', title='Восстановление пароля', form=form)


@app.route('/passwordTest')
def passwordTest():
    return render_template('passwordTest.html', title='Восстановление пароля')


@app.route('/returnPassword/<string:text>', methods=['GET', 'POST'])
def returnPassword(text):
    db_sess = db_session.create_session()
    decoded = caesar_code(text, shift=-13)
    form = LoginLoginBack()
    if form.validate_on_submit():
        userId, userUs = decoded.split(';;;')
        if userUs == "user":
            user = db_sess.query(User).get(userId)
        elif userUs == "teacher":
            user = db_sess.query(Teacher).get(userId)
        elif userUs == "admin":
            user = db_sess.query(Admin).get(userId)
        else:
            return redirect("/")
        user.set_password(form.password.data)
        db_sess.commit()
        db_sess.close()
        return redirect('/login')
    db_sess.close()
    return render_template('returnPassword.html', title='Восстановление пароля', form=form)


@app.route('/logout')
def logout():
    res = make_response(redirect("/"))
    res.set_cookie("coc", '1', max_age=0)
    return res


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        nameUs = f'Здравствуйте {userUs.name} {userUs.surname}'
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(
                    User.login == form.login.data).first() \
                    or db_sess.query(Teacher).filter(
                Teacher.login == form.login.data).first() \
                    or db_sess.query(Admin).filter(
                Admin.login == form.login.data).first() \
                    or db_sess.query(Developer).filter(
                Developer.login == form.login.data).first():
                return render_template('register.html', title='Новый ученик',
                                       form=form,
                                       message="Такой логин уже есть", us=us,
                                       nameUs=nameUs)
            user = User(
                name=form.name.data,
                surname=form.surname.data,
                login=form.login.data,
                email=form.email.data,
                classId=-1
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            db_sess.close()
            return redirect(f'/allUsers')
        db_sess.close()
        return render_template('register.html', title='Новый ученик',
                               form=form, us=us, nameUs=nameUs)
    else:
        return redirect('/')


@app.route('/newAdmin', methods=['GET', 'POST'])
def new_admin():
    form = RegisterFormAdmin()
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        nameUs = f'Здравствуйте {userUs.name} {userUs.surname}'
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(
                    User.login == form.login.data).first() \
                    or db_sess.query(Teacher).filter(
                Teacher.login == form.login.data).first() \
                    or db_sess.query(Admin).filter(
                Admin.login == form.login.data).first() \
                    or db_sess.query(Developer).filter(
                Developer.login == form.login.data).first():
                db_sess.close()
                return render_template('registerAdmin.html',
                                       title='Новый админ',
                                       form=form,
                                       message="Такой логин уже есть", us=us,
                                       nameUs=nameUs)
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
            db_sess.close()
            return redirect('/developer')
        db_sess.close()
        return render_template('registerAdmin.html', title='Новый админ',
                               form=form, us=us, nameUs=nameUs)
    else:
        return redirect('/')


@app.route('/newTeacher', methods=['GET', 'POST'])
def new_teacher():
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        nameUs = f'Здравствуйте {userUs.name} {userUs.surname}'
        form = RegisterFormTeacher()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(
                    User.login == form.login.data).first() \
                    or db_sess.query(Teacher).filter(
                Teacher.login == form.login.data).first() \
                    or db_sess.query(Admin).filter(
                Admin.login == form.login.data).first() \
                    or db_sess.query(Developer).filter(
                Developer.login == form.login.data).first():
                return render_template('registerTeacher.html',
                                       title='Новый учитель',
                                       form=form,
                                       message="Такой логин уже есть", us=us,
                                       nameUs=nameUs)
            teacher = Teacher(
                surname=form.surname.data,
                name=form.name.data,
                login=form.login.data,
                email=form.email.data,
                adminId=-1
            )
            teacher.set_password(form.password.data)
            db_sess.add(teacher)
            db_sess.commit()
            db_sess.close()
            return redirect('/allTeachers')
        db_sess.close()
        return render_template('registerTeacher.html', title='Новый учитель',
                               form=form, us=us, nameUs=nameUs)
    else:
        return redirect("/")


@app.route('/newUserAdmin', methods=['GET', 'POST'])
def new_user_admin():
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        nameUs = f'Здравствуйте {userUs.name} {userUs.surname}'
        classsId = int(coc.split(';')[3])
        form = RegisterFormUserAdmin()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(
                User.login == form.login.data).first()
            if not user:
                db_sess.close()
                return render_template('registerUserAdmin.html',
                                       title='Новый ученик',
                                       form=form,
                                       message="Такого ученика не существует!",
                                       us=us, nameUs=nameUs)
            if not (user.classId == 0 or user.classId == -1):
                db_sess.close()
                return render_template('registerUserAdmin.html',
                                       title='Новый ученик',
                                       form=form,
                                       message="Такой ученик учится в другой школе!",
                                       us=us, nameUs=nameUs)
            user.adminId = int(coc.split(';')[0])
            user.classId = classsId
            db_sess.commit()
            db_sess.close()
            return redirect(f'/classes/{classsId}')
        db_sess.close()
        return render_template('registerUserAdmin.html', title='Новый ученик',
                               form=form, us=us, nameUs=nameUs)
    else:
        return redirect("/")


@app.route('/newTeacherAdmin', methods=['GET', 'POST'])
def new_teacher_admin():
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        nameUs = f'Здравствуйте {userUs.name} {userUs.surname}'
        form = RegisterFormTeacherAdmin()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            teacher = db_sess.query(Teacher).filter(
                Teacher.login == form.login.data).first()
            if not teacher:
                return render_template('registerTeacherAdmin.html',
                                       title='Новый учитель',
                                       form=form,
                                       message="Такого учителя не существует!",
                                       us=us, nameUs=nameUs)
            if teacher.adminId != -1:
                return render_template('registerTeacherAdmin.html',
                                       title='Новый учитель',
                                       form=form,
                                       message="Такой учитель работает в другой школе!",
                                       us=us, nameUs=nameUs)
            teacher.adminId = int(coc.split(';')[0])
            db_sess.commit()
            db_sess.close()
            return redirect('/allTeachersAdmin')
        db_sess.close()
        return render_template('registerTeacherAdmin.html',
                               title='Новый учитель', form=form, us=us,
                               nameUs=nameUs)
    else:
        return redirect("/")


@app.route('/newClass', methods=['GET', 'POST'])
def new_class():
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        nameUs = f'Здравствуйте {userUs.name} {userUs.surname}'
        form = RegisterFormClass()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            classs = Classs(
                name=form.name.data,
                adminId=int(coc.split(';')[0])
            )
            db_sess.add(classs)
            db_sess.commit()
            db_sess.close()
            return redirect('/admin')
        db_sess.close()
        return render_template('registerClass.html', title='Новый класс',
                               form=form, us=us, nameUs=nameUs)
    else:
        return redirect("/")


@app.route('/newTeacher/<int:id>', methods=['GET', 'POST'])
def edit_teacher(id):
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        nameUs = f'Здравствуйте {userUs.name} {userUs.surname}'
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
                db_sess.close()
                return redirect('/allTeachers')
            else:
                abort(404)
        return render_template('registerTeacher.html',
                               title='Редактирование учителя',
                               form=form, us=us, nameUs=nameUs)
    else:
        return redirect('/')


@app.route('/newUser/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        nameUs = f'Здравствуйте {userUs.name} {userUs.surname}'
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
                db_sess.close()
                return redirect(f'/developer')
            else:
                abort(404)
        db_sess.close()
        return render_template('register.html',
                               title='Редактирование ученика',
                               form=form, us=us, nameUs=nameUs)
    else:
        return redirect('/')


@app.route('/newAdmin/<int:id>', methods=['GET', 'POST'])
def edit_admin(id):
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        nameUs = f'Здравствуйте {userUs.name} {userUs.surname}'
        form = RegisterFormAdmin()
        if request.method == "GET":
            db_sess = db_session.create_session()
            admin = db_sess.query(Admin).filter(Admin.id == id).first()
            if admin:
                form.surname.data = admin.surname
                form.name.data = admin.name
                form.login.data = admin.login
                form.school.data = admin.school
                form.email.data = admin.email
            else:
                abort(404)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            admin = db_sess.query(Admin).filter(Admin.id == id).first()
            if admin:
                admin.surname = form.surname.data
                admin.name = form.name.data
                admin.login = form.login.data
                admin.email = form.email.data
                admin.school = form.school.data
                admin.set_password(form.password.data)
                db_sess.commit()
                db_sess.close()
                return redirect(f'/allUsers')
            else:
                abort(404)
        db_sess.close()
        return render_template('registerAdmin.html',
                               title='Редактирование директора',
                               form=form, us=us, nameUs=nameUs)
    else:
        return redirect('/')


@app.route('/class_delete/<int:id>', methods=['GET', 'POST'])
def class_delete(id):
    db_sess = db_session.create_session()
    classs = db_sess.query(Classs).filter(Classs.id == id).first()
    if classs:
        db_sess.delete(classs)
        db_sess.commit()
    else:
        abort(404)
        db_sess.close()
    return redirect('/admin')


@app.route('/newTeacherAdmin/<int:id>', methods=['GET', 'POST'])
def new_teacherAdmin(id):
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(
            Admin.id == int(coc.split(';')[0])).first()
        nameUs = f'Здравствуйте {userUs.name} {userUs.surname}'
        db_sess = db_session.create_session()
        userUs = db_sess.query(Teacher).filter(
            Teacher.id == int(coc.split(';')[0])).first()
        form = RegisterFormTeacherClass()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            classs = db_sess.query(Classs).filter(
                Classs.name == form.login.data).first()
            teacher = db_sess.query(Teacher).filter(Teacher.id == id).first()
            if not classs:
                db_sess.close()
                return render_template('registerTeacherClass.html',
                                       title='Подключение учителя',
                                       form=form,
                                       message="Такого класса в школе нет!",
                                       us=us, nameUs=nameUs)
            if classs.adminId != userUs.id:
                db_sess.close()
                return render_template('registerTeacherClass.html',
                                       title='Подключение учителя',
                                       form=form,
                                       message="Такого класса нет в школе!",
                                       us=us, nameUs=nameUs)
            predmet = db_sess.query(Predmet).filter(
                Predmet.id == form.predmet.data).first()
            if not predmet:
                db_sess.close()
                return render_template('registerTeacherClass.html',
                                       title='Подключение учителя',
                                       form=form,
                                       message="Такого предмета нет!", us=us,
                                       nameUs=nameUs)

            db_sess = db_session.create_session()
            predmetAndTeacher = PredmetAndTeacher(
                idPredmet=predmet.id,
                idClass=classs.id,
                idTeacher=teacher.id
            )
            db_sess.add(predmetAndTeacher)
            db_sess.commit()
            db_sess.close()
            return redirect('/allTeachersAdmin')
        db_sess.close()
        return render_template('registerTeacherClass.html',
                               title='Подключение учителя', form=form, us=us,
                               nameUs=nameUs)
    return redirect('/')


@app.route('/teacher_delete/<int:id>', methods=['GET', 'POST'])
def teacher_delete(id):
    db_sess = db_session.create_session()
    teacher = db_sess.query(Teacher).filter(Teacher.id == id).first()
    if admin:
        db_sess.delete(teacher)
        db_sess.commit()
    else:
        abort(404)
        db_sess.close()
    return redirect('/allTeachers')


@app.route('/user_deleteAdmin/<int:id>', methods=['GET', 'POST'])
def user_deleteAdmin(id):
    coc = request.cookies.get("coc", 0)
    if coc:
        classsId = int(coc.split(';')[3])
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()
        if user:
            user.adminId = -1
            user.classId = -1
            db_sess.commit()
            db_sess.close()
        else:
            abort(404)
            db_sess.close()
        return redirect(f'/classes/{classsId}')
    return redirect('/')


@app.route('/teacher_deleteAdmin/<int:id>', methods=['GET', 'POST'])
def teacher_deleteAdmin(id):
    db_sess = db_session.create_session()
    teacher = db_sess.query(Teacher).filter(Teacher.id == id).first()
    if teacher:
        teacher.adminId = -1
        db_sess.commit()
        db_sess.close()
    else:
        abort(404)
        db_sess.close()
    return redirect('/allTeachersAdmin')


@app.route('/uplode', methods=['POST', 'GET'])
def sample_file_upload():
    coc = request.cookies.get("coc", 0)
    if coc and coc.split(';')[1] == 'developer':
        if request.method == 'GET':
            return render_template("uplodeFails.html")
        elif request.method == 'POST':
            try:
                db_sess = db_session.create_session()
                file_content = request.files['file'].read().decode(
                    'utf-8')  # Прочитать содержимое файла как строку
                lines = file_content.splitlines()  # Разделить содержимое на строки
                name = lines[0]  # Первая строка - название
                text = '\n'.join(lines[1:])  # Остальные строки - текст
                tem = Tems(name=name, text=text)
                db_sess.add(tem)
                db_sess.commit()
                db_sess.close()
            except Exception as e:
                print(
                    f"Тип исключения: {type(e).__name__}, сообщение: {str(e)}")
            return redirect('/allTems')

    return redirect('/')


@app.route('/allTems', methods=['GET', 'POST'])
def all_tems():
    coc = request.cookies.get("coc", 0)
    if coc and coc.split(';')[1] == 'developer':
        db_sess = db_session.create_session()
        a = []
        for i in db_sess.query(Tems):
            a.append([i.name, i.text.split('\\n'), i.id])
        db_sess.close()
        return render_template(f'allTems.html', us="developer", news=a, bg='img')
    return redirect('/')


@app.route('/tems_delete/<int:id>', methods=['GET', 'POST'])
def tem_delete(id):
    db_sess = db_session.create_session()
    tem = db_sess.query(Tems).filter(Tems.id == id).first()
    if tem:
        db_sess.delete(tem)
        db_sess.commit()
        db_sess.close()
    else:
        abort(404)
        db_sess.close()
    return redirect(f'/allTems')


@app.route('/user_delete/<int:id>', methods=['GET', 'POST'])
def user_delete(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    if user:
        db_sess.delete(user)
        db_sess.commit()
        db_sess.close()
    else:
        abort(404)
        db_sess.close()
    return redirect(f'/allUsers')


@app.route('/admin_delete/<int:id>', methods=['GET', 'POST'])
def admin_delete(id):
    db_sess = db_session.create_session()
    admin = db_sess.query(Admin).filter(Admin.id == id).first()
    if admin:
        db_sess.delete(admin)
        db_sess.commit()
        db_sess.close()
    else:
        abort(404)
        db_sess.close()
    return redirect('/developer')


if __name__ == '__main__':
    app.run()
