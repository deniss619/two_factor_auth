import random

from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from sweater import db, app
from sweater import module
from sweater.models import User


@app.route('/success', methods=['GET'])
@login_required
def success():
    return render_template('index.html')


@app.route('/greet', methods=['GET'])
@login_required
def say_hello():
    return 'hello from server'


@app.route('/', methods=['GET', 'POST'])
def firstFactor():
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password and login != ' ' and password != ' ':
        user = User.query.filter_by(login=login).first()
        if user and user != ' ':
            if user and check_password_hash(user.password, password):
                return 'checkMethodForm'
        else:
            return 'error'
    else:
        flash('Введите логин и пароль')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
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
            user = User.query.filter_by(login=login).first()
            if user is None:
                hash_pwd = generate_password_hash(password)
                probability = []
                for i in range(50):
                    probability.append(random.randint(22, 30))
                zone = module.gen_zone(list(map(int, pass_img.split(','))))
                new_user = User(login=login, password=hash_pwd, pass_img=pass_img, banned=0, zone=zone,
                                probability=probability)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('firstFactor'))
            else:
                flash('Такой пользователь уже существует')
    return render_template('register.html')


@app.route('/checkMethod', methods=['GET', 'POST'])
def checkMethod():
    method = request.form.get("method")
    if method == '1':
        return 'triangle'
    elif method == '2':
        return 'diagonal'
    else:
        return 'frame'


@app.route('/secondFactor', methods=['POST'])
def secondFactor():
    login = request.form.get('login')
    coordinate = request.form.get("coordinate")
    fast_mod = request.form.get("fastMod")
    method = request.form.get("method")
    user = User.query.filter_by(login=login).first()
    if coordinate is not None:
        coordinate_mass = list(map(int, coordinate.replace('{', '').replace('}', '').split(',')))
    # user.banned = 0
    user.false_click_counter = 0
    db.session.add(user)
    db.session.commit()
    if user.banned != 1:
        if coordinate is not None:
            if method == '1':
                result = module.check_triangle(coordinate_mass, user, fast_mod)
            elif method == '2':
                result = module.check_diagonal(coordinate_mass, user, fast_mod)
            elif method == '3':
                result = module.check_frame(list(map(int, request.form.get("coordinate").split(','))), user, fast_mod)
            if result:
                user.counter += 1
                db.session.add(user)
                db.session.commit()
            else:
                user.counter = 0
                user.false_click_counter += 1
                db.session.add(user)
                db.session.commit()

            if user.false_click_counter > 5:
                user.banned = 1
                user.false_click_counter = 0
                db.session.add(user)
                db.session.commit()
                return 'banned'
        else:
            user.counter = 0
            db.session.add(user)
            db.session.commit()

        if 0 <= user.counter < 5:
            if method == '1':
                return module.generate_img(user, 1)
            elif method == '2':
                return module.generate_img(user, 2)
            elif method == '3':
                return jsonify({'img1': module.make_mass_for_img(user, 3), 'img2': module.generate_img(user, 3).decode('ascii')})

        else:
            login_user(user)
            user.counter = 0
            db.session.add(user)
            db.session.commit()
            return 'success'
    else:
        return 'banned'


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        logout_user()
    return redirect(url_for('firstFactor'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('firstFactor') + '?next=' + request.url)
    return response
