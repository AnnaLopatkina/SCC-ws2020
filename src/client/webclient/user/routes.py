import requests
from flask import render_template, redirect, url_for, flash, session
from flask_login import current_user, login_user, login_required, logout_user

from webclient import app, db
from webclient.study.models import Study
from webclient.study.routes import getstudies
from webclient.user.forms import LoginForm, RegistrationForm, ProfileForm, RoleForm, APITokenForm
from webclient.user.models import User, Role
from webclient.user.usermanagement import createprofileform, createstudychoices, \
    get_role, register_user, getToken, check_login, admin_required, getRoles, submit_user, find_all_users, getUser
from webclient.config import service_port, service_ip, api_version
from requests.auth import HTTPBasicAuth


@app.route('/')
def index():
    if not 'logged_in' in session:
        session['logged_in'] = False
        session['is_admin'] = False

    return render_template('index.html')


@app.route('/login', methods=['GET'])
def login():
    if session['logged_in']:
        return redirect(url_for('index'))

    form = LoginForm()

    return render_template('login.html', form=form)


@app.route('/login', methods=['POST'])
def login2():
    form = LoginForm()

    if form.validate_on_submit():
        # user = User.query.filter_by(email=form.email.data).first()
        # if user is None or not user.check_password(form.password.data):
        #     flash('Nutzername oder Passwort falsch')
        #     return redirect(url_for('login'))
        #
        # login_user(user, True)

        response = getToken(form.email.data, form.password.data)

        if response.status_code != 200:
            form.password.errors.append('Nutzername oder Passwort falsch!')
            return render_template('login.html', form=form)

        session['token'] = response.json()['token']
        session['id'] = response.json()['id']
        session['logged_in'] = True
        session['is_admin'] = response.json()['is_admin']

        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET'])
def register():
    form = RegistrationForm()

    return render_template('register.html', form=form)


@app.route('/register', methods=['POST'])
def register_post():
    form = RegistrationForm()

    if form.validate_on_submit():
        response = register_user(form.name.data, form.email.data, form.password.data)

        if response.status_code == 500:
            for error in response.json()['errors']:
                if error['error'] == 'email':
                    form.email.errors.append("Diese E-Mail kann nicht verwendet werden!")
            return render_template('register.html', form=form)

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/profile', methods=['GET'])
@check_login
def profile():
    form = createprofileform(session['id'])

    return render_template('profileedit.html', form=form)


@app.route('/profile', methods=['POST'])
@check_login
def profileedit():
    form = ProfileForm()

    if form.validate_on_submit():

        response = submit_user(form.user_id.data, form.passwordold.data, form.password.data, form.name.data,
                               form.email.data, form.semester.data, form.roles.data, form.studies.data)

        if response.status_code == 500:
            for error in response.json()['errors']:
                if error['error'] == 'password':
                    form.passwordold.errors.append("Passwort stimmt nicht!")

            form.studies.choices = createstudychoices()
            form.roles.choices = getRoles().json()['roles']

            return render_template('profileedit.html', form=form)

        # user = User.query.filter_by(id=current_user.id).first()
        #
        # if form.studies.data is not None:
        #
        #     if Study.query.filter_by(id=form.studies.data).first() is not None:
        #         user.study = Study.query.filter_by(id=form.studies.data).first().id
        #     else:
        #         studies = getstudies().json()['studies']
        #
        #         new_study = Study()
        #
        #         new_study.id = [study for study in studies if study['id'] == int(form.studies.data)][0]['id']
        #         new_study.title = [study for study in studies if study['id'] == int(form.studies.data)][0]['title']
        #
        #         db.session.add(new_study)
        #         user.study = new_study.id
        #         db.session.add(user)
        #         db.session.commit()
        #
        # user.username = form.name.data
        # user.email = form.email.data
        # user.semester = form.semester.data
        #
        # if form.passwordold.data != "":
        #     user.set_password(form.password.data)
        #
        # db.session.add(user)
        # db.session.commit()

        return redirect(url_for('profile'))

    form.studies.choices = createstudychoices()
    form.roles.choices = getRoles().json()['roles']

    return render_template('profileedit.html', form=form)


