# Import DroneKit-Python
from dronekit import connect
# Connect to the Vehicle.
vehicle = connect("/dev/ttyACM1", wait_ready=True)

# Get some vehicle attributes (state)
print("Get some vehicle attribute values:")
print(vehicle.location.global_frame)
print(vehicle.gps_0)
print(vehicle.attitude)
#print " Battery: %s" % vehicle.battery
#print " Last Heartbeat: %s" % vehicle.last_heartbeat
#print " Is Armable?: %s" % vehicle.is_armable
#print " System status: %s" % vehicle.system_status.state
#print " Mode: %s" % vehicle.mode.name    # settable
vehicle.close()