# 数据集拆分 训练集：验证集 = 9：1
import os
import random

path = 'handbone/data/arthrosis'


for folder in os.listdir(path):
    # folder 分类名称

    # 图片地址 + 等级数
    train_list = []
    val_list = []

    # 拆分比例
    train_ratio = 0.9

    path_folder = os.path.join(path,folder)

    for level in os.listdir(path_folder):
        # level 等级数
        path_level = os.path.join(path_folder, level)
        print(path_level)

        # 判断是否是文件
        if os.path.isfile(path_level):
            continue

        # 等级数下所有的图片
        level_list = os.listdir(path_level)
        # 等级数下所有的图片数量
        level_num = len(level_list)
        # 随机打乱
        random.shuffle(level_list)
        # 训练集数量
        train_num = level_num * train_ratio
        for index, img in enumerate(level_list):
            if index < train_num:
                # 保存到训练集
                train_list.append(os.path.join(path_level,img) + " " + str(int(level)-1) +"\n")
            else:
                # 保存到验证集
                val_list.append(os.path.join(path_level, img) + " " + str(int(level) - 1) + "\n")

    random.shuffle(train_list)
    random.shuffle(val_list)
    # 保存文件 train.txt  val.txt
    path_trian_txt = os.path.join(path_folder,"train.txt")
    if os.path.exists(path_trian_txt):
        os.remove(path_trian_txt)
    with open(path_trian_txt,'w') as f:
        f.writelines(train_list)

    path_val_txt = os.path.join(path_folder, "val.txt")
    if os.path.exists(path_val_txt):
        os.remove(path_val_txt)
    with open(path_val_txt, 'w') as f:
        f.writelines(val_list)