@app.route('/logout')
@check_login
def logout():
    session['logged_in'] = False
    session['is_admin'] = False
    return redirect(url_for('index'))


@app.route("/users")
@admin_required
def users_admin():
    data = find_all_users()
    data_json = data.json()

    return render_template("users.html", users=data.json()['users'])


@app.route("/apiToken", methods=['GET'])
@admin_required
def get_api_token():
    form = APITokenForm()

    return render_template("token_admin.html", form=form)


@app.route("/apiToken", methods=['POST'])
@admin_required
def get_api_token_post():
    form = APITokenForm()

    if form.validate_on_submit():
        url = "http://{}:{}/{}/getToken".format(service_ip, service_port, api_version)

        r = requests.get(url=url, auth=(form.username.data, form.password.data))

        if r.status_code != 200:
            print("request failed with status: {}".format(r.status_code))
            form.submit.errors.append('Es konnte kein API Key für diese Zugangsdaten erzeugt werden!')
            return render_template("token_admin.html", form=form)

        print(r.json())
        user = User.query.filter_by(id=current_user.id).first()
        user.api_token = r.json()['token']
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("profile"))

    return render_template("token_admin.html", form=form)


@app.route("/editUser/<int:userid>", methods=['GET'])
@admin_required
def edit_user(userid):
    form = createprofileform(userid)

    return render_template('profileedit.html', form=form)


@app.route('/editUser/<int:userid>', methods=['POST'])
@admin_required
def edit_user_post(userid):
    form = ProfileForm()
    if form.validate_on_submit():

        user = getUser(userid)

        response = submit_user(form.user_id.data, form.passwordold.data, form.password.data, form.name.data,
                               form.email.data, form.semester.data, form.roles.data, form.studies.data)

        if response.status_code == 500:
            for error in response.json()['errors']:
                if error['error'] == 'password':
                    form.passwordold.errors.append("Passwort stimmt nicht!")

            form.studies.choices = createstudychoices()
            form.roles.choices = getRoles().json()['roles']

            return render_template('profileedit.html', form=form)

        # if form.studies.data is not None:
        #
        #     if Study.query.filter_by(id=form.studies.data).first() is not None:
        #         user.study = Study.query.filter_by(id=form.studies.data).first().id
        #     else:
        #         studies = getstudies().json()['studies']
        #
        #         new_study = Study()
        #
        #         new_study.id = [study for study in studies if study['id'] == int(form.studies.data)][0]['id']
        #         new_study.title = [study for study in studies if study['id'] == int(form.studies.data)][0]['title']
        #
        #         db.session.add(new_study)
        #         user.study = new_study.id
        #         db.session.add(user)
        #         db.session.commit()
        #
        # user.username = form.name.data
        # user.email = form.email.data
        # user.semester = form.semester.data
        #
        # if form.passwordold.data != "":
        #     user.set_password(form.password.data)
        #
        # print(form.roles.data)
        # if form.roles.data is not None:
        #     if Role.query.filter_by(id=form.roles.data).first() is not None:
        #         user.clear_roles()
        #         print("set new role {}".format(Role.query.filter_by(id=form.roles.data).first().name))
        #         user.set_role(Role.query.filter_by(id=form.roles.data).first())
        #
        #         if userid == current_user.id:
        #             db.session.add(user)
        #             db.session.commit()
        #             redirect(url_for("logout"))
        #
        # db.session.add(user)
        # db.session.commit()
        return redirect(url_for('edit_user', userid=userid))

    form.studies.choices = createstudychoices()
    return render_template('profileedit.html', form=form)


@app.route('/roles')
@admin_required
def roles():
    return render_template("roles.html", roles=Role.query.all(), title="Rollen")


@app.route('/addRole', methods=['GET'])
@admin_required
def addRole():
    roleform = RoleForm()
    return render_template("editRole.html", form=roleform)


@app.route('/addRole', methods=['POST'])
@admin_required
def addRole_post():
    form = RoleForm()

    if form.validate_on_submit():
        role = Role()
        role.name = form.name.data
        db.session.add(role)
        db.session.commit()

        return redirect(url_for('roles'))

    render_template("editRole.html", form=form)
