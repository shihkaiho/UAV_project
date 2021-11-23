import time
import json
#from pymavlink import mavutil
import serial
ser = serial.Serial('/dev/ttyACM0',9600)
time.sleep(3)
counter = 1
while True:
    ser.write((str(counter)+"\n").encode())
    print("transmitted: "+str(counter))
    time.sleep(0.3)
    if(ser.in_waiting):
        try:
            line = ser.readline().decode().rstrip()
            print("received: "+line)
        except:
            print("error")
    counter = counter+1
    time.sleep(0.3)
