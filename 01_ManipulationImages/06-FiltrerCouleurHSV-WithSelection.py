# installer uniquement la partie opensource
# pip install opencv-python
# installer uniquement la partie opensource + la partie avec licences restrictive
# pip install opencv-contrib-python

import cv2
import numpy as np

A_X=-1
A_Y=-1
B_X=-1
B_Y=-1
buttonClicked=False
colorMin=(-1,-1,-1)
colorMax=(-1,-1,-1)

def calculerIntervalHSV(img,A,B):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    Xmin = min(A[0], B[0])
    Xmax = max(A[0], B[0])
    Ymin = min(A[1], B[1])
    Ymax = max(A[1], B[1])

    Hmax=0;Smax=0;Vmax=0
    Hmin=255;Smin=255;Vmin=255
    for y in range(Xmin,Xmax+1):
        for x in range(Ymin,Ymin+1):
            Hmax = max(Hmax, imgHSV[x, y][0])
            Hmin = min(Hmin, imgHSV[x, y][0])
            Smax = max(Smax, imgHSV[x, y][1])
            Smin = min(Smin, imgHSV[x, y][1])
            Vmax = max(Vmax, imgHSV[x, y][2])
            Vmin = min(Vmin, imgHSV[x, y][2])

    return (Hmin,Smin,Vmin),(Hmax,Smax,Vmax)

def mouseEventManager(event,x,y,flags,param):
    global colorMin,colorMax,img,A_X,A_Y,B_X,B_Y,buttonClicked
    if event == cv2.EVENT_LBUTTONDOWN:
        A_X=x
        A_Y=y
        #cv2.circle(img, (x,y), 10, (255,0,0),2)
        cv2.imshow('Image Originale', img)
        buttonClicked=True

    if event == cv2.EVENT_LBUTTONUP:
        B_X = x
        B_Y = y
        #cv2.circle(img, (x,y), 5, (0,255,0),2)
        cv2.imshow('Image Originale', img)
        buttonClicked = False
        colorMin,colorMax=calculerIntervalHSV(img,(A_X,A_Y),(B_X,B_Y))
        print("(Hmin,Smin,Vmin),(Hmax,Smax,Vmax) =",colorMin,colorMax)
        imgFiltreHSV = filtrerCouleurHSV_Interval(img, colorMin, colorMax)
        cv2.imshow('Image Originale', img)
        cv2.imshow('Image Filtree HSV', imgFiltreHSV)

    if event == cv2.EVENT_MOUSEMOVE and buttonClicked==True:
        imgCopy=img.copy()
        cv2.rectangle(imgCopy,(A_X,A_Y),(x,y),(0,0,255),2)
        cv2.imshow('Image Originale', imgCopy)


def filtrerCouleurHSV_Interval(source,colorMin,colorMax):
    vEgalise = 100
    imgHSV = cv2.cvtColor(source, cv2.COLOR_BGR2HSV)
    imgHSVEgalise = egaliserV(imgHSV,vEgalise)

    #plus efficace car le travail est fait dans le code opencv qui est en C et C++
    min=np.array([colorMin[0],colorMin[1],vEgalise])
    max = np.array([colorMax[0],colorMax[1],vEgalise])
    print("TTT",(min,max))
    mask=cv2.inRange(imgHSVEgalise,min,max)
    cv2.imshow('Image mask HSV', mask)
    result=cv2.bitwise_and(source,source,mask=mask);
    cv2.imshow('Image HSV', imgHSV)
    cv2.imshow('Image HSV Egalise', imgHSVEgalise)
    return result

def egaliserV(source,V):
    result = source.copy()
    colonnes, lignes, couleurs = result.shape
    for x in range(colonnes):
        for y in range(lignes):
            result[x, y][2] = V
    return result

#exemple avec la balle
#img=cv2.imread("../Data/objets2.jpg" )

#exemple avec une main
img=cv2.imread("../Data/main2.jpg" )

colonnes,lignes,couleurs=img.shape
ratio=25
newSize=(int(lignes*ratio/100),int(colonnes*ratio/100))
# redimentionnement de l'image
img=cv2.resize(img,newSize)

cv2.imshow('Image Originale',img)
cv2.setMouseCallback('Image Originale',mouseEventManager)




while True:
    if(cv2.waitKey(1)==27):
        break

cv2.destroyAllWindows()