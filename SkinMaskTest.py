from grovepi import *
import paho.mqtt.client as mqtt
import cv2
import time
import base64
import numpy as np

button = 2
pinMode(button, "INPUT")        # event listener for button press
cap = cv2.VideoCapture(0)       # turns on the video camera
cap.set(3,640) #Width=640
cap.set(4,480) #Height=480

while True:
    ret,frame = cap.read()      # return a single frame in variable `frame`
    if (digitalRead(button) == 0):
        hsvim = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower = np.array([0,48,80], dtype = "uint8")
        upper = np.array([20,255,255], dtype = "uint8")
        skinRegionHSV = cv2.inRange(hsvim, lower, upper)
        blurred = cv2.blur(skinRegionHSV, (2,2))
        ret, thresh = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY)
        cv2.imshow('thresh',thresh)   # display the captured image
        cv2.waitKey(1000)
        ##frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # image processing
        #out = cv2.imwrite('capture.jpg', frame)
