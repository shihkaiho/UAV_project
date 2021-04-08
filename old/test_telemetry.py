"""
This script will introduce multiple things:
 > Run the simulator inside dronekit
 > Read and handle telemetry from the UAV
 > Read and change parameters
"""

from dronekit import connect, VehicleMode
import time

#--- Start the Software In The Loop (SITL)
import dronekit_sitl
#
connection_string = "/dev/ttyACM0"
baud_rate=57600

#--- Now that we have started the SITL and we have the connection string (basically the ip and udp port)...

print(">>>> Connecting with the UAV <<<")
vehicle = connect(connection_string,baud=baud_rate, wait_ready=True)     #- wait_ready flag hold the program untill all the parameters are been read (=, not .)

#- Read the actual position
print('Position: %s'% vehicle.location.global_frame)

#- Read the actual attitude roll, pitch, yaw
print('Attitude: %s'% vehicle.attitude)

#- Read the actual velocity (m/s)
print('Velocity: %s'%vehicle.velocity) #- North, east, down


print('gps0: %s'%vehicle.gps_0)
#--- Now we close the simulation
vehicle.close()

print("done")
