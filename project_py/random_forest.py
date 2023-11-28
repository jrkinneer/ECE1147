import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import time
from math import sqrt
#get raw data
file_path = "./project_data/data.csv"
raw_data = pd.read_csv(file_path, delimiter=',', on_bad_lines='skip')
# (1609485, 10)
print("raw data shape: ", raw_data.shape)

#one hot encoding
features = pd.get_dummies(raw_data)
print("one hot encoding shape: ", features.shape)
#(1609485, 206)

# print("\n")
# f = open("features.txt", "w")
# i = 0
# for col in features.columns:
#     try:
#         f.write(col)
#         f.write("\n")
#         i+=1
#     except:
#         print("error for feature")
# f.close()
# print("features = ", i)

#isolate y variable
y = np.array(features['NUMBER OF PERSONS KILLED'])

#remove y variable from feature data
features = features.drop('NUMBER OF PERSONS KILLED', axis=1)

feature_names = list(features.columns)

features = np.array(features)

#get training and testing data, and training and testing labels
train_X, test_X, train_y, test_y = train_test_split(features, y, test_size=.2, random_state=42)

print('Training Features Shape:', train_X.shape)
print('Training Y Shape:', train_y.shape)
print('Testing Features Shape:', test_X.shape)
print('Testing Y Shape:', test_y.shape)
print(np.unique(train_y))
print(np.unique(test_y))
# Training Features Shape: (1287588, 205)
# Training Y Shape: (1287588,)
# Testing Features Shape: (321897, 205)
# Testing Y Shape: (321897,)

# #establish baseline
# baseline_predictions = test_X[:, feature_names.index('NUMBER OF PERSONS KILLED')]
# print("baseline established")

# #baseline errors
# baseline_errors = abs(baseline_predictions - test_y)
# print('average baseline error: ', round(np.mean(baseline_errors), 2))

#instantiate with T decision trees
T = 25
features_per_tree = int(sqrt(train_X.shape[1]))
rf = RandomForestRegressor(n_estimators=T, random_state=42, max_depth=features_per_tree, verbose=2)
print("forest instantiated with ", T , " trees")

#train the model
start = time.time()
rf.fit(train_X, train_y)
end = time.time()
print("model training finished, time elapsed = ", end - start)

#use the test data
start = time.time()
predictions = rf.predict(test_X)
end = time.time()
print("model prediction finished, time elapsed = ", end - start)

#testing errors
errors = abs(predictions - test_y)
print("Mean absolute error: ", round(np.mean(errors), 2))

mae = sum(errors)/test_y.shape[0]

accuracy = 100 - ((mae/np.max(test_y)) * 100)

print("accuracy = ", accuracy)

#get most important features]
importances = list(rf.feature_importances_)
# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_names, importances)]
# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
# Print out the feature and importances 
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]