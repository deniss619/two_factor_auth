from PIL import Image
import base64
import random
import math

from sweater import db, app


def make_mass_for_img(user, method=None):
    # генерирует массив из которого будет создано изображение
    img_size = 13
    random_mas = random.sample(range(400), 400)
    random_mas[random_mas.index(0)] = 400
    pass_img = list(map(int, user.pass_img.replace('{', '').replace('}', '').split(',')))
    if method == 1:
        img_amount = 4
    elif method == 3:
        img_amount = 1
    else:
        img_amount = 3
    for i in list(map(int, user.pass_img.replace('{', '').replace('}', '').split(','))):
        del random_mas[random_mas.index(i)]
    random_mas = random.sample(random_mas, img_size ** 2)
    password_images = random.sample(pass_img, len(pass_img))
    zone = list(map(int, user.zone.replace('{', '').replace('}', '').split(',')))
    probability = list(map(int, user.probability.replace('{', '').replace('}', '').split(',')))
    for i in range(len(zone)):
        # в массив добавляются числа с повышенной вероятностью выпадения
        check = random.choices([0, 1], weights=[probability[i], 10])
        if check[0] == 0 and zone[i] not in random_mas:
            random_mas[random.randint(0, img_size ** 2 - 1)] = zone[i]
    pass_img_coordinates = []
    i = 0
    while i < img_amount:
        position = random.randint(0, img_size ** 2 - 1)
        if position not in pass_img_coordinates:
            pass_img_coordinates.append(position)
            random_mas[position] = password_images[i]
            i += 1
    return random_mas


def generate_img(user, method=None):
    img_size = 13
    newimg = Image.new('RGB', (img_size * 37, img_size * 37))
    random_mas = make_mass_for_img(user, method)
    password_img_mass = list(map(int, user.pass_img.split(',')))
    coordinates = []
    g = 0
    for i in range(img_size):
        for j in range(img_size):
            img = Image.open('./sweater/static/image/' + str(random_mas[g]) + '.png')
            newimg.paste(img, (i * 37, j * 37))
            for z in password_img_mass:
                if random_mas[g] == z:
                    if method == 3:
                        coordinates = img_size * j + i
                    else:
                        coordinates.append((i * 37) + 18 + 1)
                        coordinates.append((j * 37) + 18 + 1)
            g += 1
    user.coordinates = coordinates
    db.session.add(user)
    db.session.commit()
    if method != 1:
        return triangle_img(user, newimg)
    else:
        return diagonal_img(user, newimg)


def triangle_img(user, newimg):
    coordinates_mass = list(map(int, user.coordinates.replace('{', '').replace('}', '').split(',')))
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


def diagonal_img(user, new_img):
    coordinates_mass = list(map(int, user.coordinates.replace('{', '').replace('}', '').split(',')))
    k = list(map(lambda i: [coordinates_mass[i + i], coordinates_mass[i + i + 1]], range(4)))
    for i in range(4):
        point1 = (k[2][0] - k[0][0]) * (k[1][1] - k[0][1]) - (k[2][1] - k[0][1]) - (k[1][0] - k[0][0])
        point2 = (k[3][0] - k[0][0]) * (k[1][1] - k[0][1]) - (k[3][1] - k[0][1]) - (k[1][0] - k[0][0])
        if (point1 <= 0 and point2 <= 0) or (point1 >= 0 and point2 >= 0):
            k = k[1:] + [k[0]]
        else:
            return generate_img(user, 1)
    new_img.save("./sweater/static/user_img.png")
    image = open("./sweater/static/user_img.png", 'rb')
    img_read = image.read()
    img_encode = base64.encodebytes(img_read)
    return img_encode


def check_frame(mass, user, fast_mod):
    if fast_mod == 'true':
        for i in list(map(int, user.pass_img.split(','))):
            if i in mass:
                pos1 = mass.index(i)
    else:
        pos1 = pass_coordinates(list(map(int, user.pass_img.replace('{', '').replace('}', '').split(','))))
    return math.ceil(pos1 % 13) == math.ceil(int(user.coordinates) % 13)


