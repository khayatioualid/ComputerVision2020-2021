import cv2
import numpy as np

def bgrTogray(frame):
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgGray = cv2.GaussianBlur(imgGray, (5, 5), 0)
    return imgGray

def difference(source,cible):
    result = cv2.absdiff(source, cible)
    _, result = cv2.threshold(result, 25, 255, cv2.THRESH_BINARY)
    return result

class BackgroundSubtractorINREV:
    def __init__(self):
        self.lastFrame=None
    def apply(self,frame):
        if np.shape(self.lastFrame)==():
            self.lastFrame=frame
            return None
        self.lastFrameGray = bgrTogray(self.lastFrame)
        self.frameGray = bgrTogray(frame)
        mask=difference(self.frameGray,self.lastFrameGray)
        self.lastFrame = frame
        contoursImg=frame.copy()

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # affichage des contours
        #cv2.drawContours(contoursImg,contours,-1,(0,255,0),3)


        for contour in contours :
            contours_poly = cv2.approxPolyDP(contour, 3, True)
            x,y,w,h = cv2.boundingRect(contours_poly)
            cv2.rectangle(contoursImg, (int(x), int(y)), \
                          (int(x+w), int(y+h)),
                          (0, 0, 255),2)
            cv2.rectangle(mask, (int(x), int(y)), \
                          (int(x + w), int(y + h)),
                          (255,), -1)

        cv2.imshow("contoursImg", contoursImg)
        return mask




#methode 1
#subtractor=cv2.createBackgroundSubtractorMOG2(history=20,varThreshold=25,detectShadows=False)
#methode 2
#subtractor=cv2.createBackgroundSubtractorKNN(history=20,dist2Threshold =400,detectShadows=False)
#methode 3
subtractor=BackgroundSubtractorINREV()

cap=cv2.VideoCapture("../Data/Trafic autoroutier A15 (Partie 2).mp4")
while True:
    _, frame=cap.read()
    mask=subtractor.apply(frame)
    if np.shape(mask) == ():
        continue
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)

    key=cv2.waitKey(30)
    if key==27:
        break