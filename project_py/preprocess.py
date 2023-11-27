import pandas as pd
N = 40

raw_data = pd.read_csv("data.csv", delimiter=',', on_bad_lines='skip')

vehicle_one_types = raw_data["VEHICLE TYPE CODE 1"].value_counts()
n_most_common_values = vehicle_one_types.head(N).index
for a in n_most_common_values:
    print(a)
print("\n")
vehicle_two_types = raw_data["VEHICLE TYPE CODE 2"].value_counts()
n_most_common_values = vehicle_two_types.head(N).index
for a in n_most_common_values:
    print(a)