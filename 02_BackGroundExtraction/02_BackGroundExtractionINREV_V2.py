import cv2
import numpy as np

def bgrTogray(frame):
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgGray = cv2.GaussianBlur(imgGray, (5, 5), 0)
    return imgGray

def difference(source,cible,threshold):
    result = cv2.absdiff(source, cible)
    _, result = cv2.threshold(result, threshold, 255, cv2.THRESH_BINARY)
    #result = cv2.adaptiveThreshold(result,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

    return result

class BackgroundSubtractorINREV:
    def __init__(self,updateRatio):
        self.lastFrame=None
        self.backGroundModel=None
        self.updateRatio=updateRatio
    def apply(self,frame):
        if np.shape(self.lastFrame)==():
            self.lastFrame=frame
            self.backGroundModel=frame
            return None
        self.lastFrameGray = bgrTogray(self.lastFrame)
        self.frameGray = bgrTogray(frame)
        mask=difference(self.frameGray,self.lastFrameGray,25)
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
        partialBackGround=frame.copy()
        partialForeGround = frame.copy()
        maskBackGround=cv2.bitwise_not(mask)
        partialBackGroundModel=self.backGroundModel.copy()
        partialBackGroundModel=cv2.bitwise_and(partialBackGroundModel, partialBackGroundModel, mask=mask)
        partialBackGround = cv2.bitwise_and(partialBackGround, partialBackGround, mask=maskBackGround)
        partialForeGround = cv2.bitwise_and(partialForeGround, partialForeGround, mask=mask)

        cv2.imshow("mask", mask)
        cv2.imshow("maskBackGround", maskBackGround)
        cv2.imshow("partialBackGround", partialBackGround)
        cv2.imshow("partialForeGround", partialForeGround)
        cv2.imshow("partialBackGroundModel", partialBackGroundModel)
        partialBackGroundModelPatched=cv2.add(partialBackGroundModel,partialBackGround)
        self.backGroundModel = cv2.addWeighted(self.backGroundModel, 1-self.updateRatio, partialBackGroundModelPatched, self.updateRatio, 0)

        cv2.imshow("backGroundModel", self.backGroundModel)

        cv2.imshow("contoursImg", contoursImg)

        self.backGroundModelGray=bgrTogray(self.backGroundModel)
        result = difference(self.frameGray, self.backGroundModelGray,10)

        return result




#methode 1
#subtractor=cv2.createBackgroundSubtractorMOG2(history=20,varThreshold=25,detectShadows=False)
#methode 2
#subtractor=cv2.createBackgroundSubtractorKNN(history=20,dist2Threshold =400,detectShadows=False)
#methode 3
subtractor=BackgroundSubtractorINREV(0.25)

cap=cv2.VideoCapture("../Data/Trafic autoroutier A15 (Partie 2).mp4")
while True:
    _, frame=cap.read()
    maskObjets=subtractor.apply(frame)
    if np.shape(maskObjets) == ():
        continue
    cv2.imshow("frame", frame)

    cv2.imshow("maskObjets", maskObjets)

    key=cv2.waitKey(30)
    if key==27:
        break