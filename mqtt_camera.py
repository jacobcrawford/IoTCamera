from picamera import PiCamera
from time import sleep
import time
import os, os.path
from subprocess import call
import paho.mqtt.client as mqtt

import numpy as np
import cv2 as cv

# initialize classifiers
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

# Connect to the camera
camera = PiCamera()
camera.start_preview()

#Define functions for mqtt client

def on_connect(client,userdata,flags,rc):
	print("Broker connection established")

host = '37.187.16.177'
port = 1883

client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set("pibroker",password="raspberry")
client.connect(host,port,7200)
# Let the camera warm up
sleep(2)

while True:
	client.loop()
	#file_name = "./image" + str(i) + ".jpg"
	file_name = "./image.jpg"
	sleep(0.1)
	# Take picture
	current = time.time()
	camera.capture(file_name)
	
	# Analyse with openCV
	img = cv.imread(file_name)

	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	#Check if any faces are there
	
	if isinstance(faces, tuple):
		client.publish("pi/cam/value",str({'time':current,'value':0}))
		print("0 published")
	else:
		client.publish("pi/cam/value",str({'time':current, 'value':1}))
		print("1 published")

	
camera.stop_preview()

print( "Done sending image")

