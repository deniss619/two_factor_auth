import glob, random
from PIL import Image
import numpy as np
from io import BytesIO
import base64


# images = glob.glob("./sweater/static/image/*.png")
# image = open('./sweater/static/image\\' + str(2) + '.png')
# print(image)
# b=image.encode("UTF-8")
# e=base64.b64encode(b)
# s1=e.decode("UTF-8")
# print(s1)
# img_data=None
# with open('./sweater/static/image\\' + str(2) + '.png','rb') as fh:
#     img_data=fh.read()
#     print(img_data)
# with BytesIO(img_data) as img_buf:
#     with Image.open(img_buf) as img:
#         img.show()
# newimg = Image.new('RGB', (481, 481))
# random_mas = random.sample(range(400), 400)
# random_mas[random_mas.index(0)] = 400
# strPassImg = '4,5,6'
# mass = []
# g=0
# buf=''
# random_mas=[236, 380, 382, 216, 111, 134, 123, 117, 356, 371, 158, 21, 195, 392, 148, 287, 333, 151, 82, 174, 318, 57, 43, 203, 112, 177, 32, 248, 100, 242, 189, 55, 78, 319, 11, 283, 314, 362, 37, 274, 336, 265, 327, 383, 239, 133, 186, 290, 1, 143, 7, 351, 352, 340, 280, 374, 365, 114, 217, 312, 232, 165, 332, 297, 172, 63, 24, 385, 368, 185, 393, 226, 150, 118, 9, 34, 13, 162, 212, 272, 215, 230, 166, 306, 22, 270, 180, 102, 400, 29, 47, 119, 35, 77, 348, 154, 129, 366, 320, 244, 72, 369, 233, 334, 31, 6, 53, 337, 207, 298, 121, 12, 145, 301, 223, 64, 273, 139, 325, 52, 122, 308, 240, 67, 194, 69, 124, 61, 229, 92, 74, 347, 54, 5, 93, 15, 210, 130, 161, 170, 345, 329, 324, 292, 94, 188, 105, 18, 191, 209, 196, 257, 28, 85, 311, 228, 335, 354, 398, 59, 286, 60, 276, 342, 178, 263, 322, 62, 81, 147, 338, 361, 310, 261, 321, 225, 267, 26, 155, 113, 89, 296, 182, 258, 222, 70, 328, 284, 127, 331, 256, 84, 285, 370, 202, 339, 243, 213, 75, 269, 275, 38, 291, 344, 152, 51, 375, 278, 364, 277, 264, 255, 58, 353, 2, 198, 388, 14, 106, 97, 295, 175, 169, 309, 208, 397, 304, 357, 303, 206, 330, 8, 390, 394, 316, 80, 103, 176, 16, 140, 87, 300, 214, 197, 48, 116, 204, 108, 20, 136, 65, 305, 363, 50, 313, 25, 247, 33, 131, 153, 99, 359, 101, 250, 219, 132, 36, 326, 159, 40, 377, 181, 396, 220, 282, 49, 128, 10, 98, 350, 164, 384, 224, 79, 3, 205, 68, 156, 126, 399, 44, 171, 343, 341, 355, 251, 349, 30, 379, 288, 376, 358, 259, 96, 241, 4, 17, 90, 268, 211, 386, 235, 27, 200, 149, 86, 71, 218, 107, 187, 125, 307, 234, 378, 41, 167, 227, 299, 23, 160, 157, 146, 294, 252, 45, 95, 19, 389, 120, 293, 184, 238, 83, 246, 289, 315, 260, 163, 302, 144, 110, 395, 201, 317, 179, 221, 91, 373, 262, 135, 281, 346, 381, 387, 245, 367, 138, 391, 39, 42, 254, 56, 193, 360, 237, 109, 279, 192, 183, 88, 73, 168, 190, 66, 76, 141, 142, 372, 137, 271, 104, 323, 249, 253, 231, 115, 173, 266, 199, 46]
# a=[]
# b=[]
# for i in range(13):
#     a=[]
#     for j in range(13):
#         a.append(random_mas[g])
#         g+=1
#     b.append(a)
# print(b)
# for i in range(len(strPassImg)):
#     print(strPassImg[i])
#     if (strPassImg[i] != ','):
#         buf+=str(strPassImg[i])
#     else:
#         mass.append(int(buf))
#         buf = ''
# mass.append(int(buf))
# print(random_mas)
# for i in range(len(mass)):
#     if (random_mas.index(mass[i]) > 168):
#         random_mas[random.sample(range(168), 1)[0]] = mass[i]
# g = 1
# for i in range(13):
#     for j in range(13):
#         img = Image.open('./sweater/static/37/' + str(random_mas[g]) + '.png')
#         g += 1
#         newimg.paste(img, (i * 37, j * 37))
# newimg.show()
# newimg.save("./sweater/111.png")
# for i in range(13):
#     for j in range(13):
#         img = Image.open('./sweater/static/image/' + str(random_mas[g]) + '.png')
#         g += 1
#         newimg.paste(img, (i * 37, j * 37))
# newimg.show()
# newimg.save("./sweater/111.png")

