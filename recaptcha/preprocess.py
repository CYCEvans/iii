import os
import json

import numpy as np
from PIL import Image

image_dirs = ["images/tmp/"]

pictures = []
ch_index = {}
labels = []

index = 0
image_no = 0
for img_dir in image_dirs:
    for pic in os.listdir(img_dir):
        # suffix_index = pic.find(".")
        # cur_pic_label = pic[0:suffix_index]
        pic_label = pic.split(".")[0]
        labels.append(pic_label)
        # lable's json ，隨機給值(看你的sample)
        for letter in pic_label:
            if letter not in ch_index:
                ch_index[letter] = index
                index += 1
        img = Image.open(img_dir + pic)
        # all convert to Height = 60, width=250, channel = 3
        img = img.resize((250, 60), Image.BILINEAR)
        # images to vectors
        img = np.array(img)
        # print(img)
        pictures.append(np.rollaxis(img, 2, 0))
        image_no += 1
        if image_no % 1000 == 0:
            print(image_no)

print("save pictures")

with open("pic", "wb") as inp:
    np.save(inp, pictures)

# 多給一個'<EOF>'值為list長度
ch_index['<EOF>'] = index

with open("ch_index", "w") as inp:
    json.dump(ch_index, inp)

# lable處理
# 為了方便訓練我們需要轉換成相同尺寸的。另外由於驗證碼長度不同，我們需要在label上多加一個符號來表示這個序列的結束。
# one_hot_encoding
max_caption_length = 7 + 1

id_labels = []
for label in labels:
    template = [ch_index['<EOF>']] * max_caption_length
    for (i, c) in enumerate(label):
        template[i] = ch_index[c]
    id_labels.append(template)

print("save labels")
with open("labels", "wb") as inp:
    np.save(inp, id_labels)
