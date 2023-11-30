from random_forest import rf_fatalities
from random_forest_injuries import rf_injuries
import numpy as np
import pandas as pd

T_list = [2, 10 , 25, 100]

#14 is the sqrt of the feature space (205)
depth_list = [3, 5, 10, 14, 25, 100, 205]

rows = [str(t) for t in T_list]
columns = [str(d) for d in depth_list]

training_times = np.zeros((len(T_list), len(depth_list)))
testing_times = np.zeros((len(T_list), len(depth_list)))
accuracies = np.zeros((len(T_list), len(depth_list)))
mae = np.zeros((len(T_list), len(depth_list)))
important_features = np.empty((len(T_list), len(depth_list)), dtype=object)

training_times_injuries = np.zeros((len(T_list), len(depth_list)))
testing_times_injuries = np.zeros((len(T_list), len(depth_list)))
accuracies_injuries = np.zeros((len(T_list), len(depth_list)))
mae_injuries = np.zeros((len(T_list), len(depth_list)))
important_features_injuries = np.empty((len(T_list), len(depth_list)), dtype=object)

for i, T in enumerate(T_list):
    for j, depth in enumerate(depth_list):
        #fatalities
        print("fatality rf")
        train, test, mae_, accuracy, features = rf_fatalities(T, depth)
        training_times[i][j] = train
        testing_times[i][j] = test
        mae[i][j] = mae_
        accuracies[i][j] = accuracy
        important_features[i][j] = features
        
        #injuries
        print("injury rf")
        train, test, mae_, accuracy, features = rf_injuries(T, depth)
        training_times_injuries[i][j] = train
        testing_times_injuries[i][j] = test
        mae_injuries[i][j] = mae_
        accuracies_injuries[i][j] = accuracy
        important_features_injuries[i][j] = features
        
#save data to csv
basefile_name = "./results_data/fatalities_"
DF = pd.DataFrame(training_times, columns=columns, index=rows)
DF.to_csv(basefile_name+"training_times.csv")

DF = pd.DataFrame(testing_times, columns=columns, index=rows)
DF.to_csv(basefile_name+"testing_times.csv")

DF = pd.DataFrame(mae, columns=columns, index=rows)
DF.to_csv(basefile_name+"mae.csv")

DF = pd.DataFrame(accuracies, columns=columns, index=rows)
DF.to_csv(basefile_name+"accuracies.csv")

DF = pd.DataFrame(important_features, columns=columns, index=rows)
DF.to_csv(basefile_name+"features.txt")

basefile_name = "./results_data/injuries_"
DF = pd.DataFrame(training_times_injuries, columns=columns, index=rows)
DF.to_csv(basefile_name+"training_times_injuries.csv")

DF = pd.DataFrame(testing_times_injuries, columns=columns, index=rows)
DF.to_csv(basefile_name+"testing_times_injuries.csv")

DF = pd.DataFrame(mae_injuries, columns=columns, index=rows)
DF.to_csv(basefile_name+"mae_injuries.csv")

DF = pd.DataFrame(accuracies_injuries, columns=columns, index=rows)
DF.to_csv(basefile_name+"accuracies_injuries.csv")

DF = pd.DataFrame(important_features_injuries, columns=columns, index=rows)
DF.to_csv(basefile_name+"features_injuries.txt")