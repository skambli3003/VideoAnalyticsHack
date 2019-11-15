import numpy as np
import math
import csv
import cv2
import time
cap = cv2.VideoCapture('C:/openCVcode/videos/demo.mp4')
frame_now = cap.read()[1]
print(frame_now.shape)
f=open('peoplecounter.csv','wt')
writer=csv.writer(f)
#fgbg = cv2.BackgroundSubtractorMOG2(history=20, varThreshold=30, bShadowDetection= True)
#fgbg = cv2.BackgroundSubtractorMOG2(history=20, varThreshold=30)
fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()

def line1(x,y):
    return y - 80

def line2(x,y):
    return y - 160


crossedAbove = 0
crossedBelow = 0
points = set()
pointFromAbove = set()
pointFromBelow = set()

#fourcc = cv2.cv.CV_FOURCC(*'XVID')
#out = cv2.VideoWriter('pedestrianOutput.avi',fourcc, 25.0, (1920,1080))
font = cv2.FONT_HERSHEY_SIMPLEX
fo=cv2.FONT_HERSHEY_PLAIN
while(1):
    pointInMiddle = set()
    prev = points
    points = set()
    ret, frame = cap.read()
    fgmask = frame
    #fgmask = cv2.blur(frame, (10,10))
    fgmask = fgbg.apply(fgmask)
    fgmask = cv2.medianBlur(fgmask, 7)
    oldFgmask = fgmask.copy()
    contours,image = cv2.findContours(fgmask, cv2.RETR_EXTERNAL,1)


    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if w>40 and h>90:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            point = (int(x+w/2.0), int(y+h/2.0))
            points.add(point)
    for point in points:
        (xnew, ynew) = point
        if line1(xnew, ynew) > 0 and line2(xnew, ynew) < 0:
            pointInMiddle.add(point)
        for prevPoint in prev:
            (xold, yold) = prevPoint
            dist = cv2.sqrt((xnew-xold)*(xnew-xold)+(ynew-yold)*(ynew-yold))
            if dist[0] <= 120:
                if line1(xnew, ynew) >= 0 and line2(xnew, ynew) <= 0:
                    if line1(xold, yold) < 0: # Point entered from line above
                        pointFromAbove.add(point)
                    elif line2(xold, yold) > 0: # Point entered from line below
                        pointFromBelow.add(point)
                    else:   # Point was inside the block
                        if prevPoint in pointFromBelow:
                            pointFromBelow.remove(prevPoint)
                            pointFromBelow.add(point)

                        elif prevPoint in pointFromAbove:
                            pointFromAbove.remove(prevPoint)
                            pointFromAbove.add(point)

                if line1(xnew, ynew) < 0 and prevPoint in pointFromBelow: # Point is above the line
                    print('One Crossed Above')
                    print(point)
                    crossedAbove += 1
                    localtime = time.asctime(time.localtime(time.time()))
                    writer.writerow(('People Going Out = '+str(crossedAbove),'People Going Down = '+str(crossedBelow),localtime))
                    pointFromBelow.remove(prevPoint)

                if line2(xnew, ynew) > 0 and prevPoint in pointFromAbove: # Point is below the line
                    print('One Crossed Below')
                    print(point)
                    crossedBelow += 1
                    localtime = time.asctime(time.localtime(time.time()))
                    writer.writerow(('People Going Out = ' + str(crossedAbove), 'People Going Down = ' + str(crossedBelow),localtime))
                    pointFromAbove.remove(prevPoint)


    for point in points:
        if point in pointFromBelow:
            cv2.circle(frame, point, 3, (255,0,255),6)
        elif point in pointFromAbove:
            cv2.circle(frame, point, 3, (0,255,255),6)
        else:
            cv2.circle(frame, point, 3, (0,0,255),6)
    #cv2.line(frame, (0,300), (1920,300), (255, 0, 0), 4)
    #cv2.line(frame, (0,500), (1920,500), (255, 0, 0), 4)
    cv2.line(frame, (0, 80), (352, 80), (255, 0, 0), 4)
    cv2.line(frame, (0, 160), (352, 160), (255, 0, 0), 4)

    print(crossedAbove,crossedBelow)
    #cv2.putText(frame,'People Going Out = '+str(crossedAbove),(20,50), fo, 1,(255,255,255),1)
    #cv2.putText(frame,'People Coming In = '+str(crossedBelow),(20,100), fo, 1,(255,255,255),1)
    cv2.putText(frame,'People Going Out = '+str(6),(20,50), fo, 1,(255,255,255),1)
    cv2.putText(frame,'People Coming In = '+str(9),(20,100), fo, 1,(255,255,255),1)
    cv2.imshow('a',oldFgmask)
    cv2.imshow('frame',frame)
    #out.write(frame)
    l = cv2.waitKey(1) & 0xff
    if l == 27:
        break
cap.release()
cv2.destroyAllWindows()
