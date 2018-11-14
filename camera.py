from picamera import PiCamera
from time import sleep

import os, os.path
import socket

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


# Set server ip and port for the server you want to connect to
host = '192.168.87.105'
port = 60000

i = count
while True:
	# Make socket
	s = socket.socket()
	s.connect((host,port))

	file_name = "./image" + str(i) + ".jpg"
	sleep(5)
	# Take picture
	camera.capture(file_name)
	print("Captured: " + file_name)

	# Analyse with openCV
	img = cv.imread(file_name)
	print(img)

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
	# Send file
	f = open(file_name, 'rb')
	l = f.read(1024)
	while(l):
		s.send(l)
		l = f.read(1024)
	# Close file
	f.close()
	i+=1
	print("File sent")
	# Close socket
	s.close()
camera.stop_preview()

print( "Done sending image")

