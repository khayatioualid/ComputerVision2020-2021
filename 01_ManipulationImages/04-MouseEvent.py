# installer uniquement la partie opensource
# pip install opencv-python
# installer uniquement la partie opensource + la partie avec licences restrictive
# pip install opencv-contrib-python

import cv2
import numpy as np

img=cv2.imread("../Data/tomates.jpg" )
#extraction des dimensions
colonnes,lignes,couleurs=img.shape


def mouseEventManager(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(img[x,y])
        cv2.circle(img, (x,y), 10, (255,0,0),2)
        cv2.imshow('Image Originale', img)


cv2.imshow('Image Originale',img)
cv2.setMouseCallback('Image Originale',mouseEventManager)
while True:

    if(cv2.waitKey(1)==27):
        break

cv2.destroyAllWindows()