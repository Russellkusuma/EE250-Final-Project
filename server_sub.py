import json
import paho.mqtt.client as mqtt
import time
import base64

from api_utils import get_access_token, get_results, run_model
from argparser import parse_args
from utils import save_results

# Default message upon connection to broker, subscribing to "scottsus/image"
def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code " + str(rc))
    client.subscribe("scottsus/image")

# Upon receiving the image, send it to the cloud for processing
def on_message(client, userdata, msg):
    decodedMsg = str(msg.payload, "utf-8")
    imgdata = base64.b64decode(decodedMsg)
    with open('output.jpg', 'wb') as f:
        f.write(imgdata)
    send_to_cloud()

def send_to_cloud():
    print("Sending to cloud!")
    email = "scottsus@usc.edu"  # credentials
    password = "Susanto0!"
    model_id = 42
    jpegfile = "./output.jpg"
    # jpegfile = "../../ASL Pictures/Dx.jpeg"

    access_token = get_access_token(email, password)        # auth   
    task_id = run_model(model_id, jpegfile, access_token)   # task
    results = get_results(task_id, access_token)            # results

    if len(results['result']) == 0:                         # ML model unable to decipher image
        print("Unable to convert to alphabet!")
    else:                                                   # ML model successfully deciphers image
        alphabet = results['result'][0]['class_name']
        print("The letter is:", alphabet)

    # client.publish("proj/display", alphabet)

# Main function
if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(2)


