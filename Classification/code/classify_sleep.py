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
#
########################################################################################################################

def main():
	##### OPTIONS #############################################
	parser = argparse.ArgumentParser()
	parser.add_argument('-data', required=True, help='Path to data')
	parser.add_argument('-c', '--classifier', default='nb', help='nb | lr | log | svm')
	parser.add_argument('-m', '--model', default='gen', help='gen | ind')
	parser.add_argument('-v', '--verbose', help='verbose output')
	opts = parser.parse_args()
	############################################################

	##### BUILD TRAINING SET ###################################
	vectorizer = DictVectorizer(separator=',')

	# Load training text and training labels
	csv_file = open(opts.data)
	csv_reader = csv.reader(csv_file)
	next(csv_reader, None) # skip the header in the csv file

	# CLASSIFY WITH EVERYONE
	data = []
	labels = []
	next_item = next(csv_reader, None)

	if opts.model == 'gen':
		while next_item != None: 
			# quality = int(next_item[8]) #sleep quality
			# tts = int(next_item[9])
			# moveEvents = int(next_item[7]) #number of move events per night
			# data.append(moveEvents)
			# data.append(tts)
			# labels.append(quality)

			isAsleep = int(next_item[2])
			avgMove = float(next_item[1])
			data.append(avgMove)
			labels.append(isAsleep)

			next_item = next(csv_reader, None)
		csv_file.close()

		# data_train = np.reshape(data_train, (len(labels), 1))
		# data_test = np.reshape(data_test, (len(labels), 1))

		# data = np.reshape(data, (len(labels), 2) ) #two features
		data = np.reshape(data, (len(labels), 1) ) #only one feature
		data_train, data_test, labels_train, labels_test = train_test_split(data, labels, test_size=0.20)

		print "GENERAL CLASSIFIER:", opts.classifier
		[acc, test_acc] = classify(opts, data_train, data_test, labels_train, labels_test)
		print "accuracy:", acc
		print "test accuracy:", test_acc


	# CLASSIFY PER INDIVIDUAL
	if opts.model == 'ind':
		print "CLASSIFIER BY USER:", opts.classifier

		num_items = 0
		accuracies = [0,0]
		while next_item != None:
			num_items += 1
			user = next_item[0]
			data = []
			labels = []
			next_item = next(csv_reader, None)
			while next_item != None and next_item[0] == user:
				# quality = int(next_item[8]) #sleep quality
				# tts = int(next_item[9])
				# moveEvents = int(next_item[7]) #number of move events per night
				# data.append(moveEvents)
				# data.append(tts)
				# labels.append(quality)

				isAsleep = int(next_item[2])
				avgMove = float(next_item[1])
				data.append(avgMove)
				labels.append(isAsleep)

				next_item = next(csv_reader, None)
			if opts.verbose:
				print "\nuser ID:", user
			# data_train = np.reshape(data_train, (len(labels), 1))
			# data_test = np.reshape(data_test, (len(labels), 1))

			# data = np.reshape(data, (len(labels), 2) ) #two features
			data = np.reshape(data, (len(labels), 1) ) #only one feature
			data_train, data_test, labels_train, labels_test = train_test_split(data, labels, test_size=0.20)

			[acc, test_acc] = classify(opts, data_train, data_test, labels_train, labels_test)
			accuracies[0] += acc
			accuracies[1] += test_acc
		csv_file.close()
		print "number of users:", num_items
		print "average accuracy:", float(accuracies[0])/num_items
		print "average test accuracy:", float(accuracies[1])/num_items


# ############################################################

