from captcha.image import ImageCaptcha
from random import sample
import os

image = ImageCaptcha(fonts=[ "font/Xenotron.ttf", "font/Xenophobia.ttf"])
characters = list("abcdefghijklmnopqrstuvwxyz1234567890")


def generate_data(digits_num, output, total):
    if not os.path.exists(output):
        os.makedirs(output)
    num = 0
    while num < total:
        # 隨機挑出N個數字, list
        cap = sample(characters, digits_num)
        cap = ''.join(cap)
        _ = image.generate(cap)	
        image.write(cap, output+cap+".png")
        num += 1


def main():
    generate_data(4, "images/tmp/", 1700)
    generate_data(5, "images/tmp/", 1700)
    generate_data(6, "images/tmp/", 1700)
    generate_data(7, "images/tmp/", 1700)

if __name__ == "__main__":
    main()
