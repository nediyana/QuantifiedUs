from __future__ import division
import sys
import csv
import argparse
from collections import defaultdict

import util

import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import classification_report, confusion_matrix #can't find this???
from sklearn import cross_validation
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.cross_validation import train_test_split

########################################################################################################################
#
# CLASSIFY_SLEEP.PY
#
# To run, navigate to the directory where this code is, and:
# python classify_sleep.py -data [path to data] -c [classifier: nb | lr | log | svm] -m [size: gen | ind] -v [1 | 0]
#
# 
#
########################################################################################################################

def print_csv(fields):
	return ','.join([str(i) for i in fields])

def main():
	##### OPTIONS #############################################
	parser = argparse.ArgumentParser()
	parser.add_argument('-train', required=True, help='Path to data')
	parser.add_argument('-test', required=True, help='Path to data')
	parser.add_argument('-c', '--classifier', default='nb', help='nb | lr | log | svm')
	parser.add_argument('-v', '--verbose', help='verbose output')
	opts = parser.parse_args()
	############################################################

	##### BUILD TRAINING SET ###################################
	vectorizer = DictVectorizer(separator=',')

	# Load training text and training labels
	csv_train = open(opts.train)
	csv_train = csv.reader(csv_train)
	next(csv_train, None) # skip the header in the csv file

	# CLASSIFY WITH EVERYONE
	data_train = []
	data_test = []
	labels_train = []
	labels_test = []

	next_train = next(csv_train, None)

	while next_train != None: 
		isAsleep = int(next_train[2])
		avgMove = float(next_train[1])
		data_train.append(avgMove)
		if avgMove > 0.2:
			isAsleep = 1
		else:
			isAsleep = 0
		labels_train.append(isAsleep)
		# print avgMove, isAsleep

		next_train = next(csv_train, None)

	data_train = np.reshape(data_train, (len(labels_train), 1))

	classifier = classify(opts, data_train, labels_train)


	# Load training text and training labels
	csv_test = open(opts.test)
	csv_test = csv.reader(csv_test)
	next(csv_test, None) # skip the header in the csv file

	print print_csv(['id', 'asleepTime','awakeTime','currTime','accel','isAsleep=1', 'noise'])
	next_test = next(csv_test, None)

	while next_test != None:
		avgMove = 0
		numPts = 0
		userid = next_test[0]
		night = next_test[1]
		morning = next_test[2]
		currTime = next_test[3]
		accel = next_test[4]
		noise = next_test[5]

		while next_test != None and currTime == next_test[3]:
			print print_csv( [userid,night,morning,currTime,accel,None, noise] )#print previous night's stuff so that outside this loop the one with the averages gets printed
			userid = next_test[0]
			night = next_test[1]
			morning = next_test[2]
			currTime = next_test[3]
			accel = next_test[4]
			if next_test[5] != "None":
				noise = next_test[5]

			avgMove += float(next_test[4])
			numPts += 1
			next_test = next(csv_test, None)

		avgMove = float(avgMove)/numPts
		pred = int(classifier.predict(avgMove)[0])
		# print avgMove, pred
		print print_csv( [userid,night,morning,currTime,accel,pred, noise] )


# ############################################################

def classify(opts, data_train, labels_train):
	# ##### TRAIN THE MODEL ######################################
	# Initialize the corresponding type of the classifier and train it (using 'fit')
	if opts.classifier == 'nb':
		classifier = BernoulliNB(binarize=None)
		
	elif opts.classifier == 'lr':
		classifier = LinearRegression()

	elif opts.classifier == 'log':
		classifier = LogisticRegression()
		
	elif opts.classifier == 'svm':
		classifier = LinearSVC()
		
	else:
		raise Exception('Unrecognized classifier!')

	classifier.fit(data_train, labels_train) #all np

	# ###### VALIDATE THE MODEL ##################################
	# Print training mean accuracy
	accuracy = classifier.score(data_train, labels_train)
	# if opts.verbose:
	# 	print "accuracy = ", accuracy
	
	# ############################################################

	# Predict labels for the test set
	# labels_predicted = classifier.predict(data_test)
	# labels_predicted = np.round(labels_predicted, 2) #round to hundredths place for readability
	# # print "***************"
	# if opts.verbose:
	# 	print "predicted labels:\n", labels_predicted

	return classifier
	
 		
if __name__ == '__main__':
	main()
