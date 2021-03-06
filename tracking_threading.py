#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import serial
import pynmea2
import threading
import time
import json
import numpy as np

def read_nmea1803():
    global ser_lat
    global ser_lon
    global ser_alt
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        try:
            msg = local_gps_ser.readline().decode().rstrip()
            if msg[0:6] == '$GNGGA':
                msg = pynmea2.parse(msg)
                if msg.lat=='' or msg.lon=='':
                    print("no GPS data")
                    continue
                ser_lat = float(msg.lat[0:2])+float(msg.lat[2:])/60.
                ser_lon = float(msg.lon[0:3])+float(msg.lon[3:])/60.
                ser_alt = float(msg.altitude)+float(msg.geo_sep)
        except:
            pass

def read_serial():
    global uav_lat
    global uav_lon
    global uav_alt
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        try:
            raw_data = remote_gps_ser.readline().decode().rstrip()
            data = json.loads(raw_data)
            uav_lat = float(data["lat"])
            uav_lon = float(data["lon"])
            uav_alt = float(data["alt"])
        except:
            pass
            

if __name__ == '__main__':
    local_gps_ser = serial.Serial()
    local_gps_ser.baudrate = 9600
    local_gps_ser.port = '/dev/tty.usbmodem141301'
    local_gps_ser.open()
    
    remote_gps_ser = serial.Serial()
    remote_gps_ser.baudrate = 9600
    remote_gps_ser.port = '/dev/tty.usbmodem141101'
    remote_gps_ser.open()
    
    turn_table_ser = serial.Serial()
    turn_table_ser.baudrate = 9600
    turn_table_ser.port = "/dev/tty.usbserial-00000000"
    turn_table_ser.open()
    
    ser_lat = 0.0
    ser_lon = 0.0
    ser_alt = 0.0
    uav_lat = 0.0
    uav_lon = 0.0
    uav_alt = 0.0
    turn_angle = 0.0
    R = 6378137
    t_ser = threading.Thread(target=read_nmea1803, name='T1')
    t_ser.start()
    t_uav = threading.Thread(target=read_serial, name='T2')
    t_uav.start()
    while(1):
        print(uav_lat)
        print(ser_lat)
        print(uav_lon)
        print(ser_lon)
        delta_x = (uav_lon-ser_lon)/180*np.pi*R
        delta_y = (uav_lat-ser_lat)/180*np.pi*R
        delta_z = (uav_alt-ser_alt)
        print(delta_x)
        print(delta_y)
        print(delta_z)
        print("D:" +str(np.sqrt(delta_x**2+delta_y**2)))
        if delta_x != 0:
            print("azimuth: "+str(np.arctan(delta_y/delta_x)/np.pi*180))
            turn_angle = np.arctan(delta_y/delta_x)/np.pi*180
        print("============")
        move.on_the_fly_move_x(turn_angle)
        time.sleep(1)
