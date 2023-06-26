# read csv file in a directory

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from BlandAltman import bland_altman_plot

# get the current working directory
cwd = os.getcwd()
# print(f'cwd: {cwd}')
# get one directory up from cwd
main_path = os.path.dirname(cwd)
print(f'main_path: {main_path}')

main_path = main_path.replace('\\', '/')
# print(f'cwd: {cwd}')

# csv_path = main_path + "/DataFolder/mpFiles/14/elbrest-abd-add-06-04-2023-15-17-34/analysis/fixedTime/"
csv_path = main_path + "/DataFolder/mpFiles/14/elbrest-abd-add-06-04-2023-15-17-34/analysis/AlignedAndResampled"
file1_path = csv_path + "/kin.csv"
file2_path = csv_path + "/mp.csv"
print(f'csv_path: {csv_path}')
# offset = -0.8
# offset = 0

# read all csv files in the directory
for file in os.listdir(csv_path):
    # print(f'file: {file}')
    # get the path of the file
    file_path = csv_path + "/" + file
    print(f'file_path: {file_path}')

    # read the csv file
    df = pd.read_csv(file_path)
    
    print(f'df: {df.head()}')

    # plot time vs elev as a scatter plot
    plt.scatter(df['x'], df['y'])
plt.show()


import matplotlib.pyplot as plt
import numpy as np


# load file1
df1 = pd.read_csv(file1_path)
# only keep the x, and y columns
df1 = df1[['y']]
# load file2
df2 = pd.read_csv(file2_path)
# only keep the x, and y columns
df2 = df2[['y']]


# plot bland altman plot
bland_altman_plot(df1, df2, "Kinect vs. Mediapipe Bland-Altman Plot")

