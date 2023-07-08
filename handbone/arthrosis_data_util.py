import random

import cv2
import os
from PIL import Image

# 去雾
def opt_img(img_path):
    img = cv2.imread(img_path, 0)

    clahe = cv2.createCLAHE(tileGridSize=(3, 3), clipLimit=2.0)
    dst1 = clahe.apply(img)

    cv2.imwrite(img_path, dst1)

# 数据增样
def img_rotate(img_path, flag=5):
    img = Image.open(img_path)

    for i in range(flag):
        rota = random.randint(-45,45)
        dst = img.rotate(rota)
        file_name,_ = img_path.split(".")
        dst.save(file_name+ f"{i}.png")

path = "handbone/data/arthrosis"
print("图片预处理开始")
for folder in os.listdir(path):
    # folder 所有的类别名称
    path_folder = os.path.join(path, folder)
    for lev in os.listdir(path_folder):
        # lev 等级 1~10
        path_lev = os.path.join(path_folder, lev)
        for img_name in os.listdir(path_lev):
            path_img = os.path.join(path_lev, img_name)
            # print(path_img)
            # 去雾
            opt_img(path_img)
            # 增样
            img_rotate(path_img)
print("图片预处理结束")