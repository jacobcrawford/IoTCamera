from picamera import PiCamera
from time import sleep

import os, os.path

# Count the number of files in folder
count = len([name for name in os.listdir(".")])

camera = PiCamera()

camera.start_preview()

for i in range(10):
	file_name = "./image" + str(count + i) + ".jpg"
	sleep(4)
	camera.capture(file_name)
	print("Captured: " + file_name)

camera.stop_preview()
