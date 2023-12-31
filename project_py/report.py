import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy

T_list = [2, 10 , 25, 100]
feature_subset_size = [3, 5, 10, 14, 25, 100, 205]

# data = pd.read_csv("./results_data/fatalities_training_times.csv")
# data_injuries = pd.read_csv("./results_data/injuries_training_times_injuries.csv")

# for i, t in enumerate(T_list):
#     y = data.iloc[i]
#     y_2 = data_injuries.iloc[i]
#     plt.plot(feature_subset_size, y[1:], label="fatalities")
#     plt.plot(feature_subset_size, y_2[1:], label="injuries")
#     plt.title("Training time for forest size T = " + str(t))
#     plt.xlabel("max features")
#     plt.ylabel("training time (seconds)")
#     plt.legend()
    
#     plt.savefig("./graphs/training_time_forest_size_"+str(t))
#     plt.close()
    
# for i, f in enumerate(feature_subset_size):
#     y = data[str(f)]
#     y_2 = data_injuries[str(f)]
    
#     plt.plot(T_list, y, label="fatalites")
#     plt.plot(T_list, y_2, label="injuries")

#     plt.title("Training time for maximum features  = " + str(f))
#     plt.xlabel("forest size")
#     plt.ylabel("training time (seconds)")
#     plt.legend()
#     plt.savefig("./graphs/training_time_maximum_features_"+str(f))
#     plt.close()
    
#accuracy
# data = pd.read_csv("./results_data/fatalities_accuracies.csv")
# data_injuries = pd.read_csv("./results_data/injuries_accuracies_injuries.csv")

# for i, t in enumerate(T_list):
#     y = data.iloc[i]
#     y_2 = data_injuries.iloc[i]
#     plt.plot(feature_subset_size, y[1:], label="fatalities")
#     plt.plot(feature_subset_size, y_2[1:], label="injuries")
#     plt.title("Accuracies for forest size T = " + str(t))
#     plt.xlabel("max features")
#     plt.ylabel("training time (seconds)")
#     plt.legend()
    
#     plt.savefig("./graphs/accuracy_forest_size_"+str(t))
#     plt.close()
    
# for i, f in enumerate(feature_subset_size):
#     y = data[str(f)]
#     y_2 = data_injuries[str(f)]
    
#     plt.plot(T_list, y, label="fatalites")
#     plt.plot(T_list, y_2, label="injuries")

#     plt.title("Accuracies for maximum features  = " + str(f))
#     plt.xlabel("forest size")
#     plt.ylabel("training time (seconds)")
#     plt.legend()
#     plt.savefig("./graphs/accuracy_maximum_features_"+str(f))
#     plt.close()
    
# #MAE
# data = pd.read_csv("./results_data/fatalities_mae.csv")
# data_injuries = pd.read_csv("./results_data/injuries_mae_injuries.csv")

# for i, t in enumerate(T_list):
#     y = data.iloc[i]
#     y_2 = data_injuries.iloc[i]
#     plt.plot(feature_subset_size, y[1:], label="fatalities")
#     plt.plot(feature_subset_size, y_2[1:], label="injuries")
#     plt.title("Mean Absolute Error (MAE) for forest size T = " + str(t))
#     plt.xlabel("max features")
#     plt.ylabel("training time (seconds)")
#     plt.legend()
    
#     plt.savefig("./graphs/mae_forest_size_"+str(t))
#     plt.close()
    
# for i, f in enumerate(feature_subset_size):
#     y = data[str(f)]
#     y_2 = data_injuries[str(f)]
    
#     plt.plot(T_list, y, label="fatalites")
#     plt.plot(T_list, y_2, label="injuries")

#     plt.title("Mean Absolute Error (MAE) for maximum features  = " + str(f))
#     plt.xlabel("forest size")
#     plt.ylabel("training time (seconds)")
#     plt.legend()
#     plt.savefig("./graphs/mae_maximum_features_"+str(f))
#     plt.close()
    
#r2
data = pd.read_csv("./results_data_2/fatalities_r2.csv")
data_injuries = pd.read_csv("./results_data_2/injuries_r2.csv")

for i, t in enumerate(T_list):
    y = data.iloc[i]
    y_2 = data_injuries.iloc[i]
    plt.plot(feature_subset_size, y[1:], label="fatalities")
    plt.plot(feature_subset_size, y_2[1:], label="injuries")
    plt.title("R^2 for forest size T = " + str(t))
    plt.xlabel("max features")
    plt.ylabel("training time (seconds)")
    plt.legend()
    
    plt.savefig("./graphs/r2_forest_size_"+str(t))
    plt.close()
    
for i, f in enumerate(feature_subset_size):
    y = data[str(f)]
    y_2 = data_injuries[str(f)]
    
    plt.plot(T_list, y, label="fatalites")
    plt.plot(T_list, y_2, label="injuries")

    plt.title("R^2 for maximum features  = " + str(f))
    plt.xlabel("forest size")
    plt.ylabel("training time (seconds)")
    plt.legend()
    plt.savefig("./graphs/r2_maximum_features_"+str(f))
    plt.close()
    