import cv2
img = cv2.imread('image.jpg')
det = cv2.QRCodeDetector()
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
(thresh, img) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
val = det.detectAndDecodeMulti(img)
print("val:", val)