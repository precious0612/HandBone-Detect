import cv2
import os
import keras_common
from PIL import Image
import tensorflow as tf

def detect(model, sex, path_img, small_model):
    results = model(path_img)  # Assuming your model is a YOLO-based model
    original_box = results.xyxy[0]
    print(original_box)

    if original_box.shape[0] != 21:
        return "侦测到的关节数量不正确，请重新放一张x光片！"

    box = keras_common.bone_filter(original_box)
    print(box)

    res = {}
    score_num = 0
    img = cv2.imread(path_img)
    for i, name in enumerate(keras_common.arthrosis_new):
        x1 = int(original_box[i][0])
        y1 = int(original_box[i][1])
        x2 = int(original_box[i][2])
        y2 = int(original_box[i][3])

        print(x1, y1, x2, y2)
        img_roi = img[y1:y2, x1:x2]
        if not os.path.exists("cut_img"):
            os.mkdir("cut_img")
        cv2.imwrite(f'cut_img/{name}.png', img_roi)
        
        # 根据name找到模型名称
        model_name = keras_common.arthrosis[name][0]

        # 找对应的模型
        model = small_model[model_name]
        # 把图片传给模型
        img2 = Image.open(f'cut_img/{name}.png')
        # 做成正方形
        img2 = keras_common.trans_square(img2)
        # 转换成灰度图
        img2 = img2.convert("L")
        # 放大图片、归一化、NCHW
        img2 = keras_common.load_and_preprocess_image(img2)

        # img2= img2.unsqueeze(dim=0)
        print(img2.shape)

        leval = model(img2)
        index = int(tf.argmax(leval, axis=1).numpy().item())

        # 获取到得分
        score = keras_common.SCORE[sex][name][index]
        score_num += score

        # 保存 骨节名称 和 对应的等级数and得分
        res[name] = [index+1, score]
    # 根据总得分和性别，计算年龄
    age = keras_common.calcBoneAge(score_num, sex)
    return keras_common.export(res,score_num,age)
