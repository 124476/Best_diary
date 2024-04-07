import os
from os import abort

from flask import Flask, render_template, redirect, make_response, request
from flask_restful import reqparse, abort, Api, Resource

import teachers_api
import user_api
import users_resource
import teachers_resource
from data import db_session
from data.admins import Admin
from data.developers import Developer
from data.evaluations import Evaluation
from data.teachers import Teacher
from data.users import User
from data.classes import Classs
from data.predmet import Predmet
from data.predmetAndTeacher import PredmetAndTeacher
from forms.admin import RegisterFormAdmin
from forms.classs import RegisterFormClass
from forms.predmet import RegisterFormEvaluation
from forms.teacher import RegisterFormTeacher
from forms.teacherAdmin import RegisterFormTeacherAdmin
from forms.teacherClass import RegisterFormTeacherClass
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required

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
api.add_resource(teachers_resource.TeachersResource, '/api/v2/teachers/<int:teachers_id>')

app.register_blueprint(user_api.blueprint)
app.register_blueprint(teachers_api.blueprint)


def main():
    app.run()


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
    return render_template("index.html", us="None")


@app.route("/admin")
def admin():
    coc = request.cookies.get("coc", 0)
    if coc:
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(Admin.id == int(coc.split(';')[0])).first()
        us = coc.split(';')[1]
        nameUs = coc.split(';')[2]
        a = []
        for i in db_sess.query(Classs).filter(Classs.adminId == userUs.id):
            a.append([i.id, i.name])
        b = []
        for i in db_sess.query(Teacher).filter(Teacher.adminId == userUs.id):
            b.append([i.id, i.name, i.surname])
        return render_template("admin.html", us=us, nameUs=nameUs, news=a, newss=b)
    else:
        return redirect("/")


@app.route("/allUsers")
def allUsers():
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        nameUs = coc.split(';')[2]
        db_sess = db_session.create_session()
        a = []
        for i in db_sess.query(User):
            a.append([i.id, i.surname, i.name])
        return render_template('allUsers.html',
                               title='Ученики',
                               news=a, us=us, nameUs=nameUs)
    else:
        return redirect("/")


@app.route("/classes/<int:id>")
def classes(id):
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        nameUs = coc.split(';')[2]
        db_sess = db_session.create_session()
        a = []
        for i in db_sess.query(User).filter(User.classId == id):
            a.append([i.id, i.surname, i.name])

        res = make_response(render_template("classes.html", us=us, nameUs=nameUs, news=a))
        res.set_cookie('coc', coc.split(';')[0] + ';' + coc.split(';')[1] + ';' + coc.split(';')[2] + ';' + str(id),
                       max_age=60 * 60 * 24 * 7)
        return res
    else:
        return redirect('/')


@app.route("/allTeachers")
def allTeachers():
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        nameUs = coc.split(';')[2]
        db_sess = db_session.create_session()
        a = []
        for i in db_sess.query(Teacher):
            a.append([i.id, i.surname, i.name])
        return render_template("allTeachers.html", us=us, nameUs=nameUs, news=a)
    else:
        return redirect("/")


@app.route("/allTeachersAdmin")
def allTeachersAdmin():
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        nameUs = coc.split(';')[2]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Admin).filter(Admin.id == int(coc.split(';')[0])).first()
        a = []
        for i in db_sess.query(Teacher).filter(Teacher.adminId == userUs.id):
            a.append([i.id, i.surname, i.name])
        return render_template("allTeachersAdmin.html", us=us, nameUs=nameUs, news=a)
    else:
        return redirect("/")


@app.route("/developer")
def developer():
    coc = request.cookies.get("coc", 0)
    if coc:
        db_sess = db_session.create_session()
        us = coc.split(';')[1]
        nameUs = coc.split(';')[2]
        a = []
        for i in db_sess.query(Admin).all():
            a.append([i.id, i.surname, i.name, i.school])

        return render_template("developer.html", news=a, us=us, nameUs=nameUs)
    else:
        return redirect("/")


