#coding:utf-8
import random
import os
from itertools import product
from PIL import Image, ImageDraw, ImageFont


def randRGB():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def cha_draw(cha, text_color, font, rotate, size_cha):
    im = Image.new(mode='RGBA', size=(size_cha*2, size_cha*2))
    drawer = ImageDraw.Draw(im) 
    drawer.text(xy=(0, 0), text=cha, fill=text_color, font=font) #text 内容，fill 颜色， font 字体（包括大小）
    if rotate:
        max_angle = 60 # to be tuned
        angle = random.randint(-max_angle, max_angle)
        im = im.rotate(angle, Image.BILINEAR, expand=1)
    im = im.crop(im.getbbox())
    return im


def captcha_draw(size_im, nb_cha, set_cha, fonts=None, overlap=0.0, 
        rd_bg_color=False, rd_text_color=False, rd_text_pos=False, rd_text_size=False,
        rotate=False, noise=None, dir_path=''):	
    rate_cha = 0.8
    width_im, height_im = size_im
    width_cha = int(width_im / max(nb_cha-overlap, 1)) # 字符區域宽度
    height_cha = height_im # 字符區域高度
    bg_color = 'white'
    text_color = 'black'
    derx = 0
    dery = 0

    if rd_text_size:
        rate_cha = random.uniform(rate_cha-0.1, rate_cha+0.1)
    size_cha = int(rate_cha*min(width_cha, height_cha)) # 字符大小
    
    if rd_bg_color:
        bg_color = randRGB()
    im = Image.new(mode='RGB', size=size_im, color=bg_color) # color 背景颜色，size 圖片大小

    drawer = ImageDraw.Draw(im)
    contents = []
    for i in range(nb_cha):
        if rd_text_color:
            text_color = randRGB()
        if rd_text_pos:
            derx = random.randint(0, max(width_cha-size_cha-5, 0))
            dery = random.randint(0, max(height_cha-size_cha-5, 0))

        # font = ImageFont.truetype("arial.ttf", size_cha)
        cha = random.choice(set_cha)
        font = ImageFont.truetype(fonts['eng'], size_cha)
        contents.append(cha)
        im_cha = cha_draw(cha, text_color, font, rotate, size_cha)
        im.paste(im_cha, (int(max(i-overlap, 0)*width_cha)+derx, dery), im_cha) # 字符左上角位置
        
    if 'point' in noise:
        nb_point = 30
        color_point = randRGB()
        for i in range(nb_point):
            x = random.randint(0, width_im)
            y = random.randint(0, height_im)
            drawer.point(xy=(x, y), fill=color_point)
    if 'line' in noise:
        nb_line = 10
        for i in range(nb_line):
            color_line = randRGB()
            sx = random.randint(0, width_im)
            sy = random.randint(0, height_im)
            ex = random.randint(0, width_im)
            ey = random.randint(0, height_im)
            drawer.line(xy=(sx, sy, ex, ey), fill=color_line)
    if 'circle' in noise:
        nb_circle = 5
        color_circle = randRGB()
        for i in range(nb_circle):
            sx = random.randint(0, width_im-50)
            sy = random.randint(0, height_im-20)
            ex = sx+random.randint(15, 25)
            ey = sy+random.randint(10, 15)
            drawer.arc((sx, sy, ex, ey), 0, 360, fill=color_circle)

    # 如果文件夾不存在，则創建對應的文件夹
    if os.path.exists(dir_path) == False:
        os.makedirs(dir_path)

    content_text = ''.join(contents)
    img_name = str(content_text) + '.jpg'
    img_path = dir_path + img_name
    im.save(img_path)
    

def captcha_generator():
    size_im = (200, 50) # width, height
    set_cha = "0123456789abcdefghijklmnopqrstuvwxyz" # 字符集
    nb_image = 1000 # 生成圖片數
    font_dir = 'fonts/english'
    fonts_path = []
    for dirpath, dirnames, filenames in os.walk(font_dir):
        for filename in filenames:
            filepath = dirpath + os.sep + filename
            fonts_path.append(filepath)
    for i in range(nb_image):
        for font_path in fonts_path:
            nb_cha = random.choice([4, 7])# 圖片字符個數
            captcha_draw(size_im=size_im, nb_cha=nb_cha, set_cha=set_cha, 
                overlap=0.3, 
                rd_text_pos=True, 
                rd_text_size=True,
                rd_text_color=True,
                rd_bg_color=True,
                noise=['line', 'point'],
                rotate=True,
                dir_path='img_data/tmp/',
                fonts={'eng': font_path})

if __name__ == "__main__":
    captcha_generator()
