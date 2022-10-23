#!/usr/bin/env python

import sys
import time
from Blobo import Blobo

try:
    address = sys.argv[1]
except IndexError:
    print("Missing BT address.")
    try:
        for i in [1, 5, 15]:
            print(f"Discovering devices (duration = {i})")
            devs = Blobo.find_all(i)
            if devs:
                address = devs[0]
                break
        else:
            print("No blobos.")
            exit(1)
    except:
        print("Error in discovery.")
        exit(1)

print(f"Connecting to {address}")
blobo = Blobo(address)

try:
    while not blobo.stopped:
        time.sleep(0.1)
        print("accelerometer = {:6}, {:6}, {:6}".format(*blobo.accelerometer))
        print("gyroscope     = {:6}, {:6}, {:6}".format(*blobo.gyroscope))
        print("magnetometer  = {:6}, {:6}, {:6}".format(*blobo.magnetometer))
        print("pressure      = {:6}".format(blobo.pressure))
        print("---------------------------------------------")
except KeyboardInterrupt:
    print("Quitting.")
finally:
    blobo.stop()
