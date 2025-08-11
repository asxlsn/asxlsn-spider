import cv2
import numpy as np

img= cv2.imread('dataset/fj.jpg')
img = cv2.resize(img, (320, 160))
img = img.astype(np.float64)
img[0:80,0:80,:] *=0.7
img = img.astype(np.uint8)
cv2.imshow('img',img)
temp = img[0:80,0:80,:].copy()
#第一块和第二块交换
img[0:80,0:80,:] = img[0:80,160:240,:]
img[0:80,160:240,:] = temp

cv2.imshow('img',img)

cv2.waitKey(0)