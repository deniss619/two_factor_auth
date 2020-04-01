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
#img_data=None
# with open('./sweater/static/image\\' + str(2) + '.png','rb') as fh:
#     img_data=fh.read()
#     print(img_data)
# with BytesIO(img_data) as img_buf:
#     with Image.open(img_buf) as img:
#         img.show()
newimg = Image.new('RGB', (481, 481))
random_mas = random.sample(range(400), 400)
random_mas[random_mas.index(0)] = 400
strPassImg = '4,5,6'
mass = []
g=0
buf=''
for i in range(len(strPassImg)):
    print(strPassImg[i])
    if (strPassImg[i] != ','):
        buf+=str(strPassImg[i])
    else:
        mass.append(int(buf))
        buf = ''
mass.append(int(buf))
print(mass)
for i in range(len(mass)):
    if (random_mas.index(mass[i]) > 168):
        random_mas[random.sample(range(168), 1)[0]] = mass[i]
g = 1
for i in range(13):
    for j in range(13):
        img = Image.open('./sweater/static/37/' + str(random_mas[g]) + '.png')
        g += 1
        newimg.paste(img, (i * 37, j * 37))
newimg.show()
newimg.save("./sweater/static/image.png")

# for i in range(400):
#     image=Image.open('./sweater/static/image/' + str(i+1) + '.png')
#     image.thumbnail((37,37))
#     image.save("./sweater/static/37/"+str(i+1)+".png")