#!/usr/bin/python
import sys
import time

import matplotlib.pyplot as plt

import csv
import os, glob

from sklearn.externals import joblib

from .ai_captain_utils import get_data, PilotControl
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier

import tensorflow as tf

import pickle

learning_data ,learning_labels,test_data ,test_labels = get_data()


file_name = sys.argv[1]
clf = joblib.load(file_name)

while True:
    pilot_control = PilotControl('192.168.1.12')
    pred = clf.predict([pilot_control.get_data_from_pilot()])
    pilot_control.set_rudder_angle(pred[0])
    time.sleep(3)

