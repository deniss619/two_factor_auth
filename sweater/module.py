from PIL import Image
import base64
import random

from sweater import db, app


def make_mass_for_img(user, method=None):
    # генерирует массив из которого будет создано изображение
    img_size = 13
    random_mas = random.sample(range(400), 400)
    random_mas[random_mas.index(0)] = 400
    if method == 1:
        imgAmount = 4
    else:
        imgAmount = 3
    for i in make_mass(user.pass_img):
        del random_mas[random_mas.index(i)]
    random_mas = random.sample(random_mas, img_size ** 2)
    print(len(random_mas))
    password_images = random.sample(make_mass(user.pass_img), len(make_mass(user.pass_img)))
    zone = make_mass(user.zone)
    probability = make_mass(user.probability)
    for i in range(len(zone)):
        # в массив добавляются числа с повышенной вероятностью выпадения
        check = random.choices([0, 1], weights=[probability[i], 10])
        if (check[0] == 0 and zone[i] not in random_mas):
            random_mas[random.randint(0, img_size ** 2 - 1)] = zone[i]
    pass_img_coordinates = []

    for i in range(imgAmount):
        # в массив добавляются парольные изображения
        position = random.randint(0, img_size ** 2)
        if position not in pass_img_coordinates:
            pass_img_coordinates.append(position)
            random_mas[position] = password_images[i]
        else:
            i -= 1
    return random_mas


def generate_img(user, method=None):
    img_size = 13
    newimg = Image.new('RGB', (img_size * 37, img_size * 37))
    random_mas = make_mass_for_img(user, method)
    password_img_mass = make_mass(user.pass_img)
    coordinates = ''
    g = 0
    for i in range(img_size):
        for j in range(img_size):
            img = Image.open('./sweater/static/image/' + str(random_mas[g]) + '.png')
            newimg.paste(img, (i * 37, j * 37))
            for z in password_img_mass:
                if random_mas[g] == z:
                    coordinates += str((i * 37) + 18 + 1) + ',' + str((j * 37) + 18 + 1) + ','
            g += 1
    coordinates = coordinates[0:-1]
    user.coordinates = coordinates
    db.session.add(user)
    db.session.commit()
    coordinates_mass = make_mass(user.coordinates)
    if method != 1:
        return triangle_img(user, newimg)
    else:
        return diagonal_img(user, newimg)


def triangle_img(user, newimg):
    coordinates_mass = make_mass(user.coordinates)
    if len(coordinates_mass) < 6:
        newimg.save("./sweater/static/user_img.png")
        image = open("./sweater/static/user_img.png", 'rb')
        img_read = image.read()
        img_encode = base64.encodebytes(img_read)
        return img_encode
    else:
        pass_img_1 = [coordinates_mass[0], coordinates_mass[1]]
        pass_img_2 = [coordinates_mass[2], coordinates_mass[3]]
        pass_img_3 = [coordinates_mass[4], coordinates_mass[5]]
        S = 0.5 * (abs((pass_img_2[0] - pass_img_1[0]) * (pass_img_3[1] - pass_img_1[1]) -
                       (pass_img_3[0] - pass_img_1[0]) * (pass_img_2[1] - pass_img_1[1])))
        if S < 10718 or S > 64810:
            return generate_img(user)
        else:
            newimg.save("./sweater/static/user_img.png")
            image = open("./sweater/static/user_img.png", 'rb')
            img_read = image.read()
            img_encode = base64.encodebytes(img_read)
            return img_encode


def diagonal_img(user, newimg):
    coordinates_mass = make_mass(user.coordinates)
    k = []
    for i in range(4):
        buf = []
        buf.append(coordinates_mass[i + i])
        buf.append(coordinates_mass[i + i + 1])
        k.append(buf)
    for i in range(4):
        point1 = (k[2][0] - k[0][0]) * (k[1][1] - k[0][1]) - (k[2][1] - k[0][1]) - (k[1][0] - k[0][0])
        point2 = (k[3][0] - k[0][0]) * (k[1][1] - k[0][1]) - (k[3][1] - k[0][1]) - (k[1][0] - k[0][0])
        if (point1 <= 0 and point2 <= 0) or (point1 >= 0 and point2 >= 0):
            buf = []
            for j in range(3):
                buf.append(k[j + 1])
            buf.append(k[0])
            k = buf
        else:
            return generate_img(user, 1)
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


