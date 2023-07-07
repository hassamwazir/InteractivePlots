import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# read the csv data from folder "TempDistanceData"

# read all files in the folder and return a list of dataframes
def read_csv_data():
    import os
    import glob
    os.chdir("TempDistanceData")
    # get all the csv files in the folder
    extension = 'txt'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    return all_filenames

all_filenames = read_csv_data()

# read file names from list and create a list of dataframes
def create_dataframes(dataFrames):
    df_list = []
    for file in dataFrames:
        df_list.append(pd.read_csv(file, sep=',', header=None))
        df_list[-1].columns = ['time', 'SSID', 'distance', 'RSSI', 'est_rtt', 'rtt_sum', 'avg_raw_rtt', 'raw_dist']
        file = file.split("_")
        # createt a new column called "ground_truth"
        df_list[-1]['ground_truth'] = f'{file[-2]}.{file[-1][:-5]}'
        # add header to the dataframe
    return df_list

df_list = create_dataframes(all_filenames)

print(df_list[2])

# if a file has name "07_07_2023_15_08_52_LAB_offset_13_3m.txt", get "13_3" from it

# filename = "07_07_2023_15_08_52_LAB_offset_13_3m.txt"
# filename = filename.split("_")
# print(filename[-2:])
# print(f'{filename[-2]}.{filename[-1][:-5]}')

# reverse the dflist
df_list.reverse()


# plot the column "distance" against "groundtruth"
def plot_distance_groundtruth(df_list):
    # create figure
    ground_truth = []
    fig, ax = plt.subplots()
    for df in df_list:
        # convert dataframe column to float
        df['distance'] = df['distance'].astype(float)
        df['ground_truth'] = df['ground_truth'].astype(float)
        

        # plot the distance column
        ax.plot(df['ground_truth'], df['distance'], 'o')
        ax.axhline(df['ground_truth'][0], color='r', linestyle='--')
        ax.axvline(df['ground_truth'][0], color='r', linestyle='--')

        # save ground truth value in a np array
        ground_truth.append(df['ground_truth'][0])
    # plot ground_truth values as a black line
    ax.plot(ground_truth, ground_truth, color='black')
    ax.plot()
    plt.show()

plot_distance_groundtruth(df_list)

    



