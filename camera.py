from picamera import PiCamera
from time import sleep

import os, os.path
import socket


# Count the number of files in folder at the start of script
count = len([name for name in os.listdir(".")])

# Connect to the camera
camera = PiCamera()
camera.start_preview()


host = '192.168.87.105'
port = 60000

i = count
while True:
	# Make socket
	s = socket.socket()
	s.connect((host,port))
	file_name = "./image" + str(i) + ".jpg"
	sleep(10)
	camera.capture(file_name)
	print("Captured: " + file_name)

	f = open(file_name, 'rb')
	# Send file
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

