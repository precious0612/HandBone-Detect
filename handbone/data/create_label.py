import xml.etree.ElementTree as ET
import os
from os import getcwd
import shutil

datasets_path = "handbone/data/orignal"  # 数据集路径
sets = ['train', 'trainval', 'val']
classes = ['Radius', 'Ulna', 'MCPFirst', 'MCP','ProximalPhalanx','MiddlePhalanx','DistalPhalanx']  #


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def convert_annotation(image_id):
    in_file = open(datasets_path + '/Annotations/%s.xml' % image_id)
    out_file = open(datasets_path + 'labels/%s.txt' % image_id, 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        # 0,1 表示实例是否难以识别，0表示不难1表示困难
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


for image_set in sets:
    if not os.path.exists('labels/'):
        os.makedirs('labels/')
    image_ids = open(datasets_path + '/ImageSets/Main/%s.txt' % image_set).read().strip().split()
    list_file = open('%s.txt' % image_set, 'w')
    for image_id in image_ids:
        list_file.write('/Users/precious/yolov5/handbone/data/images/%s.png\n' % image_id)
        convert_annotation(image_id)
    list_file.close()

path = getcwd()
if not os.path.exists(path + "/images"):
    os.mkdir(path + "/images")
if os.path.exists(path + "/images"):
    # 递归删除文件夹以及里面的文件
    shutil.rmtree(path + "/images")
shutil.copytree(datasets_path + "/JPEGImages", path + "/images")
print("done")