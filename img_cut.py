from PIL import Image
img = Image.open('zzz.png')
# area = (5*38+10, 2, 5*38+10+38, 40)
# cropped_img = img.crop(area)
# cropped_img.show()
# cropped_img.save("1.png")
name=0
img.show()
for i in range(20):
    #img = Image.open("Emojis.png")
    for j in range(20):
        name+=1
        if j==0:
            g=0
        else:
            g=2
        area = (38*j, ((38*i)), 38*j+38, 38*i+38)
        cropped_img = img.crop(area)
        #cropped_img.show()
        cropped_img.save(str(name)+'.png')


