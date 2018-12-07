import time
import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

import paho.mqtt.client as mqtt

host = '37.187.16.177'
port = 1883

def on_connect(client,userdata,flags,rs):
	print("Connected to broker!")

client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set("pibroker","raspberry")
client.connect(host, port, 7200)


while True:
    
    client.loop()
    time.sleep(0.1)
    value = adc.read_adc(0, gain=GAIN)
    print(value)
    current = time.time()
    json = str({'time':current,'value':value})
    client.publish("pi3/pressure/value",json)
    """
    if adc.read_adc(0, gain=GAIN) < 23000:
        print("Occupied")
    else:
        print("Available")
    time.sleep(0.1)
    """
