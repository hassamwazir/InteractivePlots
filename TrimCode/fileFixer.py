import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import StartEndSelector as SES 
from GetPeaksAndTroughs import GetPeaksAndTroughs


def Fix_time(kin_file_path, mp_file_path, plot=False):
    # Read kin file into a DataFrame
    kin_df = pd.read_csv(kin_file_path, sep=',', header=None)
    kin_df.columns = ['elev', 'shp', 'rie', 'elb', 'time']

    # Read mp file into a DataFrame
    mp_df = pd.read_csv(mp_file_path, sep=',', header=None)
    mp_df.columns = ['elev', 'shp', 'time', 'elb', 'rie']

    # rearrange columns in mp_df
    mp_df = mp_df[['elev', 'shp', 'rie', 'elb', 'time']]
    # add a column called "images" to mp_df which has the same valeus as "time" column + ".jpg" + date from kin_df

    # print(f'kin_df: {kin_df.head()}')

    # Convert datetime format in kin_df
    kin_df['time'] = pd.to_datetime(kin_df['time'], format='%m-%d-%y-%H-%M-%S-%f')

    # # convert time to YYYY-MM-DD-HH-MM-SS-MS format
    # kin_df['time'] = kin_df['time'].dt.strftime('%Y-%m-%d-%H-%M-%S-%f')

    # print(f'kin_df: {kin_df.head()}')

    # Separate date and time into two columns in kin_df
    kin_df['date'] = kin_df['time'].dt.date
    kin_df['time'] = kin_df['time'].dt.time
    
    # add a date column to mp_df with the same date as kin_df
    mp_df['date'] = kin_df['date'][0]

    # print(f'kin_df: {kin_df.head()}')
    # print(f'mp_df: {mp_df.head()}')

    # convert mp_df date to d m y format instead of y m d
    mp_df['date'] = pd.to_datetime(mp_df['date'], format='%Y-%m-%d')

    # print('date changed')
    # print(f'kin_df: {kin_df.head()}')
    # print(f'mp_df: {mp_df.head()}')

    mp_df['time'] = pd.to_datetime(mp_df['time'], format='%H-%M-%S-%f')\
    

    # add a column called "images" to mp_df which has the same valeus as "time" column + ".jpg" + date from kin_df
    # Generate the 'images' column
    mp_df['images'] = mp_df.apply(
        lambda row: '{:02d}-{:02d}-{:04d}-{:02d}-{:02d}-{:02d}-{:03d}.jpg'.format(
            row['date'].month % 100, row['date'].day, row['date'].year, row['time'].hour, row['time'].minute,
            row['time'].second, row['time'].microsecond // 1000), axis=1
    )

    # Convert datetime format in mp_df


    # Set the same hour in kin_df as in mp_df
    kin_df['time'] = kin_df['time'].apply(lambda x: x.replace(hour=mp_df['time'][0].hour))


    # Convert time to seconds with microseconds
    kin_df['time'] = kin_df['time'].apply(lambda x: x.hour * 3600 + x.minute * 60 + x.second + x.microsecond * 0.001 * 0.001)
    mp_df['time'] = mp_df['time'].apply(lambda x: x.hour * 3600 + x.minute * 60 + x.second + x.microsecond * 0.001 * 0.001)

    if plot:
        # Plot time vs elevation
        plt.plot(kin_df['time'], kin_df['elev'], label='kinect')
        plt.plot(mp_df['time'], mp_df['elev'], label='motion capture')
        plt.xlabel('time (s)')
        plt.ylabel('elevation (m)')
        plt.title('Elevation vs Time')
        plt.legend()
        plt.show()

    return kin_df, mp_df

# kin_file_path = "DataFolder/kinFiles/14/kin-elbrest-abd-add-06-04-23-07-17-44.txt"
# mp_file_path = "..", "DataFolder/mpFiles/elbrest-abd-add-06-04-2023-15-17-34/"

cwd = os.getcwd()
print(f'cwd: {cwd}')
# get one directory up from cwd
main_path = os.path.dirname(cwd)
print(f'main_path: {main_path}')

main_path = main_path.replace('\\', '/')
# print(f'cwd: {cwd}')

# mp_source_folder = main_path + "/DataFolder/mpFiles/elbrest-abd-add-06-04-2023-15-17-34/"
mp_source_folder = main_path + "/DataFolder/mpFiles/14/"
kin_source_folder = main_path + "/DataFolder/kinFiles/14/"

kin_csv_path = kin_source_folder + "/kin-elbrest-abd-add-06-04-23-07-17-44.txt"
mp_csv_path =  mp_source_folder + "/analysis/elbrest-abd-add-06-04-2023-15-17-34.csv"

kin_df_new, mp_df_new =  Fix_time(kin_csv_path, mp_csv_path, plot=False)

# print(mp_df_new.head())
# print()
# print(kin_df_new.head())
# print()

# get the time, elev, and images columns from mp_df_new as x, y, and images columns

# if mp_csv_path contains "abd-add" then get the time, elev, and images columns from mp_df_new as x, y, and images columns
if "abd-add" in mp_csv_path:
    data = pd.DataFrame({'x': mp_df_new['time'], 'y': mp_df_new['elev'], 'images': mp_df_new['images']})
elif "shp" in mp_csv_path:
    data = pd.DataFrame({'x': mp_df_new['time'], 'y': mp_df_new['shp'], 'images': mp_df_new['images']})
elif "rie" in mp_csv_path:
    data = pd.DataFrame({'x': mp_df_new['time'], 'y': mp_df_new['rie'], 'images': mp_df_new['images']})
elif "elb" in mp_csv_path:
    data = pd.DataFrame({'x': mp_df_new['time'], 'y': mp_df_new['elb'], 'images': mp_df_new['images']})


# Assuming your signal DataFrame is called 'data' with 'x' and 'y' columns

# print(f'data: {data.head()}')

# mp_csv_path = "D:/InteractivePlots/DataFolder/mpFiles/elbrest-abd-add-06-04-2023-15-17-34/"
# mp_src_folder = "D:/InteractivePlots/DataFolder/mpFiles/elbrest-abd-add-06-04-2023-15-17-34/"

# add "D:/InteractivePlots/" to data['images'] column
# data['images'] = data['images'].apply(lambda x: mp_csv_path + x)

# cwd = os.getcwd()
# cwd = cwd.replace('\\', '/')
# print(f'cwd: {cwd}')
# print(f'mp_csv_path: {mp_csv_path}')

# iterate through all folders in mp_sorce_folder
for folder in os.listdir(mp_source_folder):
    print(f'folder: {folder}')
    # get the path of the folder
    folder_path = mp_source_folder + folder
    print(f'folder_path: {folder_path}')
    # iterate through all files in the folder
    for file in os.listdir(folder_path):
        print(f'file: {file}')
        # get the path of the file
        file_path = folder_path + "/" + file
        print(f'file_path: {file_path}')


# peaks_troughs = GetPeaksAndTroughs(data, mp_csv_path, source_folder = mp_source_folder, prox_threshold=0)
# peaks_troughs.run()

