# Bone Age Detection System: Based on YOLOv5 and ResNet18

This project was implemented in the junior year's practice project. The main goal of the project is to develop a system that can determine the bone age based on the hand bone joints.

[中文版本](README.md)|[English version](README.en.md)

We first use the YOLOv5 model to train the semantic segmentation of hand X-ray images.

Note: `handbone/data` and `hnadbone/orignal_data` have been compressed and uploaded to release.

Project environment: macOS Sonoma 14.0 beta (23A5286g), device is MacBook Pro 14-inch, 2023 (Apple M2 MAX, 96GB version)

The YOLOv5 training phase is based on the yolov5 release 7.0 version, Python 3.11.0 and PyTorch 2.1.0.dev20230703. Due to the need for float64 in the training process, but Metal does not support float64, so CPU training was adopted. We used the official pre-trained weights of yolov5s.

yolov5 stage project structure: 
- Image data: `handbone/data/orignal_data/Image`
- Data labels: `handbone/data/orignal_data/Annotations`
- Label category: `handbone/data/ImageSets/label_list.txt`

Code files: 
- `handbone/data/orignal_data/ImageSets/get_list.py`: Divide the data set into train, trainval, and val, and store the corresponding filenames in `handbone/data/orignal_data/ImageSets`: `train.txt`, `trainval.txt`, `val.txt`
- `handbone/data/create_label.py`: Convert the data set in `handbone/data/original_data` into label files and image files suitable for target detection model training, and save the files in `handbone/data/images` and `handbone/data/labels`, and save the file paths corresponding to the three data sets in `handbone/data/train.txt` `handbone/data/trainval.txt` `handbone/data/val.txt`

Use the official training script of yolo for model training, and save the trained weights in `runs/train/exp/weights/best.pt`.

Use resnet18 to predict bone age:
(`handbone/data/arthrosis` has content related to bone age calculation)

The dataset has nine types of joint categories, namely「DIP, DIPFirst, MCP, MCPFirst, MIP, PIP, PIPFirst, Radius,

Ulna」, each category has 11 levels, scored according to gender, and infer the bone age according to the score.

- `handbone/arthrosis_data_util.py`: Enhance the image using Adaptive Histogram Equalization (CLAHE) and Random Rotation.
- `handbone/arthrosis_datalist.py`: Divide the image into data (9:1), and save the corresponding file path in each category folder
- `handbone/arthrosis_dataset.py`: The dataloader of the main training process, where the format of the input data is unified and certain data enhancement is performed
- `handbone/arthrosis_trainer.py`: The main program of model training. The main framework network is resnet18, but the input of the first layer is changed to (1, 244, 244), and the output is changed to the corresponding category, and each category's optimal model is saved in `./params`
- `handbone/common.py`: Provides some functions for calculating and processing hand bone age, including filtering hand bone joints, calculating bone age, generating reports, etc.

Due to the bus error in the loss function during pytorch training, we rewrote some code based on keras: `keras_datasets.py`, `keras_trainer.py`, `keras_common.py`

The other parts are also implemented based on keras:
- `handbone/hand_bone_detect.py`
- `handbone/hand_view.py`
- `handbone/main.py`
