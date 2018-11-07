from picamera import PiCamera
from time import sleep

import os, os.path

# Count the number of files in folder
count = len([name for name in os.listdir(".")])

camera = PiCamera()

camera.start_preview()
for i in range(10):
	sleep(4)
	camera.capture('./image' + str(count) + '.jpg')

camera.stop_preview()
