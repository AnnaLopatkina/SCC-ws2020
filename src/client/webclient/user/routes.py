from flask import render_template, redirect, url_for, flash, session
from flask_login import current_user, login_user, login_required, logout_user

from webclient import app, db
from webclient.study.models import Study
from webclient.study.routes import getstudies
from webclient.user.forms import LoginForm, RegistrationForm, ProfileForm, RoleForm
from webclient.user.models import User, Role
from webclient.user.usermanagement import login_required_and_roles, createprofileform, createstudychoices, \
    get_role


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    return render_template('login.html', form=form)


@app.route('/login', methods=['POST'])
def login2():
    form = LoginForm()
    form.validate()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nutzername oder Passwort falsch')
            return redirect(url_for('login'))

        login_user(user, True)
        session['logged_in'] = True
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
        user = User(username=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        user.set_role(get_role("STUDENT"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    form = createprofileform(current_user.id)

    return render_template('profileedit.html', form=form)


@app.route('/profile', methods=['POST'])
@login_required
def profileedit():
    form = ProfileForm()

    if form.validate_on_submit():

        user = User.query.filter_by(id=current_user.id).first()

        if Study.query.filter_by(id=form.studies.data).first() is not None:
            user.study = Study.query.filter_by(id=form.studies.data).first().id
        else:
            r = getstudies()

            study = Study()
            print(r.json())
            study.id = [study for study in r.json()["studies"] if study['id'] == form.studies.data][0]['id']
            study.title = [study for study in r.json()["studies"] if study['id'] == form.studies.data][0]['title']

            db.session.add(study)
            user.study = study.id
            db.session.add(user)
            db.session.commit()

        user.username = form.name.data
        user.email = form.email.data
        user.semester = form.semester.data

        if form.passwordold.data != "":
            user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('profile'))

    form.studies.choices = createstudychoices()
    form.roles.choices = Role.query.all()

    return render_template('profileedit.html', form=form)


@app.route('/logout')
@login_required
def logout():
    session['logged_in'] = False
    logout_user()
    return redirect(url_for('index'))


@app.route("/users")
@login_required_and_roles(role="ADMIN")
def users_admin():
    data = db.session.query(User, Study).outerjoin(Study).all()

    return render_template("users.html", data=data)


@app.route("/editUser/<int:userid>", methods=['GET'])
@login_required_and_roles(role="ADMIN")
def edit_user(userid):
    form = createprofileform(userid)

    return render_template('profileedit.html', form=form)


@app.route('/editUser/<int:userid>', methods=['POST'])
@login_required_and_roles(role="ADMIN")
def edit_user_post(userid):
    form = ProfileForm()
    if form.validate_on_submit():

        user = User.query.filter_by(id=userid).first()

        if Study.query.filter_by(id=form.studies.data).first() is not None:
            user.study = Study.query.filter_by(id=form.studies.data).first().id
        else:
            r = getstudies()

            study = Study()
            study.id = [study for study in r.json()["studies"] if study['id'] == form.studies.data][0]['id']
            study.title = [study for study in r.json()["studies"] if study['id'] == form.studies.data][0]['title']

            db.session.add(study)
            user.study = study.id
            db.session.add(user)
            db.session.commit()

        user.username = form.name.data
        user.email = form.email.data
        user.semester = form.semester.data

        if form.passwordold.data != "":
            user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('edit_user', userid=userid))

    form.studies.choices = createstudychoices()
    return render_template('profileedit.html', form=form)


@app.route('/roles')
@login_required_and_roles(role="ADMIN")
def roles():
    return render_template("roles.html", roles=Role.query.all(), title="Rollen")


@app.route('/addRole', methods=['GET'])
@login_required_and_roles(role="ADMIN")
def addRole():
    roleform = RoleForm()
    return render_template("editRole.html", form=roleform)


@app.route('/addRole', methods=['POST'])
@login_required_and_roles(role="ADMIN")
def addRole_post():
    form = RoleForm()

    if form.validate_on_submit():
        role = Role()
        role.name = form.name.data
        db.session.add(role)
        db.session.commit()

        return redirect(url_for('roles'))

    render_template("editRole.html", form=form)
