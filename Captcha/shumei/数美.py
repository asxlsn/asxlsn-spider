import cv2
import numpy as np
def extract_image(img):
    start_r = 0
    end_r = 0
    for r in range(img.shape[0]):
        if np.sum(img[r,:,:])>0:
            start_r = r
            print(r)
            for rr in range(r+1,img.shape[0]):
                if np.sum(img[rr,:,:])==0:
                    end_r = rr
                    print(rr)
                    break
            break
    return img[start_r:end_r+1,:,:],start_r,end_r

raw_bg = cv2.imread('bg.jpg')
raw_huakuai = cv2.imread('fg.png')
real_huakuai, start_r, end_r = extract_image(raw_huakuai)
print(real_huakuai.shape)
rol_bg = raw_bg[start_r:end_r+1,:,:]
# cv2.imshow('huakuai',real_huakuai)
# cv2.waitKey(0)

canny_bg = cv2.Canny(rol_bg, 70, 200)
canny_huakuai = cv2.Canny(real_huakuai, 70, 200)
res = cv2.matchTemplate(canny_bg, canny_huakuai, cv2.TM_CCOEFF_NORMED)
min_val,max_val,min_loc,max_loc= cv2.minMaxLoc(res)
x1, y1 = max_loc[0], max_loc[1]+start_r#左上角坐标签
x2, y2 = x1 + raw_huakuai.shape[1], y1 + real_huakuai.shape[0]#右下角坐标
# 假设 raw_bg 是你的图像，x1, y1, x2, y2 是已经计算好的坐标
cv2.rectangle(raw_bg, (x1, y1), (x2, y2), (0, 0, 255), 2)

print(max_loc)
cv2.imshow('bg', raw_bg)
cv2.imshow('huakuai',real_huakuai)
cv2.waitKey(0)