@app.route("/teacher")
def teacher():
    coc = request.cookies.get("coc", 0)
    if coc:
        db_sess = db_session.create_session()
        userUs = db_sess.query(Teacher).filter(Teacher.id == int(coc.split(';')[0])).first()
        nameUs = coc.split(';')[2]
        a = []
        for i in db_sess.query(PredmetAndTeacher).filter(PredmetAndTeacher.idTeacher == userUs.id):
            classs = db_sess.query(Classs).filter(Classs.id == i.idClass).first()
            predmet = db_sess.query(Predmet).filter(Predmet.id == i.idPredmet).first()
            a.append([classs.id, classs.name, predmet.name, predmet.id])
        return render_template("teacher.html", news=a, nameUs=nameUs)
    else:
        return redirect("/")


@app.route("/user")
def user():
    coc = request.cookies.get("coc", 0)
    if coc:
        db_sess = db_session.create_session()
        userUs = db_sess.query(User).filter(User.id == int(coc.split(';')[0])).first()
        us = coc.split(';')[1]
        headings = ["Предмет", "Средний балл"]
        a = []

        mx = 0
        for i in db_sess.query(Predmet):
            evalutions = db_sess.query(Evaluation).filter(Evaluation.idUser == userUs.id).filter(
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
            evalutions = db_sess.query(Evaluation).filter(Evaluation.idUser == userUs.id).filter(
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

        return render_template("user.html", headings=headings, data=a, us=us)
    else:
        return redirect("/")


@app.route("/predmet/<int:id>/<int:pred>")
def predmet(id, pred):
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Teacher).filter(Teacher.id == int(coc.split(';')[0])).first()
        evalutions = db_sess.query(Evaluation).filter(
            Evaluation.idUser == id).filter(Evaluation.idTeacher == userUs.id).filter(Evaluation.idPredmet == pred)

        a = []
        for i in evalutions:
            a.append([i.id, i.name, i.type])

        classs = db_sess.query(Classs).filter(
            Classs.id == db_sess.query(User).filter(User.id == id).first().classId).first()
        return render_template("predmet.html", news=a, userr=id, predmett=pred, us=us, classs=classs.id)
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
        userUs = db_sess.query(Teacher).filter(Teacher.id == int(coc.split(';')[0])).first()
        a = []
        for i in db_sess.query(User).filter(User.classId == id):
            evalutions = db_sess.query(Evaluation).filter(
                Evaluation.idUser == i.id).filter(Evaluation.idTeacher == userUs.id).filter(
                Evaluation.idPredmet == pred)

            for j in evalutions:
                if j.name not in headings:
                    headings.insert(2, j.name)

        kk = 0
        for i in db_sess.query(User).filter(User.classId == id):
            kk += 1
            evalutions = db_sess.query(Evaluation).filter(
                Evaluation.idUser == i.id).filter(Evaluation.idTeacher == userUs.id).filter(
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

        return render_template("teacher_class.html", headings=headings, data=a, us=us)
    else:
        return redirect("/")


@app.route('/newEvaluation/<int:id>/<int:pred>', methods=['GET', 'POST'])
def new_evaluation(id, pred):
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        nameUs = coc.split(';')[2]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Teacher).filter(Teacher.id == int(coc.split(';')[0])).first()
        form = RegisterFormEvaluation()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            eva = db_sess.query(Evaluation).filter(
                Evaluation.name == form.name.data).filter(Evaluation.idUser == id).filter(
                Evaluation.idPredmet == pred).first()
            if eva:
                return render_template('registerEvaluation.html', title='Новая оценка',
                                       form=form,
                                       message="За такое событие оценка стоит!", us=us, nameUs=nameUs)

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
                Classs.id == db_sess.query(User).filter(User.id == id).first().classId).first()
            return redirect(f'/teacher_class/{classs.id}/{pred}')
        return render_template('registerEvaluation.html', title='Новая оценка', form=form, us=us, nameUs=nameUs)
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
        Classs.id == db_sess.query(User).filter(User.id == userr).first().classId).first()
    return redirect(f'/teacher_class/{classs.id}/{pred}')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        nameUs = coc.split(';')[2]
    else:
        us = 'None'
        nameUs = 'None'

    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                res = make_response(redirect("/user"))
                res.set_cookie('coc', str(user.id) + ';' + 'user' + ';' + str(user.name),
                               max_age=60 * 60 * 24 * 7)
                return res
        else:
            teacher = db_sess.query(Teacher).filter(Teacher.login == form.login.data).first()
            if teacher:
                if teacher.check_password(form.password.data):
                    login_user(teacher, remember=form.remember_me.data)
                    res = make_response(redirect("/teacher"))
                    res.set_cookie('coc', str(teacher.id) + ';' + 'teacher' + ';' + str(teacher.name),
                                   max_age=60 * 60 * 24 * 7)
                    return res
            else:
                admin = db_sess.query(Admin).filter(Admin.login == form.login.data).first()
                if admin:
                    if admin.check_password(form.password.data):
                        login_user(admin, remember=form.remember_me.data)
                        res = make_response(redirect("/admin"))
                        res.set_cookie('coc', str(admin.id) + ';' + 'admin' + ';' + str(admin.name),
                                       max_age=60 * 60 * 24 * 7)
                        return res
                else:
                    developer = db_sess.query(Developer).filter(Developer.login == form.login.data).first()
                    if developer:
                        if developer.check_password(form.password.data):
                            login_user(developer, remember=form.remember_me.data)
                            res = make_response(redirect("/developer"))
                            res.set_cookie('coc', str(developer.id) + ';' + 'developer' + ';' + str(developer.login),
                                           max_age=60 * 60 * 24 * 7)
                            return res
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form, us="None", nameUs=nameUs)
    return render_template('login.html', title='Авторизация', form=form, us=us, nameUs=nameUs)


