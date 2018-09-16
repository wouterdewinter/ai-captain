#!/usr/bin/python
from time import time

import matplotlib.pyplot as plt

import csv
import os, glob

from sklearn.externals import joblib

from .ai_captain_utils import get_data
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier

import tensorflow as tf

import pickle

learning_data ,learning_labels,test_data ,test_labels = get_data()



clf = SVC()
t0 = time()
clf.fit(learning_data, learning_labels)
print("training time:", round(time() - t0, 3), "s")
pred = clf.predict(learning_data)
t0 = time()
score = accuracy_score(pred, learning_labels)
print("testing time:", round(time() - t0, 3), "s")
print('score = ' + str(score))
print("totale set " + str(len(pred)))

# save model
joblib.dump(clf, 'filename.pkl')
clf = joblib.load('filename.pkl')

pred = clf.predict(test_data)
t0 = time()
score = accuracy_score(pred, test_labels)
print("testing time:", round(time() - t0, 3), "s")
print('score = ' + str(score))
print("totale set " + str(len(pred)))
