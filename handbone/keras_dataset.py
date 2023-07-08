import tensorflow as tf
from PIL import Image
import numpy as np
import os

# 图片的等比缩放（转换成正方形）
def trans_square(image):
    img = image.convert('RGB')
    img = np.array(img, dtype=np.uint8)  # 图片转换成numpy
    img_h, img_w, img_c = img.shape
    if img_h != img_w:
        long_side = max(img_w, img_h)
        short_side = min(img_w, img_h)
        loc = abs(img_w - img_h) // 2
        img = img.transpose((1, 0, 2)) if img_w < img_h else img  # 如果高是长边则换轴，最后再换回来
        background = np.zeros((long_side, long_side, img_c), dtype=np.uint8)  # 创建正方形背景
        background[loc:loc + short_side] = img[...]  # 数据填充在中间位置
        img = background.transpose((1, 0, 2)) if img_w < img_h else background
    return Image.fromarray(img, 'RGB')

def process_path(file_path, label):
    # Convert the file path tensor to string
    file_path = file_path.numpy().decode("utf-8")
    img = Image.open(file_path)
    img = trans_square(img)
    img = img.resize((224, 224))  # Resize image
    img = img.convert("L")  # Convert to grayscale
    img = np.array(img) / 255.0  # Normalize
    img = np.expand_dims(img, axis=-1)  # Add channel dimension
    img = tf.convert_to_tensor(img, dtype=tf.float32)  # Convert to TensorFlow Tensor
    img.set_shape([224, 224, 1])  # Explicitly set shape
    label = tf.convert_to_tensor(label, dtype=tf.int32)
    label.set_shape([])  # Explicitly set shape for label
    return img, label


def load_dataset(mode, path):
    if mode == 'train':
        file_path = os.path.join(path, "train.txt")
    elif mode == 'val':
        file_path = os.path.join(path, "val.txt")

    image_paths = []
    labels = []

    with open(file_path, 'r') as f:
        for line in f:
            img_path, level = line.split()
            image_paths.append(img_path)
            labels.append(int(level))

    dataset = tf.data.Dataset.from_tensor_slices((image_paths, labels))
    
    dataset = dataset.map(
        lambda item1, item2: tf.py_function(
            func=process_path, 
            inp=[item1, item2], 
            Tout=(tf.float32, tf.int32)), 
        num_parallel_calls=tf.data.experimental.AUTOTUNE)
    
    def set_shapes(img, label):
        img.set_shape([224, 224, 1])  # Explicitly set shape
        label.set_shape([])  # Explicitly set shape for label
        return img, label
    
    dataset = dataset.map(set_shapes)  # Set the shapes of the tensors
    
    return dataset



if __name__ == '__main__':
    train_dataset = load_dataset(mode="train", path="handbone/data/arthrosis/MCP")
    train_dataset = train_dataset.batch(10).prefetch(tf.data.experimental.AUTOTUNE)

    for x, y in train_dataset.take(1):
        print(x.shape)
        print(y.shape)
