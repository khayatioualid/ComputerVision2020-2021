import numpy as np
import cv2

cap = cv2.VideoCapture("../Data/objets5.mp4")

while(True):
    # Charge les images frame par frame
    ret, frame = cap.read()

    cv2.imshow('image',frame)
    if cv2.waitKey(1) == 27:
        break

# il faut liberer les ressources avant de quitter le programme
cap.release()
cv2.destroyAllWindows()