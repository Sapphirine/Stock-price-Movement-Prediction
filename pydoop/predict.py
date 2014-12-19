__author__ = 'arkilic'

import csv
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import SGDRegressor
import random
import pprint
import sys, logging, struct
logging.basicConfig(level=logging.DEBUG)



import pydoop.pipes as pp
from pydoop.utils import jc_configure, jc_configure_int
import pydoop.hdfs as hdfs


f = open('HD-1984-2014-d.csv')
tmp_data = csv.reader(f)

my_data = list()
for item in tmp_data:
    tmp_item = list()
    for i in item:
        tmp_item.append(i)
    my_data.append(tmp_item)
data = my_data[1:]
X = list()
training_indices = list()
for i in xrange(int(len(data)*0.8)):
    training_indices.append(i)

test_indices = list()
for i in xrange(int(len(data))):
    if i in training_indices:
        pass
    else:
        if i == 0:
            pass
        else:
            test_indices.append(i)
for s_data in data:
    X.append(map(float, s_data[1:4]))
y = list()
for s_data in data:
    y.append(float(s_data[4]))

pprint.pprint('Training the supervised learning model... Fit on training data')
print('=========================================')

try:
    clf = SGDRegressor(loss="huber")
    pprint.pprint(clf.fit(X, y))
except:
    raise
print('=========================================')
print 'Model testing itself! Confidence score on the training data used to construct:', clf.score(X, y)
pprint.pprint('Ready to predict')
print('=========================================')
pprint.pprint('Testing with test data...')
test_data = list()
test_res = list()
for index in test_indices:
    tmp = data[index][1:4]
    my_tmp = list()
    for item in tmp:
        my_tmp.append(float(item))
    test_data.append(my_tmp)
    test_res.append(float(data[index][4]))

prediction_results = clf.predict(test_data)

error_array = abs(prediction_results-test_res)/(test_res)*100
print 'Error on the data set is as following on item basis...:', error_array

print 'Average error is...:', sum(error_array)/float(len(error_array)), ' percent'
