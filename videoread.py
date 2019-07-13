# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 21:01:22 2019

@author: skambli
"""

import cv2

videoPath = "C:/openCVcode/videos/cctv.mp4"

cap = cv2.VideoCapture(videoPath)

while(True):
    ret,frame = cap.read()
    cv2.imshow('frame',frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()