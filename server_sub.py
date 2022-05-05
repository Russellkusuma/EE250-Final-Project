import json
import paho.mqtt.client as mqtt
import time
import base64
import webbrowser

from api_utils import get_access_token, get_results, run_model
from argparser import parse_args
from utils import save_results
from jinja2 import Template
from flask import render_template

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

# Sending the image to the ML model on the cloud
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

    alphabet = ""
    if len(results['result']) == 0:                         # ML model unable to decipher image
        alphabet = "Unable to convert to alphabet!"
        print(alphabet)
    else:                                                   # ML model successfully deciphers image
        alphabet = results['result'][0]['class_name']
        print("The letter is:", alphabet)

    visualize(alphabet)


def visualize(alphabet):
    print("Visualizing on the browser...")

    html_file = """
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
                integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
                integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"
                crossorigin="anonymous"></script>
            <title>Document</title>
        </head>

        <body>
            <div class="container">
                <h1 class="mt-5">EE 250 Final Project: ASL Converter<h1>
                <h5 class="mb-5">Lab Members: Drew Uramoto, Russell Tan, Scott Susanto</h5>
                <h6 class="mb-5" style="text-align:justify; text-justify:inter-word; color:#868E96">Our program facilitates
                    communication between those with audio disabilities and those who do not understand sign language.
                    It works by first taking a picture of the hand sign, then applies image processing to clean the
                    picture before it is fed into the Machine Learning Algorithm, which is based in the Modelplace Cloud API. 
                    It then returns the corresponding english alphabet, which we display here on screen.</h6>
                <img src="output.jpg" class="img-fluid rounded mb-5">
                <h2>Based on the hand sign captured from the camera, the alphabet is: """ + alphabet + """!</h2>
            </div>

        </body>

        </html>
    """

    f = open("index.html", "w")
    f.write(html_file)
    f.close()

    webbrowser.open_new_tab('index.html')

    

# Main function
if __name__ == "__main__":

    visualize("I HATE EE250")

    # client = mqtt.Client()
    # client.on_connect = on_connect
    # client.on_message = on_message
    # client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    # client.loop_start()

    # while True:
    #     time.sleep(2)


