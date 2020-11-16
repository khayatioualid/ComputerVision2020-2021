import cv2
import numpy as np
def resizeImage(img,ratio):
    # extraction des dimensions
    colonnes, lignes, couleurs = img.shape
    newSize=(int(lignes*ratio/100),int(colonnes*ratio/100))
    # redimentionnement de l'image
    newImg=cv2.resize(img,newSize)
    return  newImg

def filtrerNonQuadrilateres(contours):
    result=[]
    for contour in contours:
        approx=cv2.approxPolyDP(contour,10,True)
        if(len(approx)==4):
            result.append(approx)
    return result

def SelectBiggest(contours):

    biggest=None
    biggestSurface = 0
    for contour in contours:
        surface = cv2.contourArea(contour)
        if surface>biggestSurface:
            biggest=contour
            biggestSurface=surface
    return [biggest]

def reorder(myPoints):
    print("myPoints originaux (4,1,2) : ", myPoints)
    print("myPoints.shape : ", myPoints.shape)

    myPoints = myPoints.reshape((4, 2))
    print("myPoints (4.2): ", myPoints)
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)
    print("myPoints.sum(1) : ", myPoints.sum(1))

    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]

    return myPointsNew

def ExtractsDocuments(imageOriginale,imageOriginaleResizedContour,contoursCandidats,ratio):
    result=[]
    print(imageOriginaleResized.shape)
    heightImg,widthImg,_=imageOriginale.shape;
    for contour in contoursCandidats:
        contour=reorder(contour)
        cv2.drawContours(imageOriginaleResizedContour, contour, -1, (255, 0, 0), 20)
        pts1 = np.float32(contour)  # PREPARE POINTS FOR WARP
        for i in range(len(pts1)):
            pts1[i]=pts1[i]*(100/ratio)
        pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])  # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarpColored = cv2.warpPerspective(imageOriginale, matrix, (widthImg, heightImg))
        imgWarpGray=cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
        imgWarpGray=cv2.adaptiveThreshold(imgWarpGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                             cv2.THRESH_BINARY, 5, 2)
        kernel = np.ones((3, 3))
        """
        for i in range(1):
            #imgWarpGray = cv2.dilate(imgWarpGray, kernel, iterations=1)
            imgWarpGray = cv2.erode(imgWarpGray, kernel, iterations=1)
        """
        result.append([imgWarpColored,imgWarpGray])
    for i in range(len(result)):
        cv2.imshow("Extracted document colored "+str(i),result[i][0])
        cv2.imshow("Extracted document gray " + str(i), result[i][1])
        cv2.imwrite("./Scanned/DocumentColored"+str(i)+".jpg",result[i][0])
        cv2.imwrite("./Scanned/DocumentGray" + str(i) + ".jpg", result[i][1])
    return result

print(cv2.version.opencv_version)
imageOriginale=cv2.imread("../Data/scanner6.jpg")
ratio=20
imageOriginaleResized=resizeImage(imageOriginale,ratio)
imageOriginaleResizedGray=cv2.cvtColor(imageOriginaleResized, cv2.COLOR_BGR2GRAY)
ThresholdMin=100  #100
ThresholdMax=200  #200
imageOriginaleResizedGrayBlur = cv2.GaussianBlur(imageOriginaleResizedGray, (5, 5), 0)

ImageThreshold=cv2.Canny(imageOriginaleResizedGray,ThresholdMin,ThresholdMax)
cv2.imshow("ImageThreshold",ImageThreshold)
ImageThreshold=cv2.Canny(imageOriginaleResizedGrayBlur,ThresholdMin,ThresholdMax)
kernel = np.ones((5, 5))
ImgDilat=cv2.dilate(ImageThreshold,kernel,iterations=2)
ImageThresholdErode= cv2.erode(ImgDilat, kernel, iterations=1)


contoursImg=ImageThresholdErode.copy()
contours, hierarchy = cv2.findContours(contoursImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
imageOriginaleResizedContour=imageOriginaleResized.copy()
cv2.drawContours(imageOriginaleResizedContour,contours,-1,(0,255,0),3)

contoursCandidats=filtrerNonQuadrilateres(contours)
contoursCandidats=SelectBiggest(contoursCandidats)
cv2.drawContours(imageOriginaleResizedContour,contoursCandidats,-1,(0,0,255),2)

ExtractsDocuments(imageOriginale,imageOriginaleResizedContour,contoursCandidats,ratio)

cv2.imshow("imageOriginaleResized",imageOriginaleResized)
cv2.imshow("imageOriginaleResizedGray",imageOriginaleResizedGray)
cv2.imshow("imageOriginaleResizedGrayBlur",imageOriginaleResizedGrayBlur)
cv2.imshow("ImageThresholdBlur",ImageThreshold)
cv2.imshow("imageOriginaleResizedContour",imageOriginaleResizedContour)
cv2.imshow("ImgDilat",ImgDilat)
cv2.imshow("ImageThresholdErode",ImageThresholdErode)

while True:
    key=cv2.waitKey(1)
    if key==27 : break

#cap.release()
cv2.destroyAllWindows()


