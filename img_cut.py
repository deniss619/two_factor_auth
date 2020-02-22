from PIL import Image
img = Image.open('Emojis.png')
# area = (5*38+10, 2, 5*38+10+38, 40)
# cropped_img = img.crop(area)
# cropped_img.show()
# cropped_img.save("1.png")
name=0
for i in range(24):
    #img = Image.open("Emojis.png")
    for j in range(30):
        name+=1
        if j==0:
            g=0
        else:
            g=2
        area = (38*j+g*j, ((40*i)+2), 38*j+38+g*j, 40*i+40)
        cropped_img = img.crop(area)
        #cropped_img.show()
        cropped_img.save(str(name)+'.png')


