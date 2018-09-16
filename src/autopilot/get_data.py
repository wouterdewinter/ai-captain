#!/usr/bin/python
import sys
import os
from urllib import request
import time

from code.ai_captain_utils import PilotControl

ip_address = sys.argv[1]
course = sys.argv[2]
print("{} {}".format(ip_address,course))

def get_filename_datetime(course):
    # Use current date to get a text file name.
    timestr = time.strftime("%Y%m%d-%H%M%S")
    return "log-" + timestr +"_"+ course + ".txt"

# Get full path for writing.
name = get_filename_datetime(course)
print("NAME", name)

path = "./data/" + name
print("PATH", path);
auto_pilot_control = PilotControl(ip_address)

print(auto_pilot_control.set_course(course))
with open(path, "w") as f:
    # Write data to file.
    while True:

        f.write(auto_pilot_control.get_data_from_pilot()+"\n")
        time.sleep(8)


