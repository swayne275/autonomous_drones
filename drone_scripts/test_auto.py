#!/usr/bin/env python

import drone_control
import time
import threading
import multiprocessing

# Simple test of the exploration function
# Drone tries to locate a source of gas using naive_exploration to set new waypoints
#

def drone_explore_start(drone):
    drone.bringup_drone()
    drone.arm_and_takeoff(20)
    while True:
        drone.naive_exploration()
        time.sleep(1)

def drone_bringup(drone):
    drone.bringup_drone()
    drone.arm_and_takeoff(20)

drones = []
n=1
for i in xrange(n):
    drone = drone_control.AutoPilot(simulated=True, sim_speedup=2)
    drones.append(drone)
    drone_bringup(drone)

# sensor_db = drone_control.SampleDB()
# sensor_db.sync_from(6001)

while True:
    for drone in drones:
        # drone.naive_exploration()

        # Just do nothing and test the model
        # You can change the location in APM planner to see different values
        print "RSSI = {0}".format(drone.get_signal_strength())
    time.sleep(1)
