import paho.mqtt.client as mqtt
from gpiozero import DistanceSensor, MotionSensor
from time import sleep
import time
import sys

HOST = '37.187.16.177'
PORT = 1883


def read_data(send_data=True):
    ping = DistanceSensor(23, 24)
    pir = MotionSensor(4)
    
    if send_data:
        client = mqtt.Client()
        client.on_connect = lambda client, userdata, flags, rc: print("Broker connection established!")
        client.username_pw_set("pibroker", password="raspberry")
        client.connect(HOST, PORT, 7200)
    
    while True:
        ping_value = ping.distance
        pir_value = pir.motion_detected    
        print('Distance to nearest object is', ping_value, 'm')
        print('Is there someone? ', pir_value)
        if send_data:
                client.loop()    
                client.publish("pi2/ping/value", str({'time': time.time(), 'value': ping_value}))
                client.publish("pi2/pir/value", str({'time': time.time(), 'value': pir_value}))
        sleep(0.1)

def main():
    if len(sys.argv) == 2 and sys.argv[1]== "-debug":
        read_data(send_data=False)
    else:
        read_data(send_data=True)

if __name__ == "__main__":
    main()
