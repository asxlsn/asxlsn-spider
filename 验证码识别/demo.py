import ddddocr
ocr = ddddocr.DdddOcr()
open_img = open('OIP-C.jpg', 'rb').read()
result = ocr.classification(open_img)
print(result)