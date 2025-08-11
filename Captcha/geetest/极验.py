import cv2

raw_bg = cv2.imread('../shumei/bg.jpg')
raw_huakuai = cv2.imread('../shumei/fg.png')
canny_bg = cv2.Canny(raw_bg, 70, 200)
canny_huakuai = cv2.Canny(raw_huakuai, 70, 200)
res = cv2.matchTemplate(canny_bg, canny_huakuai, cv2.TM_CCOEFF_NORMED)
min_val,max_val,min_loc,max_loc= cv2.minMaxLoc(res)
x1, y1 = max_loc[0], max_loc[1]#左上角坐标签
x2, y2 = x1 + raw_huakuai.shape[1], y1 + raw_huakuai.shape[0]#右下角坐标

# 假设 raw_bg 是你的图像，x1, y1, x2, y2 是已经计算好的坐标
cv2.rectangle(raw_bg, (x1, y1), (x2, y2), (0, 0, 255), 2)

cv2.imshow('bg', raw_bg)
cv2.imshow('hakuai',raw_huakuai)
cv2.waitKey(0)
