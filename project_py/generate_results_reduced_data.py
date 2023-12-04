import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import time

T = 50
num_features = 4

#get raw data
file_path = "./project_data/data.csv"
raw_data = pd.read_csv(file_path, delimiter=',', on_bad_lines='skip')
raw_data = raw_data.drop('CONTRIBUTING FACTOR VEHICLE 1', axis=1)
raw_data = raw_data.drop('CONTRIBUTING FACTOR VEHICLE 2', axis=1)
raw_data = raw_data.drop('VEHICLE TYPE CODE 1', axis=1)
raw_data = raw_data.drop('VEHICLE TYPE CODE 2', axis=1)

#one hot encoding
features = pd.get_dummies(raw_data)
# print("one hot encoding shape: ", features.shape)
#(1609485, 206)

#isolate y variable
y = np.array(features['NUMBER OF PERSONS KILLED'])

#remove y variable from feature data
features = features.drop('NUMBER OF PERSONS KILLED', axis=1)

feature_names = list(features.columns)

features = np.array(features)

#get training and testing data, and training and testing labels
train_X, test_X, train_y, test_y = train_test_split(features, y, test_size=.2, random_state=42)

#instantiate with T decision trees
# rf = RandomForestRegressor(n_estimators=T, random_state=42, max_depth=depth, verbose=2)
rf = RandomForestRegressor(n_estimators=T, random_state=42, max_features=num_features)

#train the model
start = time.time()
rf.fit(train_X, train_y)
end = time.time()
training_time = end-start
# print("model training finished, time elapsed = ", end - start)

#use the test data
start = time.time()
predictions = rf.predict(test_X)
end = time.time()

testing_time = end - start
# print("model prediction finished, time elapsed = ", end - start)

#testing errors
errors = abs(predictions - test_y)
# non_zero_errors = len(np.where(errors > 0)[0])
# print("number of non zero errors: ", non_zero_errors, " , %", (non_zero_errors/errors.shape[0])*100)
# print("Mean absolute error: ", round(np.mean(errors), 2))

mae = sum(errors)/test_y.shape[0]

accuracy = 100 - ((mae/np.max(test_y)) * 100)
r2 = rf.score(test_X, test_y)

# print("accuracy = ", accuracy)

#get most important features]
importances = list(rf.feature_importances_)
# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_names, importances)]
# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
# Print out the feature and importances 
print(training_time, "\n", mae, "\n", accuracy, "\n", r2, "\n", feature_importances[:20])

#get raw data
file_path = "./project_data/data_injuries.csv"
raw_data = pd.read_csv(file_path, delimiter=',', on_bad_lines='skip')
raw_data = raw_data.drop('CONTRIBUTING FACTOR VEHICLE 1', axis=1)
raw_data = raw_data.drop('CONTRIBUTING FACTOR VEHICLE 2', axis=1)
raw_data = raw_data.drop('VEHICLE TYPE CODE 1', axis=1)
raw_data = raw_data.drop('VEHICLE TYPE CODE 2', axis=1)

#one hot encoding
features = pd.get_dummies(raw_data)
# print("one hot encoding shape: ", features.shape)
#(1609485, 206)

#isolate y variable
y = np.array(features['NUMBER OF PERSONS INJURED'])

#remove y variable from feature data
features = features.drop('NUMBER OF PERSONS INJURED', axis=1)

feature_names = list(features.columns)

features = np.array(features)

#get training and testing data, and training and testing labels
train_X, test_X, train_y, test_y = train_test_split(features, y, test_size=.2, random_state=42)

#instantiate with T decision trees
# rf = RandomForestRegressor(n_estimators=T, random_state=42, max_depth=depth, verbose=2)
rf = RandomForestRegressor(n_estimators=T, random_state=42, max_features=num_features)

#train the model
start = time.time()
rf.fit(train_X, train_y)
end = time.time()
training_time = end-start
# print("model training finished, time elapsed = ", end - start)

#use the test data
start = time.time()
predictions = rf.predict(test_X)
end = time.time()

testing_time = end - start
# print("model prediction finished, time elapsed = ", end - start)

#testing errors
errors = abs(predictions - test_y)
# non_zero_errors = len(np.where(errors > 0)[0])
# print("number of non zero errors: ", non_zero_errors, " , %", (non_zero_errors/errors.shape[0])*100)
# print("Mean absolute error: ", round(np.mean(errors), 2))

mae = sum(errors)/test_y.shape[0]

accuracy = 100 - ((mae/np.max(test_y)) * 100)
r2 = rf.score(test_X, test_y)

# print("accuracy = ", accuracy)

#get most important features]
importances = list(rf.feature_importances_)
# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_names, importances)]
# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
# Print out the feature and importances 
    
print(training_time, "\n", mae, "\n", accuracy, "\n", r2, "\n", feature_importances[:20])