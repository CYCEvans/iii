import os
import json

import numpy as np
from PIL import Image

image_dirs = ["images/test/"]

pictures = []
# ch_index = {}
labels = []

index = 0
image_no = 0
for img_dir in image_dirs:
    for pic in os.listdir(img_dir):
        # suffix_index = pic.find(".")
        # cur_pic_label = pic[0:suffix_index]
        pic_label = pic.split(".")[0]
        labels.append(pic_label)
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

with open("pic_test", "wb") as inp:
    np.save(inp, pictures)

with open("ch_index", "r") as inp:
    ch_index = json.load(inp)

max_caption_length = 7 + 1
id_labels = []
for label in labels:
    template = [ch_index['<EOF>']] * max_caption_length
    for (i, c) in enumerate(label):
        template[i] = ch_index[c]
    id_labels.append(template)

print("save labels")
with open("labels_test", "wb") as inp:
    np.save(inp, id_labels)