@app.route('/logout')
def logout():
    res = make_response(redirect("/"))
    res.set_cookie("coc", '1', max_age=0)
    return res


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        nameUs = coc.split(';')[2]
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
                classId=-1
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect(f'/allUsers')
        return render_template('register.html', title='Новый ученик', form=form, us=us, nameUs=nameUs)
    else:
        return redirect('/')


@app.route('/newAdmin', methods=['GET', 'POST'])
def new_admin():
    form = RegisterFormAdmin()
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        nameUs = coc.split(';')[2]
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
    else:
        return redirect('/')


@app.route('/newTeacher', methods=['GET', 'POST'])
def new_teacher():
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        nameUs = coc.split(';')[2]
        form = RegisterFormTeacher()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.login == form.login.data).first() \
                    or db_sess.query(Teacher).filter(Teacher.login == form.login.data).first() \
                    or db_sess.query(Admin).filter(Admin.login == form.login.data).first() \
                    or db_sess.query(Developer).filter(Developer.login == form.login.data).first():
                return render_template('registerTeacher.html', title='Новый учитель',
                                       form=form,
                                       message="Такой логин уже есть", us=us, nameUs=nameUs)
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
            return redirect('/allTeachers')
        return render_template('registerTeacher.html', title='Новый учитель', form=form, us=us, nameUs=nameUs)
    else:
        return redirect("/")


@app.route('/newUserAdmin', methods=['GET', 'POST'])
def new_user_admin():
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        nameUs = coc.split(';')[2]
        classsId = int(coc.split(';')[3])
        form = RegisterFormUserAdmin()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.login == form.login.data).first()
            if not user:
                return render_template('registerUserAdmin.html', title='Новый ученик',
                                       form=form,
                                       message="Такого ученика не существует!", us=us, nameUs=nameUs)
            if not (user.classId == 0 or user.classId == -1):
                return render_template('registerUserAdmin.html', title='Новый ученик',
                                       form=form,
                                       message="Такой ученик учится в другой школе!", us=us, nameUs=nameUs)
            user.adminId = int(coc.split(';')[0])
            user.classId = classsId
            db_sess.commit()
            return redirect(f'/classes/{classsId}')
        return render_template('registerUserAdmin.html', title='Новый ученик', form=form, us=us, nameUs=nameUs)
    else:
        return redirect("/")


