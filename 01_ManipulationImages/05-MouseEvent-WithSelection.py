# installer uniquement la partie opensource
# pip install opencv-python
# installer uniquement la partie opensource + la partie avec licences restrictive
# pip install opencv-contrib-python

import cv2
import numpy as np

img=cv2.imread("../Data/tomates.jpg" )
#extraction des dimensions
colonnes,lignes,couleurs=img.shape
A_X=-1
A_Y=-1
B_X=-1
B_Y=-1
buttonClicked=False

def calculerIntervalHSV(img,A,B):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    Xmin = min(A[0], B[0])
    Xmax = max(A[0], B[0])
    Ymin = min(A[1], B[1])
    Ymax = max(A[1], B[1])

    Hmax=0;Smax=0;Vmax=0
    Hmin=255;Smin=255;Vmin=255
    for x in range(Xmin,Xmax+1):
        for y in range(Ymin,Ymin+1):
            Hmax = max(Hmax, imgHSV[x, y][0])
            Hmin = min(Hmin, imgHSV[x, y][0])
            Smax = max(Smax, imgHSV[x, y][1])
            Smin = min(Smin, imgHSV[x, y][1])
            Vmax = max(Vmax, imgHSV[x, y][2])
            Vmin = min(Vmin, imgHSV[x, y][2])

    return (Hmin,Smin,Vmin),(Hmax,Smax,Vmax)

def mouseEventManager(event,x,y,flags,param):
    global A_X,A_Y,B_X,B_Y,buttonClicked
    if event == cv2.EVENT_LBUTTONDOWN:
        A_X=x
        A_Y=y
        cv2.circle(img, (x,y), 10, (255,0,0),2)
        cv2.imshow('Image Originale', img)
        buttonClicked=True

    if event == cv2.EVENT_LBUTTONUP:
        B_X = x
        B_Y = y
        cv2.circle(img, (x,y), 5, (0,255,0),2)
        cv2.imshow('Image Originale', img)
        buttonClicked = False
        (Hmin,Smin,Vmin),(Hmax,Smax,Vmax)=calculerIntervalHSV(img,(A_X,A_Y),(B_X,B_Y))
        print("(Hmin,Smin,Vmin),(Hmax,Smax,Vmax) =",(Hmin,Smin,Vmin),(Hmax,Smax,Vmax))

    if event == cv2.EVENT_MOUSEMOVE and buttonClicked==True:
        imgCopy=img.copy()
        cv2.rectangle(imgCopy,(A_X,A_Y),(x,y),(0,0,255),2)
        cv2.imshow('Image Originale', imgCopy)



cv2.imshow('Image Originale',img)
cv2.setMouseCallback('Image Originale',mouseEventManager)
while True:

    if(cv2.waitKey(1)==27):
        break

cv2.destroyAllWindows()