#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import serial
import pynmea2
import threading
import time
import json
import numpy as np

#read GPS 
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
#read remote LoRa
def read_serial():
    global uav_lat
    global uav_lon
    global uav_alt
    global uav_pitch
    global uav_yaw
    global uav_roll
    global amp
    global index
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        try:
            raw_data = remote_gps_ser.readline().decode().rstrip()
            data = json.loads(raw_data)
            uav_lat = float(data["lat"])
            uav_lon = float(data["lon"])
            uav_alt = float(data["alt"])
            uav_pitch = float(data["pitch"])
            uav_yaw = float(data["yaw"])
            uav_roll = float(data["roll"])
            amp = float(data["amp"])
            index = float(data["index"])
        except:
            pass
            

if __name__ == '__main__':
    #open gps port
    local_gps_ser = serial.Serial()
    local_gps_ser.baudrate = 9600
    local_gps_ser.port = '/dev/tty.usbmodem141401'
    local_gps_ser.open()
    #open LoRa port
    remote_gps_ser = serial.Serial()
    remote_gps_ser.baudrate = 9600
    remote_gps_ser.port = '/dev/tty.usbmodem141301'
    remote_gps_ser.open()
    #variable define
    data_list = []
    ser_lat = 0.0
    ser_lon = 0.0
    ser_alt = 0.0
    uav_lat = 0.0
    uav_lon = 0.0
    uav_alt = 0.0
    uav_pitch = 0.0
    uav_yaw = 0.0
    uav_roll = 0.0
    amp = 0.0
    index = 0
    R = 6378137
    #start threading
    t_ser = threading.Thread(target=read_nmea1803, name='T1')
    t_ser.start()
    t_uav = threading.Thread(target=read_serial, name='T2')
    t_uav.start()
    
    while(1):
        print("Index: "+str(index))
        print("UAV lat: "+str(uav_lat))
        print("DUT lat: "+str(ser_lat))
        print("UAV lon: "+str(uav_lon))
        print("DUT lon: "+str(ser_lon))
        delta_x = (uav_lon-ser_lon)/180*np.pi*R
        delta_y = (uav_lat-ser_lat)/180*np.pi*R
        delta_z = (uav_alt-ser_alt)
        print("delta x: "+str(delta_x))
        print("delta y:"+str(delta_y))
        print("delta z:"+str(delta_z))
        print("D: " +str(np.sqrt(delta_x**2+delta_y**2)))
        print("UAV pitch: "+str(uav_pitch))     
        print("UAV yaw: "+str(uav_yaw))
        print("UAV roll: "+str(uav_roll))
        print("amplitude: "+str(amp))
        #data_temp = {"index":index,"uav_lat":uav_lat,"ser_lat"}
        
        
        if delta_x != 0 and delta_y != 0:
            print("AOA: "+str(np.arctan(delta_y/delta_x)/np.pi*180))
        else:
            print("Can not compute AOA!")
        print("============")
        time.sleep(1)