# for i in range(400):
#     image=Image.open('./sweater/static/image/' + str(i+1) + '.png')
#     image.thumbnail((37,37))
#     image.save("./sweater/static/37/"+str(i+1)+".png")


from itertools import combinations
#
# a = list(combinations(b, 3))
#
#
# print(0.17**10*100)

def make_mass(a):
    coordinate = a
    coordinateMass = []
    buf = ''
    for i in range(len(coordinate)):
        if (coordinate[i] != ' '):
            buf += str(coordinate[i])
        else:
            coordinateMass.append(int(buf))
            buf = ''
    coordinateMass.append(int(buf))
    return coordinateMass

from itertools import combinations
b=[]
for i in range(169):
    b.append(str(i+1))

mass = []
for i in combinations(b, 3):
    mass.append(make_mass(' '.join(i)))


def coordinates(num):
    g = 1
    for i in range(13):
        for j in range(13):
            if num == g:
                return i, j
            g += 1


counter = 0
s=0
for z in range(len(mass)):
    pass_img_1 = coordinates(mass[z][0])
    pass_img_2 = coordinates(mass[z][1])
    pass_img_3 = coordinates(mass[z][2])
    S = 0.5 * (abs((pass_img_2[0] - pass_img_1[0]) * (pass_img_3[1] - pass_img_1[1]) -
                   (pass_img_3[0] - pass_img_1[0]) * (pass_img_2[1] - pass_img_1[1])))
    if (S > 1.2 and S < 7.2):
        s += S / 24
        counter += 1
print(1 / counter *s)



# mass = []
# for i in combinations(b, 3):
#     mass.append(make_mass(' '.join(i)))
# print(mass)






# yes = 0
# no = 0
# massive = []
# buf = []
# for i in range(400):
#     massive.append(i + 1)
#     buf.append(0)
# pass_img = [1, 2, 3, 4, 5]
#
# checker = 0
# a0 = 0
# b0 = 0
#
#
# def gen_zone(random_mas):
#     rand_num = random.sample(range(401), 1)
#     if rand_num[0] == 0 or rand_num[0] in pass_img:
#         return gen_zone(random_mas)
#     else:
#         return rand_num[0]
#
#
# random_mas = random.sample(range(400), 400)
# random_mas[random_mas.index(0)] = 400
# zone = []
# probability = []
# for i in range(50):
#     probability.append(random.randint(22, 30))
#     zone.append(gen_zone(random_mas))
# print(zone, probability)
#
#
#
# for i in range(100):
#     random_mas = random.sample(range(400), 400)
#     random_mas[random_mas.index(0)] = 400
#     mass = pass_img
#     mass = random.sample(mass, 3)
#     fake_img = random.choices([0, 1], weights=[1, 10])
#
#     for i in range(len(zone)):
#         check = random.choices([0, 1], weights=[probability[i], 10])
#         if (check[0] == 0 and random_mas.index(zone[i]) > 168):
#             position1 = random.sample(range(168), 1)[0]
#             position2 = random_mas.index(zone[i])
#             random_mas[position1], random_mas[position2] = random_mas[position2], random_mas[position1]
#
#
#     if fake_img[0] == 0:
#         lose_img = random.sample(range(len(mass)), len(mass))
#         for i in range(len(mass) - 1):
#             if (random_mas.index(mass[lose_img[0]]) > 168):
#                 position1 = random.sample(range(168), 1)[0]
#                 position2 = random_mas.index(mass[lose_img[i]])
#                 random_mas[position1], random_mas[position2] = random_mas[position2], random_mas[position1]
#
#                 del lose_img[0]
#     else:
#         # print(mass)
#         # print(random_mas.index(mass[0]), random_mas.index(mass[1]), random_mas.index(mass[2]))
#         for i in range(len(mass)):
#             if (random_mas.index(mass[i]) > 168):
#                 position1 = random.sample(range(168), 1)[0]
#                 for z in range(len(mass)):
#                     if position1==random_mas.index(mass[z]):
#                         position1 = random.sample(range(168), 1)[0]
#                         z=0
#                 position2 = random_mas.index(mass[i])
#                 random_mas[position1], random_mas[position2] = random_mas[position2], random_mas[position1]
#     for j in range(168):
#         buf[massive.index(random_mas[j])]+=1
#
#
#
#
# print(buf)
# max_mas = []
# for i in range(len(buf)):
#     max_mas.append(buf.index(max(buf)) + 1)
#     buf[buf.index(max(buf))] = 0
# print(max_mas)
# print(96**5)

