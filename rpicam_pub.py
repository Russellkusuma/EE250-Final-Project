from grovepi import *
import paho.mqtt.client as mqtt
import cv2
import time
import base64

# Default message upon connection to broker
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code " + str(rc))

# Main function
if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    button = 2
    pinMode(button, "INPUT")        # event listener for button press
    cap = cv2.VideoCapture(0)       # turns on the video camera

    while True:
        ret,frame = cap.read()      # return a single frame in variable `frame`
        cv2.imshow('frame',frame)   # display the captured image
        if (digitalRead(button) == 1):
            out = cv2.imwrite('capture.jpg', frame)
            if(out):
                print("Encoding and publishing image")
                img = cv2.imread('capture.jpg')
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # image processing
                im_arr = cv2.imencode('.jpg', img)[1]       # im_arr: image in Numpy one-dim array format.
                im_bytes = im_arr.tobytes()
                im_b64 = base64.b64encode(im_bytes)
                client.publish("scottsus/image", im_b64)
            else:
                print("Failed to save jpeg")
        time.sleep(2)
            






