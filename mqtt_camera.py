from picamera import PiCamera
from time import sleep

import os, os.path
import paho.mqtt.client as mqtt

import numpy as np
import cv2 as cv

# initialize classifiers
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('haarcascade_eye.xml')

# Count the number of files in folder at the start of script
count = len([name for name in os.listdir(".")])

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
client.connect(host,port,3600)

i = count
while True:
	client.loop()
	file_name = "./image" + str(i) + ".jpg"
	sleep(5)
	# Take picture
	camera.capture(file_name)
	print("Captured: " + file_name)

	# Analyse with openCV
	img = cv.imread(file_name)

	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	for (x,y,w,h) in faces:
    		cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    		roi_gray = gray[y:y+h, x:x+w]
    		roi_color = img[y:y+h, x:x+w]
    		eyes = eye_cascade.detectMultiScale(roi_gray)
    		for (ex,ey,ew,eh) in eyes:
        		cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
	
	
	cv.imwrite(file_name,img)

	#Check if any faces are there
	print(faces)
	if isinstance(faces, tuple):
		client.publish("pi/cam/value",0)
		print("Noone there published")
	else:
		client.publish("pi/cam/value",1)
		print("Someone was there published")

	i+=1
	print("File sent")
	# Close socket
camera.stop_preview()

print( "Done sending image")

