__author__ = 'arkilic'

import csv
import numpy as np
from sklearn.linear_model import SGDRegressor
import random
import pprint




print "Prediction on IBM 30 year data:"
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
    X.append(map(float, s_data[1:5]))
y = list()
y2 = list()
for s_data in data:
    y.append(float(s_data[4]))
    y2.append(float(s_data[1]))
pprint.pprint('Training the supervised learning model... Fit on training data')
print('=========================================')
try:
    clf = SGDRegressor(loss="huber")
    pprint.pprint(clf.fit(X, y))
except:
    raise
try:
    clf2 = SGDRegressor(loss="huber")
    pprint.pprint(clf2.fit(X, y2))
except:
    raise
print('=========================================')
print 'Model testing itself! Confidence score on the training data used to construct:', clf.score(X, y)
pprint.pprint('Ready to predict')
print('=========================================')


pprint.pprint('Testing with test data...')

test_data = list()
test_diff = list()
predict_diff = list()
for index in test_indices:
    tmp = data[index][1:5]
    my_tmp = list()
    for item in tmp:
        my_tmp.append(float(item))
    test_data.append(my_tmp)
    test_diff.append(float(data[index][4]) - float(data[index][1]))
# #
prediction_results_close = clf.predict(test_data)
prediction_results_open = clf2.predict(test_data)

for i in xrange(len(prediction_results_close)):
    p_diff = prediction_results_close[i] - prediction_results_open[i]
    predict_diff.append(p_diff)


print test_diff
print predict_diff

test_inc =0
for diff in test_diff:
    if diff > 0:
        test_inc += 1

p_inc =0



total_diff = 0
s = 0
for diff in predict_diff:
    total_diff += diff
    s += 1
    if diff > -0.22:
        p_inc += 1

pprint.pprint(total_diff/float(s))

print "The accuracy of the stock price prediction with 30 years of data ..: ", (p_inc/float(test_inc))*100
print "=========================================================================================\n"

print "Prediction on IBM 10 year data:"


f = open('HD-2004-2014-d.csv')
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
    X.append(map(float, s_data[1:5]))
y = list()
y2 = list()
for s_data in data:
    y.append(float(s_data[4]))
    y2.append(float(s_data[1]))
pprint.pprint('Training the supervised learning model... Fit on training data')
print('=========================================')
try:
    clf = SGDRegressor(loss="huber")
    pprint.pprint(clf.fit(X, y))
except:
    raise
try:
    clf2 = SGDRegressor(loss="huber")
    pprint.pprint(clf2.fit(X, y2))
except:
    raise
print('=========================================')
print 'Model testing itself! Confidence score on the training data used to construct:', clf.score(X, y)
pprint.pprint('Ready to predict')
print('=========================================')


pprint.pprint('Testing with test data...')

test_data = list()
test_diff = list()
predict_diff = list()
for index in test_indices:
    tmp = data[index][1:5]
    my_tmp = list()
    for item in tmp:
        my_tmp.append(float(item))
    test_data.append(my_tmp)
    test_diff.append(float(data[index][4]) - float(data[index][1]))
# #
prediction_results_close = clf.predict(test_data)
prediction_results_open = clf2.predict(test_data)

for i in xrange(len(prediction_results_close)):
    p_diff = prediction_results_close[i] - prediction_results_open[i]
    predict_diff.append(p_diff)


print test_diff
print predict_diff

p = 0
for entry in test_diff:
    if entry > 0:
        p += 1
k=0
for entry in predict_diff:
    if entry>-0.77:
        k += 1

print "The accuracy of the stock price prediction with 10 years of data ..: ", (p/float(k))*100
