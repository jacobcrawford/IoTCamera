# IoTCamera

## To setup the pi camera do the following:

1. Connect the camera to the pi with the pins facing the hdmi port

2. ssh into the pi and run

 `sudo raspi-config`

3. Select "Interfaceing options"

4. Select "P1 camera" and enable the camera

5. Reboot pi

6. Run 

`sudo apt-get install python3-picamera`

7. Spend 4 hours installing openCV

8. install mqtt client

` pip install paho-mqtt`

# You can now run:

`python camera.py` To open a websocket connection an send a picture analysed with openCV
OR
`python mqtt_camera.py` To publish to a mqtt broker if a person is detected by the camera or not
