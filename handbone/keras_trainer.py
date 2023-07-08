import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
# from tensorflow.keras.applications import ResNet50
from classification_models.keras import Classifiers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.layers import Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, LearningRateScheduler
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.models import Sequential
from keras_dataset import load_dataset  # Assuming keras_dataset.py is the file name of your previous script

# 九个分类模型
arthrosis = {'MCPFirst': ['MCPFirst', 11],
             'MCP': ['MCP', 10],
             'DIPFirst': ['DIPFirst', 11],
             'DIP': ['DIP', 11],
             'PIPFirst': ['PIPFirst', 12],
             'PIP': ['PIP', 12],
             'MIP': ['MIP', 12],
             'Radius': ['Radius', 14],
             'Ulna': ['Ulna', 12], }

def train(category):
    # category
    # 获取地址  MCP
    path = os.path.join('handbone/data/arthrosis',category)

    # 加载训练集和验证集
    train_dataset = load_dataset(mode="train", path=path)
    val_dataset = load_dataset(mode="val", path=path)

    train_dataset = train_dataset.batch(50).prefetch(tf.data.experimental.AUTOTUNE)
    val_dataset = val_dataset.batch(50).prefetch(tf.data.experimental.AUTOTUNE)

    # 加载模型
    ResNet18, preprocess_input = Classifiers.get('resnet18')
    base_model = ResNet18((224, 224, 1), weights=None, include_top=False)
    
    model = Sequential()
    model.add(base_model)
    model.add(Flatten())
    model.add(Dense(arthrosis[category][1]))

    # 损失函数
    loss_func = SparseCategoricalCrossentropy(from_logits=True)
    # 优化器
    opt = Adam()

    model.compile(optimizer=opt, loss=loss_func, metrics=['accuracy'])
    best_acc = 0
    for epoch in range(20):
        model.fit(train_dataset, validation_data=val_dataset, epochs=1)

        loss, acc = model.evaluate(val_dataset)
        if acc > best_acc:
            best_acc = acc
            if not os.path.exists("params"):
                os.mkdir("params")
            model.save_weights(f"params/{category}")  # Saving weights in Keras format

if __name__ == '__main__':
    for item in arthrosis:
        print(f"{item}模型开始训练")
        train(item)
        print(f"{item}模型结束训练")
