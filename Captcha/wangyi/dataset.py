import cv2
import numpy as np
import os
from torch.utils.data import Dataset,DataLoader
import torchvision.transforms as T
from PIL import Image
from makeCaptcha import CaptchaGenerator



class CaptchaDataset(Dataset):
    def __init__(self,dataset_root_path):
        super(CaptchaDataset,self).__init__()
        self.image_paths = []
        for filename in os.listdir(dataset_root_path):
            img_path = os.path.join(dataset_root_path,filename)
            self.image_paths.append(img_path)



        self.image_paths = np.array(self.image_paths)
        np.random.seed(123)
        shutil_index = np.random.permutation(len(self.image_paths))
        self.image_paths = self.image_paths[shutil_index]
        self.transforms = T.Compose([
            T.ToTensor()
        ])
        self.gen = CaptchaGenerator()



    def __len__(self):
        return len(self.image_paths)


    def __getitem__(self,item):
        # 根据item索引)拿出相应的数据
        # 数据 标签

        img = cv2.imread(self.image_paths[item])
        img,lable = self.gen.genImg(img)
        img = Image.fromarray(img)
        img = self.transforms(img)
        return img,lable