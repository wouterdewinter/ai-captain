import glob
import os
import numpy as np
from urllib import request


def reformat_row(row):
    row = row.replace("(","").replace(")","").replace("\n","").split(',')
    formatted_row = row[0:1]
    formatted_row.append(row[2])
    formatted_row.append(row[3])
    formatted_row.append(row[4])
    formatted_row.append(row[5])
    formatted_row.append(row[6])
    formatted_row.append(row[7])
    formatted_row.append(row[10])
    formatted_row.append(row[11])
    formatted_row.append(int(row[7])-int(float(row[10])))
    formatted_row.append(row[8])
    return formatted_row


def get_data():
    learning_data = []
    learning_labels = []
    test_data = []
    test_labels = []
    os.chdir("data_boat")
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
        rudder_angle_url = "http://" + self.ip_address + "/set_rudder/" + str(angle) + "/"
        page = request.urlopen(rudder_angle_url)
        return page.read()

    def stop_pilot(self):
        url = "http://" + self.ip_address + "/autopilot_off/"
        page = request.urlopen(url)
        return page.read()

