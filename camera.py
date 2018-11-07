from picamera import PiCamera
from time import sleep

import os, os.path

# Count the number of files in folder
count = len([name for name in os.listdir(".")])

camera = PiCamera()

camera.start_preview()

sleep(5)

camera.capture('./image' + str(count) + '.jpg')

camera.stop_preview()
