# installer uniquement la partie opensource
# pip install opencv-python
# installer uniquement la partie opensource + la partie avec licences restrictive
# pip install opencv-contrib-python

import cv2
import numpy as np

def filtrerCouleurPython(source,r,g,b):
# probleme de lenteur car le travail est fait dans python
    result=source.copy()
    colonnes, lignes, couleurs = result.shape
    for x in range(colonnes):
        for y in range(lignes):
            # attention opencv représente les pixels en BGR et non en RGB
            #if not((result[x,y][0]==b)and(result[x,y][1]==g)and(result[x,y][2]==r)):
            #une deuxieme façon de faire la comparaison
            if not(result[x, y] == (b, g, r)).all():
                result[x, y]=(0,0,0)
    return result

def filtrerCouleur(source,r,g,b):
    #plus efficace car le travail est fait dans le code opencv qui est en C et C++
    min=np.uint8([b,g,r])
    max = np.uint8([b, g, r])
    mask=cv2.inRange(source,min,max)
    cv2.imshow('Image mask', mask)
    result=cv2.bitwise_and(source,source,mask=mask);
    return result

def filtrerCouleurHSV(source,r,g,b):
    bgrColors=np.uint8([[[b,g,r ]]])
    hsvColors = cv2.cvtColor(bgrColors, cv2.COLOR_BGR2HSV)
    h,s,v=hsvColors[0,0]
    #plus efficace car le travail est fait dans le code opencv qui est en C et C++
    min=np.uint8([h-10,s-10,v-1])
    max = np.uint8([h+10, s+10, v+1])
    mask=cv2.inRange(source,min,max)
    cv2.imshow('Image mask HSV', mask)
    result=cv2.bitwise_and(source,source,mask=mask);
    return result

def egaliserH(source):
    result = source.copy()
    colonnes, lignes, couleurs = result.shape
    for x in range(colonnes):
        for y in range(lignes):
            result[x, y][2] = 100
    return result


img=cv2.imread("../Data/tomates.jpg" )
#extraction des dimensions
#methode 1 avec code python tres lente !!!!
#imgFiltre=filtrerCouleurPython(img,237,28,36)
imgFiltre=filtrerCouleur(img,190,24,24)

imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
imgHSVEgalise=egaliserH(imgHSV)
imgFiltreHSV=filtrerCouleurHSV(imgHSVEgalise,190,24,24)

cv2.imshow('Image Originale',img)
cv2.imshow('Image HSV',imgHSV)
cv2.imshow('Image HSV Egalise',imgHSVEgalise)

cv2.imshow('Image Filtree',imgFiltre)
cv2.imshow('Image Filtree HSV',imgFiltreHSV)
while True:
    if(cv2.waitKey(1)==27):
        break

cv2.destroyAllWindows()