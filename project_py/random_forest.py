import numpy as np
import sklearn as sk
from sklearn.model_selection import train_test_split
import pandas as pd

#get raw data
raw_data = pd.read_csv("data.csv", delimiter=',', on_bad_lines='skip')
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
train_X, test_X, trainy, testy = train_test_split(features, y, test_size=.2, random_state=42)

print('Training Features Shape:', train_X.shape)
print('Training Y Shape:', trainy.shape)
print('Testing Features Shape:', test_X.shape)
print('Testing Y Shape:', testy.shape)
# Training Features Shape: (1287588, 205)
# Training Y Shape: (1287588,)
# Testing Features Shape: (321897, 205)
# Testing Y Shape: (321897,)
