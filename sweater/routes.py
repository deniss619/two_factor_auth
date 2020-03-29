import base64

from flask import render_template, redirect, url_for, request, flash, send_file, make_response
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

import glob, random
from PIL import Image

from sweater import db, app
from sweater.models import User


@app.route('/success', methods=['GET'])
def success():
    return render_template('index.html')


@app.route('/greet', methods=['GET'])
@login_required
def say_hello():
    return 'hello from server'


# @app.route('/', methods=['GET', 'POST'])
# def login_page():
#     login = request.form.get('login')
#     password = request.form.get('password')
#
#     if login and password:
#         user = User.query.filter_by(login=login).first()
#
#         if user and check_password_hash(user.password, password):
#             login_user(user)
#
#             next_page = request.args.get('next')
#             return redirect(next_page or url_for('success'))
#         else:
#             flash('Ошибка в логине или пароле')
#     else:
#         flash('Введите логин и пароль')
#     return render_template('login.html')


@app.route('/firstFactor', methods=['GET', 'POST'])
def firstFactor():
    login = request.form.get('login')
    password = request.form.get('password')
    coordinate = request.form.get("coordinate")
    if coordinate is not None:
        coordinateMass = []
        buf = ''
        for i in range(len(coordinate)):
            if (coordinate[i] != ','):
                buf += str(coordinate[i])
            else:
                coordinateMass.append(int(buf))
                buf = ''
        coordinateMass.append(int(buf))
    if login and password and login!=' ' and password!=' ':
        user = User.query.filter_by(login=login).first()
        if user and user!=' ':
            if coordinate is None:
                user.counter = 0
                db.session.add(user)
                db.session.commit()
        if user and check_password_hash(user.password, password):
            if coordinate is not None:
                if(coordinateMass[0] < 100 and coordinateMass[1] < 100):
                    counter = user.counter + 1
                    user.counter = counter
                    db.session.add(user)
                    db.session.commit()
                else:
                    user.counter = 0
                    db.session.add(user)
                    db.session.commit()
            else:
                user.counter = 0
                db.session.add(user)
                db.session.commit()
            if (user.counter == 0):
                try:
                    return generate_img(user.pass_img)
                except Exception as e:
                    return str(e)
            elif (0 < user.counter < 2):
                try:
                    return generate_img(user.pass_img)
                except Exception as e:
                    return str(e)
            else:
                login_user(user)
                user.counter = 0
                db.session.add(user)
                db.session.commit()
                return 'success'
        else:
            return 'error'
    else:
        flash('Введите логин и пароль')
    return render_template('login.html')


def generate_img(mass):
    images = glob.glob("./sweater/static/image/*.png")

    newimg = Image.new('RGB', (494, 494))
    random_mas = random.sample(range(400), 400)
    random_mas[random_mas.index(0)] = 400
    strPassImg = '4,5,6'
    mass = []
    g = 0
    buf = ''
    for i in range(len(strPassImg)):
        if (strPassImg[i] != ','):
            buf += str(strPassImg[i])
        else:
            mass.append(int(buf))
            buf = ''
    mass.append(int(buf))
    for i in range(len(mass)):
        if (random_mas.index(mass[i]) > 168):
            random_mas[random.sample(range(168), 1)[0]] = mass[i]
    g = 1
    for i in range(13):
        for j in range(13):
            img = Image.open('./sweater/static/image/' + str(random_mas[g]) + '.png')
            g += 1
            newimg.paste(img, (i * 38, j * 38))
    newimg.save("./sweater/static/user_img.png")
    image = open("./sweater/static/user_img.png", 'rb')
    img_read = image.read()
    img_encode=base64.encodestring(img_read)
    return img_encode


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
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd, pass_img=pass_img)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('firstFactor'))

    return render_template('register.html')


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