#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# read reomte GPS
#import time
import json
import serial
remote_gps_ser = serial.Serial()
remote_gps_ser.baudrate = 9600
remote_gps_ser.port = '/dev/tty.usbmodem142301'
remote_gps_ser.open()

while True:
    if(remote_gps_ser.in_waiting):
        try:
            raw_data = remote_gps_ser.readline().decode().rstrip()
            data = json.loads(raw_data)
            print(json.dumps(data, sort_keys=True, indent=4))
        except:
            print("error")