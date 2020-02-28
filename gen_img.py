import glob,random
from PIL import Image

images = glob.glob("./image/*.png")
newimg = Image.new('RGB', (760, 760))
random_mas = random.sample(range(400), 400)
#print(random_mas)
# for image in images:
#     img = Image.open(image)
#     newimg.paste(img,(0,0))
#     #img.show()
#     # img1.save("D:\sandbox\IMG\\"+image)
#     newimg.show()
g=0
for i in range(20):
    for j in range(20):
        img = Image.open(images[random_mas[g]])
        g+=1
        newimg.paste(img, (i*38, j*38))
newimg.show()
newimg.save("./zzz.png")