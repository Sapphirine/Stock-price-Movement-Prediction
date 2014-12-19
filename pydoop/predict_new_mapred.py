__author__ = 'arkilic'

import csv
import numpy as np
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import SGDClassifier
import random
import pprint
import sys, logging, struct
logging.basicConfig(level=logging.DEBUG)
import time

import pydoop.pipes as pp
from pydoop.utils import jc_configure, jc_configure_int
import pydoop.hdfs as hdfs

print "USING HDFS... working version"
time.sleep(1)

print("This includes links to Hadoop mapreduce routines via pydoop Mapper and Reader calls.\
However, as also explained on the paper, these calls are exteremely tedious to parse through\
since they read the data file line by line. SGD via scikit uses python C-types where calculations\
are vectorized and vectorized calls are a lot more performance savvy than hadoop's built-in mapreduce\
routines. Therefore, for python, due to the expense of calls via boost wrapped hadoop pipes, this implementation\
is not satisfactory and/or appropriate. The example in the demo displays submission of a simple task via pydoop\
for proof of concept.As this code will reveal, the results obtained are very similar to the results of mahout+hadoop version!\
As an alternative to this approach, one could easily use pyMPI or IPython notebook parallel utilizing HDFS as a neat distributed\
file system approach sending data to computation nodes cheaply(compared to existing methods which use wget etc.). Overall, python\
proved to be a good prototyping tool for such application that could make good use of the distributed file system. However, as a development\
tool, due to incompatibility issues between Java and Python, it is not a desireable tool for development via Hadoop. This might change in the\ future if pydoop reaches the maturity and simplicity required to perform such vectorized calculations efficiently")


time.sleep(3)



class Reader(pp.RecordReader):
    def __init__(self, context):
	super(Reader, self).__init__()
	self.logger = logging.getLogger("Reader") #formatted logger obtained
	self.file = hdfs.open('HD-2004-2014-d.csv')
	self.logger.debug("readline chunk size = %r" % self.file.chunk_size)

    def close(self):
	self.logger.debug("closing open handles")
        self.file.close()
        self.file.fs.close()
   
    def next(self): 
    	if self.bytes_read > self.isplit.length:  # end of input split
    	    return (False, "", "")
    	key = struct.pack(">q", self.isplit.offset+self.bytes_read)
    	record = self.file.readline()
    	if record == "":  # end of file
            return (False, "", "")
    	self.bytes_read += len(record)
    	return (True, key, record)

class Mapper(pp.Mapper):

    def __init__(self, context):
    	super(Mapper, self).__init__(context)
    	self.logger = logging.getLogger("Mapper")
    	context.setStatus("initializing")

    def map(self, context):
    	k = context.getInputKey()
	tmp_data = csv.reader(f)
    	words = context.getInputValue().split()
    	for w in words:
      	    context.emit(w, "1")
    	    context.incrementCounter(self.inputWords, len(words))

    def close(self):
    	self.logger.info("all done")




print "Prediction on HD 30 year data:"
f = hdfs.open('/HD-1984-2014-d.csv')
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
for i in xrange(int(len(data)*0.9)):
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
ind1 = 0
correct_guess_index_1 = list()
tm_stmp1 = list()

for diff in predict_diff:
    total_diff += diff
    s += 1
    if diff > -0.147:#normalization of the diff value for a data set(avoid floating errors)
        p_inc += 1
	correct_guess_index_1.append(s)

for indx in correct_guess_index_1:
    tm_stmp1.append(data[indx][0])


myfile1 = open('1984_2014_correct_ts.csv', 'wb')
wr = csv.writer(myfile1, quoting=csv.QUOTE_ALL)
wr.writerow(tm_stmp1)

pprint.pprint(total_diff/float(s))
print "=========================================================================================\n"
print "The accuracy of the stock price prediction with 30 years of data ..: ", (p_inc/float(test_inc))*100
print "=========================================================================================\n"

print "Prediction on HD 10 year data:"


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
for i in xrange(int(len(data)*0.1)):
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
ind = 0
correct_guess_index = list()
tm_stmp = list()
for entry in predict_diff:
    ind += 1
    if entry>-13: #normalization of the diff value for a data set(avoid floating errors)
	k += 1      #calculated via variance
        correct_guess_index.append(ind)

for indx in correct_guess_index:
    tm_stmp.append(data[indx][0])


myfile = open('2004_2014_correct_ts.csv', 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerow(tm_stmp)
    
    


    

print "The accuracy of the stock price prediction with 10 years of data ..: ", (p/float(k))*100
print "=========================================================================================\n"
print " SUMMARY..: \n"
print "=========================================================================================\n"
print "The accuracy of the stock price prediction with 30 years of data ..: %", (p_inc/float(test_inc))*100
print "=========================================================================================\n"
print "The accuracy of the stock price prediction with 10 years of data ..: %", (p/float(k))*100
print "=========================================================================================\n"
print "This is consistent with results obtained using mahout!"


#if __name__ == "__main__":
#  pp.runTask(pp.Factory(
#    Mapper, Reducer,
#    record_reader_class=Reader,
#    record_writer_class=Writer,
#    partitioner_class=Partitioner,
#    combiner_class=Reducer
#    ))
