from flask import render_template, redirect, url_for, request, flash, send_file, make_response
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from sweater import db, app
from sweater.models import User


@app.route('/success', methods=['GET'])
def success():
    return render_template('index.html')


@app.route('/greet', methods=['GET'])
@login_required
def say_hello():
    return 'hello from server'


@app.route('/', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')
            return redirect(next_page or url_for('success'))
        else:
            flash('Ошибка в логине или пароле')
    else:
        flash('Введите логин и пароль')
    return render_template('login.html')


@app.route('/firstFactor', methods=['GET', 'POST'])
def firstFactor():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            try:
                return 'zzz.png'
            except Exception as e:
                return str(e)

        else:
            return make_response('Ошибка в логине или пароле', 301)
    else:
        flash('Введите логин и пароль')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    #URL='url(./templates/register.html)'
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    pass_img = request.form.get('pass_img')
    if request.method == 'POST':
        if not (login or password or password2):
            flash('Пожалуйста, заполните поля')
        elif password != password2:
            flash('Пароли не совпадают')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd, pass_img=pass_img)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))

    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        logout_user()
    return redirect(url_for('login_page'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response