def check_triangle(coordinates, user, fast_mod):
    if fast_mod == 'true':
        coordinates_mass = list(map(int, user.coordinates.replace('{', '').replace('}', '').split(',')))
        pass_img_1 = [coordinates_mass[0], coordinates_mass[1]]
        pass_img_2 = [coordinates_mass[2], coordinates_mass[3]]
        pass_img_3 = [coordinates_mass[4], coordinates_mass[5]]
    else:
        user_img = list(map(int, user.pass_img.replace('{', '').replace('}', '').split(',')))
        pass_img_1 = pass_coordinates(user_img[0])
        pass_img_2 = pass_coordinates(user_img[1])
        pass_img_3 = pass_coordinates(user_img[2])
    a = (pass_img_1[0] - coordinates[0]) * (pass_img_2[1] - pass_img_1[1]) - (pass_img_2[0] - pass_img_1[0]) * (
            pass_img_1[1] - coordinates[1])
    b = (pass_img_2[0] - coordinates[0]) * (pass_img_3[1] - pass_img_2[1]) - (pass_img_3[0] - pass_img_2[0]) * (
            pass_img_2[1] - coordinates[1])
    c = (pass_img_3[0] - coordinates[0]) * (pass_img_1[1] - pass_img_3[1]) - (pass_img_1[0] - pass_img_3[0]) * (
            pass_img_3[1] - coordinates[1])
    return (a >= 0 and b >= 0 and c >= 0) or (a <= 0 and b <= 0 and c <= 0)


def check_diagonal(coordinates, user, fast_mod):
    k = []
    if fast_mod == 'true':
        coordinates_mass = list(map(int, user.coordinates.replace('{', '').replace('}', '').split(',')))
        for i in range(4):
            k.append([coordinates_mass[i + i], coordinates_mass[i + i + 1]])
    else:
        user_img = list(map(int, user.pass_img.replace('{', '').replace('}', '').split(',')))
        for i in range(4):
            k.append(pass_coordinates(user_img[i]))
    x, y = check_cross_point(k)
    print((coordinates[0] - x) ** 2 + (coordinates[1] - y) ** 2 <= 400)
    return (coordinates[0] - x) ** 2 + (coordinates[1] - y) ** 2 <= 400


def coordinate_of_cross_point(k):
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


def check_cross_point(k):
    mass = [k[0][0], k[1][0], k[2][0], k[3][0]]
    buf = []
    for i in range(4):
        minimum = min(mass)
        buf.append(k[mass.index(minimum)])
        mass[mass.index(minimum)] = max(mass) + 1
    if buf[0][0] == buf[1][0]:
        if buf[0][1] > buf[1][1]:
            buf[1], buf[0] = buf[0], buf[1]
    if buf[2][0] == buf[3][0]:
        if buf[2][1] < buf[3][1]:
            buf[2], buf[3] = buf[3], buf[2]
    if buf[0][1] < buf[1][1]:
        if buf[2][1] > buf[3][1]:
            k[1], k[2] = k[2], k[1]
            x, y = coordinate_of_cross_point(k)
            return x, y
        else:
            k[1], k[3] = k[3], k[1]
            x, y = coordinate_of_cross_point(k)
            return x, y
    else:
        if buf[2][1] > buf[3][1]:
            k[1], k[3] = k[3], k[1]
            x, y = coordinate_of_cross_point(k)
            return x, y
        else:
            k[1], k[2] = k[2], k[1]
            x, y = coordinate_of_cross_point(k)
            return x, y


def pass_coordinates(user_img):
    for i in range(13):
        for j in range(13):
            image = Image.open("./sweater/static/user_img.png")
            cut_img = image.crop((37 * j, 37 * i, 37 * j + 37, 37 * i + 37))
            cut_img.save("./sweater/static/cut_img.png")
            image = open("./sweater/static/cut_img.png", 'rb')
            img_read = image.read()
            img_encode_1 = base64.encodebytes(img_read)

            image = Image.open("./sweater/static/image/" + str(user_img) + ".png")
            image.thumbnail((37, 37))
            image.save("./sweater/static/pass_img.png")
            image = open("./sweater/static/pass_img.png", 'rb')
            img_read = image.read()
            img_encode_2 = base64.encodebytes(img_read)

            if img_encode_1 == img_encode_2:
                mass = [(j * 37) + 18 + 1, (i * 37) + 18 + 1]
                return mass


def gen_zone(pass_img):
    i = 0
    zone = []
    while i < 50:
        rand_num = random.randint(1, 401)
        if rand_num not in pass_img and rand_num not in zone:
            zone.append(rand_num)
            i += 1
    return zone
