import cv2
import numpy as np


# webcam
cap = cv2.VideoCapture(0)
cap.set(3, 720) # width
cap.set(4, 1080) # height
cap.set(10, 100) # brightness

#myColor = [29, 62, 26, 255, 170, 255] # ktx
myColor = [17, 102, 66, 185, 154, 255]
myPoints = []
def findColor(img, myColor):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    newPoints = []
    lower = np.array([myColor[0],myColor[2],myColor[4]])
    upper = np.array([myColor[1],myColor[3],myColor[5]])
    mask = cv2.inRange(imgHSV,lower,upper)
    x,y = getContours(mask)
    cv2.circle(imgRes,(x,y),10,(255,0,0),cv2.FILLED)
    if x!= 0 and y!=0:
        newPoints.append([x,y])
    cv2.imshow("img", mask)
    return newPoints

def getContours(img):
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for c in contours:
        area = cv2.contourArea(c)
        if area > 500:
            #cv2.drawContours(imgRes, c, -1, (255,0,0), 3)
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y

def draw(myPoints):
    for p in myPoints:
        cv2.circle(imgRes, (p[0], p[1]), 10, (255, 0, 0), cv2.FILLED)


while True:
    success, img = cap.read()
    imgRes = img.copy()

    newPoints = findColor(img,myColor)
    if len(newPoints) != 0:
        for p in newPoints:
            myPoints.append(p)
    if len(myPoints) != 0:
        draw(myPoints)
    cv2.imshow("WebCam", imgRes)
    if cv2.waitKey(1) & 0xFF == ord('q'): # press q to quit
        break