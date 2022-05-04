import paho.mqtt.client as mqtt
import time
from grovepi import *
import base64
import numpy as np
import cv2

"""
EE 250L Lab 04 Starter Code
Members: Russell Tan and Scott Susanto
Github: https://github.com/usc-ee250-spring2022/lab05-lab5-russell-scott/tree/lab05/ee250/lab05

Run rpi_pub_and_sub.py on your Raspberry Pi.
"""

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    decodedMsg = str(msg.payload, "utf-8")
    print("on_message: " + msg.topic + " " + decodedMsg)

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    button = 2
    pinMode(button, "INPUT")
    cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 

    while True:
        ret,frame = cap.read() # return a single frame in variable `frame`
        cv2.imshow('frame',frame) #display the captured image
        if (digitalRead(button) == 1):
            print("hello")
            #cv2.imwrite('capture.jpg',frame)
            out = cv2.imwrite('capture.jpg', frame)
            if(out):
                print("Encoding and publishing image")
                img = cv2.imread('capture.jpg')
                im_arr = cv2.imencode('.jpg', img)[1]  # im_arr: image in Numpy one-dim array format.
                im_bytes = im_arr.tobytes()
                im_b64 = base64.b64encode(im_bytes)
                print(type(im_b64))
                client.publish("scottsus/image", im_b64)
                #client.publish("scottsus/image", im_bytes)
                
                #f = open('capture.jpg', 'rb')
                #fileContent = f.read()
                #byteArr = bytearray(fileContent)
                #client.publish("scottsus/image", byteArr, 0)
                #client.publish("scottsus/image", "hi")
            else:
                print("failed to save jpeg")


        time.sleep(2)
            






