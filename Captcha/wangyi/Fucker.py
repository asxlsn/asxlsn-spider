import torch
from PIL import Image
import cv2
from model import MyCNN
import torchvision.transforms as T
class Captcha:
    def __init__(self,model_path):
        self.model = MyCNN().cuda()
        params = torch.load(model_path)
        self.model = self.model.eval()
        self.model.load_state_dict(params)
        self.transforms = T.Compose([
            T.ToTensor()
        ])

    def fuck(self,img):
        img = cv2.resize(img, (320, 160))
        img = Image.fromarray(img)
        img = self.transforms(img)
        img = img.to(torch.float).cuda()
        img = img.unsqueeze(0)
        predict = self.model(img)
        result = torch.argmax(predict, axis=1).item()
        return result
