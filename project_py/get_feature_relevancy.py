import pandas as pd
import ast
import matplotlib.pyplot as plt

df = pd.read_csv("./results_data/fatalities_features.txt")
feature_dict = {
    
}
bad_str = ["CONTRIBUTING FACTOR VEHICLE 1_", "CONTRIBUTING FACTOR VEHICLE 2_", "VEHICLE TYPE CODE 1_", "VEHICLE TYPE CODE 2_"]
test = df.to_numpy()
test = test[1:, 1:]

for l in test:
    for x in l:
        cell_list = ast.literal_eval(x)
        for tup in cell_list:
            feature_keys = feature_dict.keys()
            
            if tup[1] > 0:
                val = tup[0]
                for s in bad_str:
                    if tup[0].startswith(s):
                        val = tup[0][len(s):]
                        break
                if val not in feature_keys:
                    feature_dict[val] = tup[1]
                else:
                    feature_dict[val] = feature_dict[val] + round(tup[1], ndigits=2)

feature_dict = dict(sorted(feature_dict.items(), key=lambda item: item[1], reverse=True))
keys = list(feature_dict.keys())
vals = list(feature_dict.values())
plt.rc('xtick', labelsize = 8)
plt.bar(keys, vals, width=.4)
plt.xticks(range(len(keys)), keys, rotation = -90)
plt.xlabel("Features", fontsize=18)
plt.ylabel("Importance")
plt.title("Total feature importance for Fatality Random Forest")

plt.subplots_adjust(bottom=.5)
plt.savefig("./graphs/fatalities_features.png")
plt.close()

df = pd.read_csv("./results_data/injuries_features_injuries.txt")
feature_dict = {
    
}
bad_str = ["CONTRIBUTING FACTOR VEHICLE 1_", "CONTRIBUTING FACTOR VEHICLE 2_", "VEHICLE TYPE CODE 1_", "VEHICLE TYPE CODE 2_"]
test = df.to_numpy()
test = test[1:, 1:]

for l in test:
    for x in l:
        cell_list = ast.literal_eval(x)
        for tup in cell_list:
            feature_keys = feature_dict.keys()
            
            if tup[1] > 0:
                val = tup[0]
                for s in bad_str:
                    if tup[0].startswith(s):
                        val = tup[0][len(s):]
                        break
                if val not in feature_keys:
                    feature_dict[val] = tup[1]
                else:
                    feature_dict[val] = feature_dict[val] + round(tup[1], ndigits=2)

feature_dict = dict(sorted(feature_dict.items(), key=lambda item: item[1], reverse=True))
keys = list(feature_dict.keys())
vals = list(feature_dict.values())
plt.rc('xtick', labelsize = 8)
plt.bar(keys, vals, width=.4)
plt.xticks(range(len(keys)), keys, rotation = -90)
plt.xlabel("Features", fontsize=18)
plt.ylabel("Importance")
plt.title("Total feature importance for Injury Random Forest")

plt.subplots_adjust(bottom=.5)
plt.savefig("./graphs/injuries_features.png")