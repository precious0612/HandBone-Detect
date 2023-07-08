import os
import random
random.seed(2020)
train_precent=0.8
xml="handbone/orignal_data/Annotations"
save="handbone/orignal_data/ImageSets/Main"
total_xml=os.listdir(xml)

num=len(total_xml)
tr=int(num*train_precent)
train=range(0,tr)

ftrain=open("handbone/orignal_data/ImageSets/train.txt","w")
ftest=open("handbone/orignal_data/ImageSets/val.txt","w")
ftrainval=open("handbone/orignal_data/ImageSets/trainval.txt","w")

for i in range(num):
    name=total_xml[i][:-4]
    if i in train:
        ftrain.write(name)
    else:
        ftest.write(name)

for i in range(num):
    name=total_xml[i][:-4]
    ftrainval.write(name)
ftrain.close()
ftest.close()
ftrainval.close()


