import base64

from flask import render_template, redirect, url_for, request, flash, make_response
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

import random
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
    fastMod = request.form.get("fastMod")
    if coordinate is not None:
        coordinateMass=make_mass(coordinate)
    if login and password and login != ' ' and password != ' ':
        user = User.query.filter_by(login=login).first()
        if user and user != ' ':
            if coordinate is None:
                user.counter = 0
                user.false_click_counter = 0
                db.session.add(user)
                db.session.commit()
        # user.banned = 0
        # db.session.add(user)
        # db.session.commit()
        if (int(user.banned)!=1):
            if user and check_password_hash(user.password, password):
                if coordinate is not None:
                    if check_coordinates(coordinateMass, user, fastMod):
                        user.counter +=1
                        db.session.add(user)
                        db.session.commit()
                    else:
                        user.counter = 0
                        user.false_click_counter+=1
                        db.session.add(user)
                        db.session.commit()

                    if(user.false_click_counter>5):
                        user.banned=1
                        db.session.add(user)
                        db.session.commit()
                        return 'banned'

                else:
                    user.counter = 0
                    db.session.add(user)
                    db.session.commit()
                if (user.counter == 0):
                    try:
                        return generate_img(user)
                    except Exception as e:
                        print(user.counter,user)
                        return str(e)
                elif (0 < user.counter < 2):
                    try:
                        return generate_img(user)
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
            return 'banned'
    else:
        flash('Введите логин и пароль')
    return render_template('login.html')


def generate_img(user):
    newimg = Image.new('RGB', (481, 481))
    random_mas = random.sample(range(400), 400)
    random_mas[random_mas.index(0)] = 400
    mass = make_mass(user.pass_img)
    fake_img = random.choices([0, 1], weights=[1, 10])
    if fake_img[0] == 0:
        lose_img = random.sample(range(len(mass)), len(mass))
        for i in range(len(mass) - 1):
            if (random_mas.index(mass[lose_img[0]]) > 168):
                random_mas[random.sample(range(168), 1)[0]] = mass[lose_img[0]]
                del lose_img[0]
    else:
        for i in range(len(mass)):
            if (random_mas.index(mass[i]) > 168):
                random_mas[random.sample(range(168), 1)[0]] = mass[i]
    coordinates=''
    g = 1
    for i in range(13):
        for j in range(13):
            img = Image.open('./sweater/static/image/' + str(random_mas[g]) + '.png')
            g += 1
            newimg.paste(img, (i * 37, j * 37))
            for z in range(len(mass)):
                if random_mas[g-1] == mass[z]:
                    coordinates+=str((i*37)+18+1)+','+str((j*37)+18+1)+','
    coordinates = coordinates[0:-1]
    user.coordinates = coordinates
    db.session.add(user)
    db.session.commit()
    coordinates_mass = make_mass(user.coordinates)
    if(fake_img[0]==1):
        pass_img_1 = make_mass_for_coordinate(coordinates_mass, 0)
        pass_img_2 = make_mass_for_coordinate(coordinates_mass, 1)
        pass_img_3 = make_mass_for_coordinate(coordinates_mass, 2)
        S = 0.5*(abs((pass_img_2[0] - pass_img_1[0])*(pass_img_3[1] - pass_img_1[1]) -
                  (pass_img_3[0] - pass_img_1[0]) * (pass_img_2[1] - pass_img_1[1])))
        if S<9945 or S>59674:
            return generate_img(user)
        else:
            newimg.save("./sweater/static/user_img.png")
            image = open("./sweater/static/user_img.png", 'rb')
            img_read = image.read()
            img_encode = base64.encodebytes(img_read)
            return img_encode
    else:
        newimg.save("./sweater/static/user_img.png")
        image = open("./sweater/static/user_img.png", 'rb')
        img_read = image.read()
        img_encode = base64.encodebytes(img_read)
        return img_encode


def make_mass(coordinate):
    coordinateMass = []
    buf = ''
    for i in range(len(coordinate)):
        if (coordinate[i] != ','):
            buf += str(coordinate[i])
        else:
            coordinateMass.append(int(buf))
            buf = ''
    coordinateMass.append(int(buf))
    return coordinateMass


def make_mass_for_coordinate(coordinate, g):
    res = []
    counter = 0
    for i in range(int(len(coordinate) / 2)):
        buf = []
        buf.append(coordinate[counter])
        buf.append(coordinate[counter + 1])
        counter += 2
        res.append(buf)
    if len(res)>g:
        return res[g]


def check_coordinates(coordinates, user, fastMod):
    if fastMod == 'true':
        coordinates_mass = make_mass(user.coordinates)
        pass_img_1 = make_mass_for_coordinate(coordinates_mass, 0)
        pass_img_2 = make_mass_for_coordinate(coordinates_mass, 1)
        pass_img_3 = make_mass_for_coordinate(coordinates_mass, 2)
    else:
        user_img = make_mass(user.pass_img)
        pass_img_1 = pass_coordinates(user_img[0])
        pass_img_2 = pass_coordinates(user_img[1])
        pass_img_3 = pass_coordinates(user_img[2])
    if pass_img_1 and pass_img_2 and pass_img_3:
        a=(pass_img_1[0]-coordinates[0])*(pass_img_2[1]-pass_img_1[1])-(pass_img_2[0]-pass_img_1[0])*(pass_img_1[1]-coordinates[1])
        b = (pass_img_2[0] - coordinates[0]) * (pass_img_3[1] - pass_img_2[1]) - (pass_img_3[0] - pass_img_2[0]) * (pass_img_2[1] - coordinates[1])
        c = (pass_img_3[0] - coordinates[0]) * (pass_img_1[1] - pass_img_3[1]) - (pass_img_1[0] - pass_img_3[0]) * (pass_img_3[1] - coordinates[1])
        if((a>=0 and b>=0 and c>=0) or (a<=0 and b<=0 and c<=0)):
            return True
        else:
            return False
    else:
        return True


def pass_coordinates(user_img):

    for i in range(13):
        for j in range(13):
            image = Image.open("./sweater/static/user_img.png")
            cutImg = image.crop((37 * j, 37 * i, 37 * j + 37, 37 * i + 37))
            cutImg.save("./sweater/static/cut_img.png")
            image = open("./sweater/static/cut_img.png", 'rb')
            img_read = image.read()
            img_encode_1 = base64.encodebytes(img_read)

            image = Image.open("./sweater/static/image/"+str(user_img)+".png")
            image.thumbnail((37, 37))
            image.save("./sweater/static/pass_img.png")
            image = open("./sweater/static/pass_img.png", 'rb')
            img_read = image.read()
            img_encode_2 = base64.encodebytes(img_read)

            if (img_encode_1 == img_encode_2):
                mass=[(j*37)+18+1, (i*37)+18+1]
                return mass


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
                new_user = User(login=login, password=hash_pwd, pass_img=pass_img, banned=0)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('firstFactor'))
            else:
                flash('Такой пользователь уже существует')
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