@app.route('/newTeacherAdmin', methods=['GET', 'POST'])
def new_teacher_admin():
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        nameUs = coc.split(';')[2]
        form = RegisterFormTeacherAdmin()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            teacher = db_sess.query(Teacher).filter(Teacher.login == form.login.data).first()
            if not teacher:
                return render_template('registerTeacherAdmin.html', title='Новый учитель',
                                       form=form,
                                       message="Такого учителя не существует!", us=us, nameUs=nameUs)
            if teacher.adminId != -1:
                return render_template('registerTeacherAdmin.html', title='Новый учитель',
                                       form=form,
                                       message="Такой учитель работает в другой школе!", us=us, nameUs=nameUs)
            teacher.adminId = int(coc.split(';')[0])
            db_sess.commit()
            return redirect('/allTeachersAdmin')
        return render_template('registerTeacherAdmin.html', title='Новый учитель', form=form, us=us, nameUs=nameUs)
    else:
        return redirect("/")


@app.route('/newClass', methods=['GET', 'POST'])
def new_class():
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        nameUs = coc.split(';')[2]
        form = RegisterFormClass()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            classs = Classs(
                name=form.name.data,
                adminId=int(coc.split(';')[0])
            )
            db_sess.add(classs)
            db_sess.commit()
            return redirect('/admin')
        return render_template('registerClass.html', title='Новый класс', form=form, us=us, nameUs=nameUs)
    else:
        return redirect("/")


@app.route('/newTeacher/<int:id>', methods=['GET', 'POST'])
def edit_teacher(id):
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        nameUs = coc.split(';')[2]
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
        nameUs = coc.split(';')[2]
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
                return redirect(f'/developer')
            else:
                abort(404)
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
        nameUs = coc.split(';')[2]
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
                return redirect(f'/allUsers')
            else:
                abort(404)
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
    return redirect('/admin')


@app.route('/newTeacherAdmin/<int:id>', methods=['GET', 'POST'])
def new_teacherAdmin(id):
    coc = request.cookies.get("coc", 0)
    if coc:
        us = coc.split(';')[1]
        nameUs = coc.split(';')[2]
        db_sess = db_session.create_session()
        userUs = db_sess.query(Teacher).filter(Teacher.id == int(coc.split(';')[0])).first()
        form = RegisterFormTeacherClass()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            classs = db_sess.query(Classs).filter(Classs.name == form.login.data).first()
            teacher = db_sess.query(Teacher).filter(Teacher.id == id).first()
            if not classs:
                return render_template('registerTeacherClass.html', title='Подключение учителя',
                                       form=form,
                                       message="Такого класса в школе нет!", us=us, nameUs=nameUs)
            if classs.adminId != userUs.id:
                return render_template('registerTeacherClass.html', title='Подключение учителя',
                                       form=form,
                                       message="Такого класса нет в школе!", us=us, nameUs=nameUs)
            predmet = db_sess.query(Predmet).filter(Predmet.id == form.predmet.data).first()
            if not predmet:
                return render_template('registerTeacherClass.html', title='Подключение учителя',
                                       form=form,
                                       message="Такого предмета нет!", us=us, nameUs=nameUs)

            db_sess = db_session.create_session()
            predmetAndTeacher = PredmetAndTeacher(
                idPredmet=predmet.id,
                idClass=classs.id,
                idTeacher=teacher.id
            )
            db_sess.add(predmetAndTeacher)
            db_sess.commit()
            return redirect('/allTeachersAdmin')
        return render_template('registerTeacherClass.html', title='Подключение учителя', form=form, us=us,
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
        else:
            abort(404)
        return redirect(f'/classes/{classsId}')
    return redirect('/')


@app.route('/teacher_deleteAdmin/<int:id>', methods=['GET', 'POST'])
def teacher_deleteAdmin(id):
    db_sess = db_session.create_session()
    teacher = db_sess.query(Teacher).filter(Teacher.id == id).first()
    if admin:
        teacher.adminId = -1
        db_sess.commit()
    else:
        abort(404)
    return redirect('/allTeachersAdmin')


@app.route('/user_delete/<int:id>', methods=['GET', 'POST'])
def user_delete(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    if user:
        db_sess.delete(user)
        db_sess.commit()
    else:
        abort(404)
    return redirect(f'/allUsers')


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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
