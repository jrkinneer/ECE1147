from random_forest import rf_fatalities
from random_forest_injuries import rf_injuries
import numpy as np
from tqdm import tqdm
import pandas as pd

T_list = [1, 10 , 25, 100]

#14 is the sqrt of the feature space (205)
feature_subset_size = [3, 5, 10, 14, 25, 100, 205]

rows = [str(t) for t in T_list]
columns = [str(f) for f in feature_subset_size]

training_times = np.zeros((len(T_list), len(feature_subset_size)))
testing_times = np.zeros((len(T_list), len(feature_subset_size)))
accuracies = np.zeros((len(T_list), len(feature_subset_size)))
mae = np.zeros((len(T_list), len(feature_subset_size)))
important_features = np.empty((len(T_list), len(feature_subset_size)), dtype=object)

training_times_injuries = np.zeros((len(T_list), len(feature_subset_size)))
testing_times_injuries = np.zeros((len(T_list), len(feature_subset_size)))
accuracies_injuries = np.zeros((len(T_list), len(feature_subset_size)))
mae_injuries = np.zeros((len(T_list), len(feature_subset_size)))
important_features_injuries = np.empty((len(T_list), len(feature_subset_size)), dtype=object)

for i, T in tqdm(enumerate(T_list)):
    for j, feature_subset in enumerate(feature_subset_size):
        #fatalities
        train, test, mae_, accuracy, features = rf_fatalities(T, feature_subset)
        training_times[i][j] = train
        testing_times[i][j] = test
        mae[i][j] = mae_
        accuracies[i][j] = accuracy
        important_features[i][j] = features
        
        #injuries
        train, test, mae_, accuracy, features = rf_injuries(T, feature_subset)
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