import cv2
import numpy as np

cap=cv2.VideoCapture("../Data/Trafic autoroutier A15 (Partie 2).mp4")

#methode 1
subtractor=cv2.createBackgroundSubtractorMOG2(history=20,varThreshold=25,detectShadows=False)
#methode 2
#subtractor=cv2.createBackgroundSubtractorKNN(history=20,dist2Threshold =400,detectShadows=False)

while True:
    _, frame=cap.read()
    mask=subtractor.apply(frame)
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)

    key=cv2.waitKey(30)
    if key==27:
        break