from flask import render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user, login_user, logout_user
from clientManager.entities import User
from clientManager import app, db
from clientManager.inputforms import LoginForm, RegistrationForm


@app.route('/')
def index():
    u = User("Fabian", "fabi@fawolf.de")
    u.set_password('abcd')
    print(u.check_password('abcd'))
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
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/profile')
@login_required
def profile():
    user = current_user
    print("name: "+user.username)
    return render_template('profile.html', user=user)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    logout_user()
    return redirect(url_for('index'))
