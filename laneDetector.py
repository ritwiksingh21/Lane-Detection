import cv2
import numpy as np
import matplotlib.pyplot as plt

def canny(image):
    grayimg = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blurimg = cv2.GaussianBlur(grayimg,(5,5),0)
    cannyimg = cv2.Canny(blurimg,50, 100)
    return cannyimg

def areaofinterest(image):
    height = image.shape[0]
    polygons = np.array([[(200, height), (1100,height), (550, 250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    maskedimg = cv2.bitwise_and(image, mask)
    return maskedimg

def displayline(image, lines):
    lineimg = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line
            cv2.line(lineimg, (x1,y1), (x2,y2), (0,0,255), 10)
        # Below: Coloring the lane using polygon.
        if lines.shape == (2,4):
            
            polygon2 = np.array([[(lines[0,0]+10, lines[0,1]), (lines[0,2]+5,lines[0,3]), (lines[1,2]-5, lines[1,3]), (lines[1,0]-10,lines[1,1])]])
            cv2.fillPoly(lineimg, polygon2, (50,255,0))
    return lineimg

def status(image, lines):
    if lines is not None:
        if lines.shape == (2,4):
            cv2.rectangle(displayimg,(480,510),(760,580),(50,200,0),-6)
            cv2.putText(displayimg,"Lane Visibility Good", (500,550),cv2.FONT_HERSHEY_PLAIN,1.5,(0,0,255),2)
            
        else:
            cv2.rectangle(displayimg,(480,510),(760,580),(5,0,180),-6)
            cv2.putText(displayimg,"Low Lane Visibility", (500,550),cv2.FONT_HERSHEY_PLAIN,1.5,(0,255,255),2)
    return displayimg
    
def averageslopeintercept(image, lines):
    leftfit = []
    rightfit = []
    l=0
    r=0
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1,y2), 1)
        slope = parameters[0]
        intercept = parameters[1 ]
        if slope < 0:
            leftfit.append((slope, intercept))
        else:
            rightfit.append((slope, intercept))
    if len(leftfit) > 0:
        leftfitaverage = np.average(leftfit, axis = 0)
        leftline = makecoordinates(image, leftfitaverage)
        l=1
    if len(rightfit) > 0:
        rightfitaverage = np.average(rightfit, axis = 0)
        rightline = makecoordinates(image, rightfitaverage)
        r=1
    
    if l==1 and r==1:
        return np.array([leftline, rightline])
    elif l==0 and r==1:
        return np.array([rightline])
    elif l==1 and r==0:
        return np.array([lefttline])
    
    
def makecoordinates(image, lineparameters):
    slope, intercept = lineparameters
    y1 = image.shape[0]
    y2 = int(y1*(3/6))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])
    
cap = cv2.VideoCapture("road.mp4")
while{cap.isOpened()}:
    _, frame = cap.read()
    cannyimg = canny(frame)
    croppedarea = areaofinterest(cannyimg)

    lines = cv2.HoughLinesP(croppedarea,2, np.pi/180, 100, np.array([]), minLineLength = 40, maxLineGap = 5)
    averagedlines = averageslopeintercept(frame, lines)
    lineimg = displayline(frame, averagedlines)

    displayimg = cv2.addWeighted(frame, 1, lineimg, 0.3, 1)
    status(displayimg, averagedlines)

    cv2.imshow("results", displayimg )
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
