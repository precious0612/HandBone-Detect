# 启动界面
import sys

import torch.hub
from PySide6.QtWidgets import QMainWindow,QApplication,QFileDialog
from hand_view import Ui_MainWindow
from PySide6.QtGui import QPixmap
import hand_bone_detect
import keras_common

from classification_models.keras import Classifiers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bind_slots()
        # 加载yolov5模型（本地训练好的）
        self.mode = torch.hub.load('./','custom',path='./runs/train/exp/weights/best.pt',source='local')
        self.mode.eval()
        self.mode.conf = 0.5  # 置信度
        print("yolov5模型加载完成")

        # Load other keras models
        self.parm = {}
        for key, value in keras_common.arthrosis.items():
            if value[0] in self.parm:
                continue

            ResNet18, preprocess_input = Classifiers.get('resnet18')
            base_model = ResNet18((224, 224, 1), weights=None, include_top=False)

            model = Sequential()
            model.add(base_model)
            model.add(Flatten())
            model.add(Dense(value[1]))

            # Load weights
            model.load_weights(f"params/{value[0]}")

            self.parm[value[0]] = model
        print("九个模型加载完成")

    # 信号   槽（函数）

    def btn_open_img(self):
        print("点击按钮")
        file_path = QFileDialog.getOpenFileNames(self, dir="handbone/data/images", filter="*.png;*.jpeg;*.jpg")
        if file_path[0]:
            # 选择图片
            print(file_path[0][0])
            # 回显手骨x光片
            self.label_2.setPixmap(QPixmap(file_path[0][0]))

            # 获取性别
            sex = 'boy' if self.radioButton.isChecked() else 'girl'
            print(sex)

            # 侦测
            result = hand_bone_detect.detect(self.mode, sex , file_path[0][0], self.parm)

            # 显示检测结果
            self.label_3.setText(result)

    # 绑定槽
    def bind_slots(self):
        self.pushButton.clicked.connect(self.btn_open_img)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()