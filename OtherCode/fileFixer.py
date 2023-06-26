import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import StartEndSelector as SES 


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

    # Convert datetime format in kin_df
    kin_df['time'] = pd.to_datetime(kin_df['time'], format='%y-%m-%d-%H-%M-%S-%f')
    

    # Separate date and time into two columns in kin_df
    kin_df['date'] = kin_df['time'].dt.date
    kin_df['time'] = kin_df['time'].dt.time
    
    # add a date column to mp_df with the same date as kin_df
    mp_df['date'] = kin_df['date'][0]

    # convert mp_df date to d m y format instead of y m d
    mp_df['date'] = pd.to_datetime(mp_df['date'], format='%Y-%m-%d')

    mp_df['time'] = pd.to_datetime(mp_df['time'], format='%H-%M-%S-%f')\
    

    # add a column called "images" to mp_df which has the same valeus as "time" column + ".jpg" + date from kin_df
    # Generate the 'images' column
    mp_df['images'] = mp_df.apply(lambda row: '{:02d}-{:02d}-{}-{:02d}-{:02d}-{:02d}-{:03d}.jpg'.format(row['date'].year % 100, row['date'].month, row['date'].day, row['time'].hour, row['time'].minute, row['time'].second, row['time'].microsecond // 1000), axis=1)

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

kin_file_path = os.path.join(os.getcwd(), "DataFolder/kinFiles/14/kin-elbrest-abd-add-06-04-23-07-17-44.txt")
mp_file_path = os.path.join(os.getcwd(), "DataFolder/mpFiles/elbrest-abd-add-06-04-2023-15-17-34/")

mp_img_path = os.path.join(os.getcwd(), "DataFolder/mpFiles/elbrest-abd-add-06-04-2023-15-17-34/images/")

kin_csv_path = os.path.join(os.getcwd(), "DataFolder/kinFiles/14/kin-elbrest-abd-add-06-04-23-07-17-44.txt")
mp_csv_path = os.path.join(os.getcwd(), "DataFolder/mpFiles/elbrest-abd-add-06-04-2023-15-17-34/analysis/elbrest-abd-add-06-04-2023-15-17-34.csv")

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



from GetPeaksAndTroughs import GetPeaksAndTroughs
# Assuming your signal DataFrame is called 'data' with 'x' and 'y' columns

peaks_troughs = GetPeaksAndTroughs(data, mp_file_path)
# peaks_troughs.peak_threshold = 0.5  # Set the peak threshold
# peaks_troughs.trough_threshold = -0.5  # Set the trough threshold
peaks_troughs.run()


# # =============================================================================
# print(kin_df_new['time'].iloc[0])
# print(kin_df_new['time'].iloc[-1])
# # new data frame with time and elev columns named as x and y
# data = pd.DataFrame({'x': kin_df_new['time'], 'y': kin_df_new['elev']})
# # data.head()

# plot_selector = SES.PlotSelector(data)
# plot_selector.show()
