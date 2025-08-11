import torch
import torch.nn as nn
import cv2
import numpy as np
import os
from torch.utils.data import Dataset,DataLoader
import torchvision.models as models
import  torchvision.transforms as T
from PIL import Image


class CatDogDataset(Dataset):
    def __init__(self,is_train=True):
        super(CatDogDataset,self).__init__()
        self.image_paths = []
        self.labels = []
        for filename in os.listdir('./data/train/cat'):
            img_path = './data/train/cat' + filename
            img = cv2.imread(img_path)
            if img is not None:
                self.image_paths.append(img_path)
                self.labels.append(0)

        for filename in os.listdir('./data/train/dog'):
            img_path = './data/train/dog' + filename
            img = cv2.imread(img_path)
            if img is not None:
                self.image_paths.append(img_path)
                self.labels.append(1)

        self.image_paths = np.array(self.image_paths)
        self.labels = np.array(self.labels)
        np.random.seed(123)
        shutil_index = np.random.permutation(len(self.image_paths))
        self.image_paths = self.image_paths[shutil_index]
        self.labels = self.labels[shutil_index]

        if is_train:
            self.transforms = T.Compose([
                T.RandomHorizontalFlip(),
                T.RandomRotation(30),
                T.Resize(400,400),
                T.RandomCrop(300),
                T.ToTensor()
            ])
            self.image_paths = self.image_paths[:int(len(self.image_paths)*0.8)]
            self.labels = self.labels[:int(len(self.labels)*0.8)]
        else:
            self.transforms = T.Compose([
                T.Resize(300,300),
                T.ToTensor()
            ])

    def _len_(self):
        return len(self.labels)


    def __getitem__(self,item):
        # 根据item索引)拿出相应的数据
        # 数据 标签

        img = cv2.imread(self.image_paths[item])
        if img is not None:
            img = Image.fromarray(img)
            img = self.transforms(img)
        return img,self.labels[item]




cv2.imread()

train_dataset = CatDogDataset()
test_dataset = CatDogDataset(False)
train_loader = DataLoader(test_dataset,batch_size=8,shuffle=True)
tetst_loader = DataLoader(test_dataset,batch_size=8,shuffle=False)


class MyCNN(torch.nn.Module):
    def __init__(self):
        super(MyCNN, self).__init__()
        self.resnet = models.resnet50(pretrained=True)
        self.resnet.fc = nn.Linear(2048, 200)
        self.fc1 = nn.Linear(200, 200)
        self.fc2 = nn.Linear(200, 200)
        self.fc3 = nn.Linear(200, 28)
        self.relu = nn.ReLU()

    def forward(self, x):
        output = self.resnet(x)
        output = self.fc1(output)
        output = self.relu(output)
        output = self.fc2(output)
        output = self.relu(output)
        output = self.fc3(output)
        return output
        return output

model = MyCNN().cuda()