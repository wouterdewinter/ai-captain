import glob
import os
import numpy as np
from urllib import request

def get_header():
    return ',angle_of_attack,boat_angle,boat_heel,boat_speed,course_error,datetime,rudder_angle,target_angle,wind_direction,wind_speed'

"""last_data_line = '{},{},{},{},{},{},{},{},{},{}'.format(
        pitch,
        roll,
        acceleration,
        gps_coordiates['latitude'],
        gps_coordiates['longitude'],
        course,
        rudder_angle,
        utc_time,
        real_course,
        speed
    )"""
def reformat_row(row):
    row = row.replace("(","").replace(")","").replace("\n","").split(',')
    formatted_row = {}
    formatted_row.append(0) # empty
    formatted_row.append(0) # angle of attack

    formatted_row.append(row[-1]) # boat angle
    formatted_row.append(row[1]) # boat heel TODO: Calibrate
    formatted_row.append(row[-1])
    formatted_row.append()

    return formatted_row



def get_data():
    learning_data = []
    learning_labels = []
    test_data = []
    test_labels = []
    os.chdir("")
    i = 0

    for file_log in glob.glob("*.txt"):
        with open(file_log) as file:


            for row in file:
                row = reformat_row(row)
                print(row)
                if i % 10 == 0:
                    test_data.append(row[0:-1])
                    test_labels.append(int(int(row[-1])/50))
                else:
                    learning_data.append(row[0:-1])
                    learning_labels.append(int(int(row[-1])/50))
                i += 1

    return np.array(learning_data),\
           np.array(learning_labels), \
           np.array(test_data), \
           np.array(test_labels)


class PilotControl(object):

    def __init__(self, ip_address):
        self.ip_address = ip_address

    def set_course(self, course):
        course_url = "http://" + self.ip_address + "/set_course/" + str(course) + "/"
        page = request.urlopen(course_url)
        return page.read()

    def get_data_from_pilot(self):
        url = "http://" + self.ip_address + "/get_data/"
        page = request.urlopen(url)
        return page.read()

    def set_rudder_angle(self, angle):
        angle = max(155, angle)
        angle = min(700, angle)
        rudder_angle_url = "http://" + self.ip_address + "/set_rudder/" + str(angle) + "/"

        print("sending translated rudder position: ", angle)
        page = request.urlopen(rudder_angle_url)
        return page.read()

    def stop_pilot(self):
        url = "http://" + self.ip_address + "/autopilot_off/"
        page = request.urlopen(url)
        return page.read()

    def arm_out(self):
        url = "http://" + self.ip_address + "/rudder_out/"
        page = request.urlopen(url)
        return page.read()

    def arm_in(self):
        url = "http://" + self.ip_address + "/rudder_in/"
        page = request.urlopen(url)
        return page.read()

    def arm_stop(self):
        url = "http://" + self.ip_address + "/rudder_stop/"
        page = request.urlopen(url)
        return page.read()

