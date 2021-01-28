import requests
from flask import render_template, redirect, url_for, flash, session

from webclient import app, db
from webclient.user.forms import LoginForm, RegistrationForm, ProfileForm, RoleForm, APITokenForm
from webclient.user.usermanagement import createprofileform, createstudychoices, \
    get_role, register_user, getToken, check_login, admin_required, get_roles, submit_user, find_all_users, getUser, \
    setStudyToken, create_role
from webclient.config import service_port, service_ip, api_version


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
        if session['is_admin']:
            session['studyapi_token'] = response.json()['study_token']

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
            form.roles.choices = [(int(role['id']), role['name']) for role in get_roles().json()['roles']]
            form.roles.data = str(getUser(session['id']).json()['roles'][0]['id'])

            return render_template('profileedit.html', form=form)

        return redirect(url_for('profile'))

    form.studies.choices = createstudychoices()
    form.roles.choices = [(int(role['id']), role['name']) for role in get_roles().json()['roles']]
    form.roles.data = str(getUser(session['id']).json()['roles'][0]['id'])

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
        if setStudyToken(r.json()['token']).status_code == 200:
            print("set admin study api token")
            session['studyapi_token'] = r.json()['token']

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
            form.roles.choices = [(int(role['id']), role['name']) for role in get_roles().json()['roles']]

            return render_template('profileedit.html', form=form)

        return redirect(url_for('edit_user', userid=userid))

    form.studies.choices = createstudychoices()
    form.roles.choices = [(int(role['id']), role['name']) for role in get_roles().json()['roles']]
    return render_template('profileedit.html', form=form)


@app.route('/roles')
@admin_required
def roles():
    roles = get_roles()

    return render_template("roles.html", roles=roles.json()['roles'], title="Rollen")


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
        response = create_role(form.name.data)

        if response.status_code == 200:
            return redirect(url_for('roles'))

        form.name.errors.append("Rolle existiert bereits!")

    return render_template("editRole.html", form=form)
