To run the script with the simulator:

1. Start APM 2.0, turn on advanced mode and set up the UDP link to use port 14551

2. Start dronekit-sitl in a separate terminal:

    dronekit-sitl copter-3.3 --home=-35.363261,149.165230,584,353

3. Start MAVproxy in a second separate terminal:
    
    mavproxy.py --master tcp:127.0.0.1:5760 --sitl 127.0.0.1:5501 --out 127.0.0.1:14550 --out 127.0.0.1:14551

4. Run the script!