def checkTriangle(coordinates, user, fastMod):
    if fastMod == 'true':
        coordinates_mass = make_mass(user.coordinates)
        if len(coordinates_mass) < 6:
            return True
        else:
            pass_img_1 = [coordinates_mass[0], coordinates_mass[1]]
            pass_img_2 = [coordinates_mass[2], coordinates_mass[3]]
            pass_img_3 = [coordinates_mass[4], coordinates_mass[5]]
    else:
        user_img = make_mass(user.pass_img)
        pass_img_1 = pass_coordinates(user_img[0])
        pass_img_2 = pass_coordinates(user_img[1])
        pass_img_3 = pass_coordinates(user_img[2])
    if pass_img_1 and pass_img_2 and pass_img_3:
        a = (pass_img_1[0] - coordinates[0]) * (pass_img_2[1] - pass_img_1[1]) - (pass_img_2[0] - pass_img_1[0]) * (
                pass_img_1[1] - coordinates[1])
        b = (pass_img_2[0] - coordinates[0]) * (pass_img_3[1] - pass_img_2[1]) - (pass_img_3[0] - pass_img_2[0]) * (
                pass_img_2[1] - coordinates[1])
        c = (pass_img_3[0] - coordinates[0]) * (pass_img_1[1] - pass_img_3[1]) - (pass_img_1[0] - pass_img_3[0]) * (
                pass_img_3[1] - coordinates[1])
        if ((a >= 0 and b >= 0 and c >= 0) or (a <= 0 and b <= 0 and c <= 0)):
            return True
        else:
            return False
    else:
        return True


def checkDiagonal(coordinates, user, fastMod):
    k = []
    if fastMod == 'true':
        coordinates_mass = make_mass(user.coordinates)
        for i in range(4):
            k.append([coordinates_mass[i + i], coordinates_mass[i + i + 1]])
    else:
        user_img = make_mass(user.pass_img)
        for i in range(4):
            k.append(pass_coordinates(user_img[i]))
    x, y = checkCrossPoint(k)
    print(x, y)
    if (coordinates[0] - x) ** 2 + (coordinates[1] - y) ** 2 <= 100:
        print('yes')
        return True
    else:
        print('no')
        return False


def coordinateOfCrossPoint(k):
    # возвращает точку пересечения двух прямых 12 и 34 к[1,2,3,4]
    x = (k[0][0] * (k[1][1] - k[0][1]) * (k[3][0] - k[2][0]) -
         k[2][0] * (k[3][1] - k[2][1]) * (k[1][0] - k[0][0]) -
         k[0][1] * (k[1][0] - k[0][0]) * (k[3][0] - k[2][0]) +
         k[2][1] * (k[1][0] - k[0][0]) * (k[3][0] - k[2][0])) / (
                (k[1][1] - k[0][1]) * (k[3][0] - k[2][0]) - (k[3][1] - k[2][1]) * (k[1][0] - k[0][0]))

    y = (k[0][1] * (k[1][0] - k[0][0]) * (k[3][1] - k[2][1]) -
         k[2][1] * (k[1][1] - k[0][1]) * (k[3][0] - k[2][0]) -
         k[0][0] * (k[1][1] - k[0][1]) * (k[3][1] - k[2][1]) +
         k[2][0] * (k[1][1] - k[0][1]) * (k[3][1] - k[2][1])) / (
                (k[3][1] - k[2][1]) * (k[1][0] - k[0][0]) - (k[1][1] - k[0][1]) * (k[3][0] - k[2][0]))
    return x, y


def checkCrossPoint(k):
    mass = [k[0][0], k[1][0], k[2][0], k[3][0]]
    buf = []
    for i in range(4):
        minimum = min(mass)
        buf.append(k[mass.index(minimum)])
        mass[mass.index(minimum)] = max(mass) + 1
    if buf[0][0] == buf[1][0]:
        if (buf[0][1] > buf[1][1]):
            buf[1], buf[0] = buf[0], buf[1]
    if buf[2][0] == buf[3][0]:
        if (buf[2][1] < buf[3][1]):
            buf[2], buf[3] = buf[3], buf[2]
    if buf[0][1] < buf[1][1]:
        if buf[2][1] > buf[3][1]:
            k[1], k[2] = k[2], k[1]
            x, y = coordinateOfCrossPoint(k)
            return x, y
        else:
            k[1], k[3] = k[3], k[1]
            x, y = coordinateOfCrossPoint(k)
            return x, y
    else:
        if buf[2][1] > buf[3][1]:
            k[1], k[3] = k[3], k[1]
            x, y = coordinateOfCrossPoint(k)
            return x, y
        else:
            k[1], k[2] = k[2], k[1]
            x, y = coordinateOfCrossPoint(k)
            return x, y


def pass_coordinates(user_img):
    for i in range(13):
        for j in range(13):
            image = Image.open("./sweater/static/user_img.png")
            cutImg = image.crop((37 * j, 37 * i, 37 * j + 37, 37 * i + 37))
            cutImg.save("./sweater/static/cut_img.png")
            image = open("./sweater/static/cut_img.png", 'rb')
            img_read = image.read()
            img_encode_1 = base64.encodebytes(img_read)

            image = Image.open("./sweater/static/image/" + str(user_img) + ".png")
            image.thumbnail((37, 37))
            image.save("./sweater/static/pass_img.png")
            image = open("./sweater/static/pass_img.png", 'rb')
            img_read = image.read()
            img_encode_2 = base64.encodebytes(img_read)

            if (img_encode_1 == img_encode_2):
                mass = [(j * 37) + 18 + 1, (i * 37) + 18 + 1]
                return mass


def gen_zone(pass_img):
    rand_num = random.sample(range(401), 1)
    if rand_num[0] == 0 or rand_num[0] in pass_img:
        return gen_zone(pass_img)
    else:
        return rand_num[0]
