# EE250 Final Project

## Lab Members:
Drew Uramoto, Russell Tan, Scott Susanto

## Link to demo:
https://drive.google.com/drive/u/0/folders/1-49tY47brkUnAqfFn6SqdLyiAnmD-zRM


## External Libraries used:
- GrovePi
- Paho-MQTT
- OpenCV
- Modelplace Cloud AI
- base64
- webbrowser


## Requirements

1. Install Python 3.7+
    ```bash
    sudo apt install python3.8
    ```
2. Clone this repository
    ```bash
    git clone git@github.com:susantoscott/EE250-Final-Project.git
    ```
3. Change directory
    ```bash
    cd ./EE-250-Final-Project
    ```
4. Install requirements
   ```bash
   python3 -m pip install -r requirements.txt
   ```

## Usage

To quickly start using our app,

run the following command in the server node:
```bash
python3 server_sub.py
```
run the following command in the sensor node:
```bash
python3 rpicam_pub.py
```

## Troubleshooting

If you get any troubles working with Modelplace Cloud API, please, contact us at
scottsus@usc.edu and rctan@usc.edu

