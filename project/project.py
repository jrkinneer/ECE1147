import numpy as np
import tqdm
import csv

# data = np.loadtxt('Motor_Vehicle_Collisions_-_Crashes.csv')

# print(data[:2])

# file = open('Motor_Vehicle_Collisions_-_Crashes.csv')
file = csv.reader(open('U.S._Chronic_Disease_Indicators__CDI_.csv'))
file_out = csv.writer(open('test.csv', 'w'))
counter = 0
for row in file:
    print(row)
    file_out.writerow(row)
    counter += 1
    if counter >= 25:
        break
    
# w = csv.writer(open('test.csv'))
# counter = 0
# for i in file:
#     w.writerow(i)
#     counter += 1
#     if counter >= 25:
#         break