# installer uniquement la partie opensource
# pip install opencv-python
# installer uniquement la partie opensource + la partie avec licences restrictive
# pip install opencv-contrib-python

import cv2
import numpy as np

img=cv2.imread("../Data/cercles.png" )
#extraction des dimensions
colonnes,lignes,couleurs=img.shape
#calcul de la nouvelle dimension
ratio=50
newSize=(int(lignes*ratio/100),int(colonnes*ratio/100))
# redimentionnement de l'image
newImg=cv2.resize(img,newSize)
print(img.shape)

cv2.imshow('Image Originale',img)
cv2.imshow('Image redimensionnee',newImg)
while True:
    if(cv2.waitKey(1)==27):
        break

cv2.destroyAllWindows()