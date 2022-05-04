import json
import paho.mqtt.client as mqtt
import time
import base64 

def read_json():
    f = open('./results/results.json')
    data = json.load(f)
    alphabet = data[0]['class_name']
    print("The letter is:", alphabet)

def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code " + str(rc))
    client.subscribe("scottsus/image")
    client.message_callback_add("proj/image", send_to_cloud)

def on_message(client, userdata, msg):
    print("Hello Russ!")
    decodedMsg = str(msg.payload, "utf-8")
    imgdata = base64.b64decode(decodedMsg)
    with open('russ.jpg', 'wb') as f:
        f.write(imgdata)
    print("Done!")


def send_to_cloud(client, userdata, image):
    print("Sending to cloud!")
    email = "econsproject123@gmail.com"
    password = "economics102"
    model_id = 42
    # jpegfile = "../../ASL Pictures/L.jpeg"
    jpegfile = image

    access_token = get_access_token(email, password)    
    task_id = run_model(model_id, jpegfile, access_token)
    results = get_results(task_id, access_token)
    alphabet = results['result'][0]['class_name']
    print("The letter is:", alphabet)

    client.publish("proj/display", alphabet)

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        print("Connecting...")
        time.sleep(2)


