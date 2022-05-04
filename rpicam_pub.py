from grovepi import *
import paho.mqtt.client as mqtt
import cv2
import time
import base64
import numpy as np

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
    cap.set(3,640) #Width=640
    cap.set(4,480) #Height=480

    while True:
        ret,frame = cap.read()      # return a single frame in variable `frame`
        if (digitalRead(button) == 1):
            cv2.imshow('frame',frame)   # display the captured image
            cv2.waitKey(1000)
            frame = np.flip(frame, axis=-1)
            frame = cv2.GaussianBlur(frame, (9,9), 0)
            ##frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # image processing
            out = cv2.imwrite('capture.jpg', frame)
            if(out):
                print("Encoding and publishing image")
                img = cv2.imread('capture.jpg')
                im_arr = cv2.imencode('.jpg', img)[1]       # im_arr: image in Numpy one-dim array format.
                im_bytes = im_arr.tobytes()
                im_b64 = base64.b64encode(im_bytes)
                client.publish("scottsus/image", im_b64)
            else:
                print("Failed to save jpeg")
        time.sleep(2)
    
    vid.release()
    cv2.destroyAllWindows()






