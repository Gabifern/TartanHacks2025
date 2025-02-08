import cv2
import numpy as np
import matplotlib as plt

# Load image
image = cv2.imread('test_images/IMG_1888.jpg')
print("image")

image = cv2.resize(image, (360,720))

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(1,1),1000)
#flag, thresh = cv2.threshold(blur, 100, 140, cv2.THRESH_BINARY)
# thresh = cv2.adaptiveThreshold(
#     blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
# )
#flag, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
edges = cv2.Canny(gray, 50, 150)


#Find contours

contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea,reverse=True) 

#Select long perimeters only

perimeters = [cv2.arcLength(contours[i],True) for i in range(len(contours))]
listindex=[i for i in range(15) if perimeters[i]>perimeters[0]/2]
numcards=len(listindex)

#Show image

imgcont = image.copy()
[cv2.drawContours(imgcont, [contours[i]], 0, (0,250,0), 5) for i in listindex]
cv2.imshow("wee", imgcont)

cv2.waitKey(0)