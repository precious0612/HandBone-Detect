# 骨龄检测系统：基于YOLOv5与ResNet18

这个项目是在大三下学期的实训项目中实现的。项目的主要目标是开发一个能够根据手骨关节判断骨龄的系统。

[中文版本](#README)|[English version](#README_EN)

我们首先使用YOLOv5模型来训练手部X光图像进行语义分割。

注意：`handbone/data`和`hnadbone/orignal_data`已经压缩并上传到了release。

项目环境：macOS Sonoma 14.0 beta（23A5286g），设备为MacBook Pro 14-inch, 2023 （Apple M2 MAX，96GB版本）

YOLOv5训练阶段基于yolov5 release 7.0版本，Python 3.11.0和PyTorch 2.1.0.dev20230703，由于训练过程中需要float64，但Metal不支持float64，所以采用了CPU训练。我们使用了yolov5s的官方预训练权重。

yolov5阶段项目结构： 
- 图像数据：`handbone/data/orignal_data/Image`
- 数据标签：`handbone/data/orignal_data/Annotations`
- 标签类别：`handbone/data/ImageSets/label_list.txt`

代码文件： 
- `handbone/data/orignal_data/ImageSets/get_list.py`： 将数据集分为train、trainval以及val，并将对应文件名字存储于`handbone/data/orignal_data/ImageSets`中：`train.txt`，`trainval.txt`，`val.txt`
- `handbone/data/create_label.py`：将`handbone/data/original_data`中的数据集转换为适用于目标检测模型训练的标签文件和图像文件，并将文件保存在`handbone/data/images`和`handbone/data/labels`，并将三组数据集对应的文件路径保存在`handbone/data/train.txt` `handbone/data/trainval.txt` `handbone/data/val.txt`

使用yolo官方训练脚本进行模型的训练，训练好的权重保存在`runs/train/exp/weights/best.pt`。

使用resnet18进行骨龄预测：
(`handbone/data/arthrosis`中有关于骨龄计算相关内容)

数据集中有九种关节类别分别为「DIP, DIPFirst, MCP, MCPFirst, MIP, PIP, PIPFirst, Radius, Ulna」，每种类别有11个等级，根据性别来打分，根据分数推断骨龄。

- `handbone/arthrosis_data_util.py`：使用自适应直方图均衡化(CLAHE)与随机旋转对图像进行增强处理。
- `handbone/arthrosis_datalist.py`：将图像进行数据划分（9:1），同时将对应文件路径保存在每种类别的文件夹中
- `handbone/arthrosis_dataset.py`：主要训练过程的dataloader，其中统一的输入数据的格式，并进行一定的数据增强
- `handbone/arthrosis_trainer.py`：模型训练的主程序，主要框架网络是resnet18，但将第一层的输入改为（1，244，244），输出改为对应类别数，并将每类最优模型保存在`./params`中
- `handbone/common.py`：提供了一些计算和处理手骨骨龄相关的功能，包括筛选手骨骨节、计算骨龄、生成报告等功能

由于pytorch在训练过程中的loss函数出现了总线错误，我们将部分代码重新基于keras编写：`keras_datasets.py`, `keras_trainer.py`, `keras_common.py`

其他部分也是基于keras实现：
- `handbone/hand_bone_detect.py`
- `handbone/hand_view.py`
- `handbone/main.py`
