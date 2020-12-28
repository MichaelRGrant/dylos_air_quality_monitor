#!/usr/bin/python3

import grp
import os
import pwd
import re
import time
from collections import OrderedDict

import pandas as pd
import serial

"""
Reads the USB port for the Dylos air quality monitor and saves the results to the dataframe at the path listed. 
"""
PATH = "/home/pi/dylos_air_quality_monitor/air_quality_2021.csv"

# check if PATH exists and if not create empty dataframe
if os.path.exists(PATH):
    dylos_df = pd.read_csv(PATH)
# Because this python file gets started up at boot on the pi,
# it runs as root so the ownership of files that get created
# automatically need to be changed to `pi` for write privileges.
# `pi` is the default user so this should be changed to whatever your
# username is.
else:
    dylos_df = pd.DataFrame()
    uid = pwd.getpwnam("pi").pw_uid
    gid = grp.getgrnam("pi").gr_gid
    open(PATH, "w+").close()
    os.chown(PATH, uid, gid)

# ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as ser:
    while True:
        line = str(ser.readline())
        if line != "b''":
            line = str(line).split(",")
            small = re.sub("[^0-9]", "", line[0])
            large = re.sub("[^0-9]", "", line[1])
            tz_offset = -time.timezone / 3600
            now = pd.to_datetime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            dylos_df = dylos_df.append(
                pd.DataFrame(
                    # Use an OrderedDict to preserve column order in dataframe
                    OrderedDict(
                        (
                            ("time", now),
                            ("offset_from_utc", tz_offset),
                            ("year", now.year),
                            ("month", now.month),
                            ("day", now.day),
                            ("hour", now.hour),
                            ("minute", now.minute),
                            ("small_particles", small),
                            ("large_particles", large),
                        )
                    ),
                    index=[0],
                )
            )
            dylos_df.reset_index(drop=True, inplace=True)
            dylos_df.to_csv(PATH, index=False)
            print(dylos_df)