def classify(opts, data_train, data_test, labels_train, labels_test):
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
	# ############################################################


	# ###### VALIDATE THE MODEL ##################################
	# Print training mean accuracy
	accuracy = classifier.score(data_train, labels_train)
	if opts.verbose:
		print "accuracy = ", accuracy
	
	# Perform 10 fold cross validation (cross_validation.cross_val_score) with scoring='accuracy'
	# and print the mean score and std deviation
	# cv = cross_validation.KFold()
	if opts.classifier != 'lr':
		cross_val_scores = cross_validation.cross_val_score(classifier, data_train, labels_train, scoring='accuracy', cv=10)
		if opts.verbose:
			print "cross val mean = ",  cross_val_scores.mean()
			print "cross val stdev = ", cross_val_scores.std()

	# ############################################################

	test_accuracy = classifier.score(data_test, labels_test)
	if opts.verbose:
		print "test accuracy = ", test_accuracy

	# Predict labels for the test set
	labels_predicted = classifier.predict(data_test)
	labels_predicted = np.round(labels_predicted, 2) #round to hundredths place for readability
	# print "***************"
	if opts.verbose:
		print "actual labels:\n", labels_test
		print "predicted labels:\n", labels_predicted

	return [accuracy, test_accuracy]
	
	# ############################################################
	# ############# OTHER CLASSIFIER THINGS #############
	# # Print the classification report
	# print "Classification Report:"
	# print classification_report(labels_test, labels_predicted)

	# # Print the confusion matrix
	# print "Confusion Matrix:"
	# print confusion_matrix(labels_test, labels_predicted)

	# # Get predicted label of the test set
	# if opts.classifier != 'svm':
	# 	# Use predict_proba
	# 	test_predicted_proba = classifier.predict_proba(data_test)
	# 	# Plot ROC curve
	# 	# util.plot_roc_curve(labels_test, test_predicted_proba)
	# else:
	# 	# Use decision_funcion
	# 	test_predicted_proba = classifier.decision_funcion(data_test)

	# ##### EXAMINE THE MODEL ####################################
	# if opts.top is not None:
	# 	# print top n most informative features for positive and negative classes
	# 	util.print_most_informative_features(opts.classifier, vectorizer, classifier, opts.top)
	# ############################################################


	# ##### TEST THE MODEL #######################################
	# if opts.test is None:
	# 	# Test the classifier on one sample 
	# 	# TODO: sample item
	# 	test_item = [] 

	# 	# Print the predicted label of the test tweet
	# 	features = vectorizer.transform([test_item]) #list

	# 	# Print the predicted probability of each label.
	# 	if opts.classifier != 'svm':
	# 		# Use predict_proba
	# 		print classifier.predict_proba(features)
	# 	else:
	# 		# Use decision_funcion
	# 		print classifier.decision_funcion(features)

	# else:
	# 	# Test the classifier on the given test set
	# 	# Extract features from the test set and transform it using vectorizer

	# 	csv_file = open(opts.test)
	# 	csv_reader = csv.reader(csv_file) #read the tweets
	# 	next(csv_reader, None) # skip the header in the csv file

	# 	test_set = []
	# 	labels_test = []
	# 	next_item = next(csv_reader, None) #get one actor's tweets
	# 	while next_item != None: #go through all actor tweets
	# 		text = next_item[5]
	# 		label = next_item[0]
	# 		test_set.append(text)
	# 		labels_test.append(int(label))
	# 		next_item = next(csv_reader, None)
	# 	csv_file.close()

	# 	data_test = vectorizer.transform(test_set)
	# 	labels_test = np.array(labels_test) # make sure they're ints # transform to np array

	# 	# Print test mean accuracy
	# 	accuracy = classifier.score(data_test, labels_test)
	# 	print "test accuracy = ", accuracy

	# 	# Predict labels for the test set
	# 	labels_predicted = classifier.predict(data_test)


	# 	# Print the classification report
	# 	print "Classification Report:"
	# 	print classification_report(labels_test, labels_predicted)

	# 	# Print the confusion matrix
	# 	print "Confusion Matrix:"
	# 	print confusion_matrix(labels_test, labels_predicted)

	# 	# Get predicted label of the test set
	# 	if opts.classifier != 'svm':
	# 		# Use predict_proba
	# 		test_predicted_proba = classifier.predict_proba(data_test)
	# 		# Plot ROC curve
	# 		# util.plot_roc_curve(labels_test, test_predicted_proba)
	# 	else:
	# 		# Use decision_funcion
	# 		test_predicted_proba = classifier.decision_funcion(data_test)
	##############################################################

	#########################################################################
	# SLEEP DATA (this is danae's random brainstorming)
	#
	# There are three steps in processing the data:
	# 1. Classification
	# 2. Correlation
	# 3. Causation
	#
	# The broader goal here is to provide recommendations for improving sleep,
	# both based on an individual's own data, and based on a larger dataset.
	# To start, we'll focus on an individual's own data and try to use the 
	# first two thirds of that data to predict information that we can verify
	# in the last third of the data. 
	#
	# CLASSIFICATION
	# There are some basic things we should be able to classify:
	#	- Movement (what counts as a movement 'event' given raw data?)
	#	- Noise (what is a noise 'event' given raw data?)
	#	- Using that data (and other), when is a person asleep?
	# After we have these kinds of data and others, the raw data is 
	# sufficiently annotated for other classification. 
	# 
	# CORRELATION
	# I'm not totally sure where this fits in, but I think it's ike this:
	# Before we train a classifier to recognize and categorize different 
	# sleep events and phenomena, if we can show with a simple measure
	# of correlation that two attributes are correlated, then we will 
	# know that we can train a classifier to, with some reasonable
	# accuracy, predict an event or phenomenon when given test data. 
	# Otherwise, if two attributes seem completely unrelated (correlation
	# is at chance), we can't expect a classifier to use one attribute
	# to reliably predict the other. 
	#
	# CAUSATION
	# In order to give recommendations, we need to have some faith that the 
	# attributes which we see are correlated also have (ideally) some
	# causal relationship. This allows us to strongly make the claim that 
	# by following some piece of advice, the user will actually see changes
	# in their sleep. 
	# The important thing with causation is first to establish that the 
	# events being considered are in chronological order, and that changing
	# the first predicts a change in the second for new (testing) data.
	# In addition, a causation claim is much stronger if you can identify
	# a mechanism by which this process occurs. 
	#
	# PRE-PROCESSING
	# To preprocess, we need to be able to annotate the raw data with some
	# other variables:
	#	- Number/magnitude of movement/noise events per night
	#	- How many hours slept?
	#	- Is it a weekend?
	#	- How many hours slept over the last few nights?
	#		- Were there any esp. short sleeps over the previous 3 nights? 
	#########################################################################

 		
if __name__ == '__main__':
	main()
