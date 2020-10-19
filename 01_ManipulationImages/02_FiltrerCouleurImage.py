# installer uniquement la partie opensource
# pip install opencv-python
# installer uniquement la partie opensource + la partie avec licences restrictive
# pip install opencv-contrib-python

import cv2
import numpy as np

def filtrerCouleurPython(source,r,g,b):
    result=source.copy()
    colonnes, lignes, couleurs = result.shape
    for x in range(colonnes):
        for y in range(lignes):
            # attention opencv représente les pixels en BGR et non en RGB
            if not((result[x,y][0]==b)and(result[x,y][1]==g)and(result[x,y][2]==r)):
                result[x, y]=(0,0,0)
    return result

def filtrerCouleur(source,r,g,b):
    min=np.uint8([b,g,r])
    max = np.uint8([b, g, r])
    mask=cv2.inRange(source,min,max)
    cv2.imshow('Image mask', mask)
    result=cv2.bitwise_and(source,source,mask=mask);
    return result



img=cv2.imread("../Data/cercles.png" )
#extraction des dimensions
#methode 1 avec code python tres lente !!!!
#imgFiltre=filtrerCouleurPython(img,237,28,36)
imgFiltre=filtrerCouleur(img,237,28,36)


cv2.imshow('Image Originale',img)
cv2.imshow('Image Filtree',imgFiltre)
while True:
    if(cv2.waitKey(1)==27):
        break

cv2.destroyAllWindows()