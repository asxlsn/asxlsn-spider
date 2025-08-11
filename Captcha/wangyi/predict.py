import cv2

from Fucker import Captcha
from makeCaptcha import CaptchaGenerator

gen = CaptchaGenerator()
fucker = Captcha('./epoch599_train_acc_0.875_test_acc_0.8660714626312256.pt')
img = cv2.imread('yzm.jpg')
# img,label = gen.genImg(img)#模拟验证码
result = fucker.fuck(img)
print("预测：{}".format(result))


