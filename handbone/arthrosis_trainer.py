import os.path

import torch.optim

from arthrosis_dataset import My_Data
from torch.utils.data import DataLoader
from torchvision import models
from torch import nn

# 训练模型


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

device = torch.device("mps" if torch.backends.mps.is_available() else 'cpu')
device = 'cpu'


def train(category):
    # category
    # 获取地址  MCP
    path = os.path.join('handbone/data/arthrosis',category)

    # 加载训练集和验证集
    train_datasets = My_Data(path=path, mode='train')
    val_datasets = My_Data(path=path, mode='val')

    train_loader = DataLoader(train_datasets, batch_size=50, shuffle=True)
    val_loader = DataLoader(val_datasets, batch_size=50, shuffle=True)

    # 加载模型
    model = models.resnet18()
    model.conv1 = nn.Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
    model.fc = nn.Linear(512, arthrosis[category][1])
    model = model.to(device)

    # 损失函数
    loss_func = nn.CrossEntropyLoss()
    # loss_func = nn.MultiLabelSoftMarginLoss()
    # 优化器
    opt = torch.optim.Adam(model.parameters())

    best_acc = 0
    for epoch in range(10):

        model.train()
        trian_loss = 0
        for i, (img, label) in enumerate(train_loader):
            img, label = img.to(device), label.to(device)

            out = model(img)
            loss = loss_func(out, label)

            opt.zero_grad()
            loss.backward()
            opt.step()

            trian_loss += loss.item()
        print("epoch ==> ",epoch, "train_loss ==> ", trian_loss/len(train_loader) )

        model.eval()
        # 训练期间验证训练成果
        val_loss = 0
        acc_loss = 0
        for i, (img, label) in enumerate(val_loader):
            img, label = img.to(device), label.to(device)

            out = model(img)
            loss = loss_func(out, label)

            acc = torch.mean(torch.eq(out.argmax(dim=1),label).float())

            val_loss += loss.item()
            acc_loss += acc.item()

        acc_avg = acc_loss/len(val_loader)
        print("val_loss == > ", val_loss/len(val_loader) ,"val_loss ==>" , acc_avg)
        if acc_avg > best_acc:
            best_acc = acc_avg
            if not os.path.exists("params"):
                os.mkdir("params")
            torch.save(model.state_dict(),f"params/{category}.pth")





if __name__ == '__main__':
    for item in arthrosis:
        print(f"{item}模型开始训练")
        train(item)
        print(f"{item}模型结束训练")