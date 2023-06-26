import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import StartEndSelector as SES 
from GetPeaksAndTroughs import GetPeaksAndTroughs


import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from tkinter import filedialog
import numpy as np
import re
import createInteractivePlot as cip
from GetPeaksAndTroughs import GetPeaksAndTroughs
import os
import pandas as pd

screen_width = 640
screen_height = 480
padx = 50

default_dir_input = None  # Declare folder_input as a global variable
file1_input = None
file2_input = None
file1_path = None
file2_path = None

def plot_selected_data(selected_file):
    # to be fille
    return

def select_path(input_field, is_folder, file=""):
    dialog_func = filedialog.askdirectory if is_folder else filedialog.askopenfilename
    selected_path = dialog_func(initialdir="", title="Select a folder") if is_folder else dialog_func(title="Select a file", filetypes=(("Numpy files", "*.npy"),("Text files", "*.txt"), ("Text files", "*.csv"), ("all files", "*.*")))
    
    if selected_path:
        input_field.delete(0, tk.END)
        input_field.insert(0, selected_path)
        # update the global variables
        if is_folder:
            global default_dir_input
            default_dir_input = selected_path
        else:
            global file1_path, file2_path
            # if input_field is for file 1
            if file == "file1":
                file1_path = selected_path
            # if input_field is for file 2
            elif file == "file2":
                file2_path = selected_path

def Fix_time(kin_file_path, mp_file_path, plot=False):
    # Read kin file into a DataFrame
    kin_df = pd.read_csv(kin_file_path, sep=',', header=None)
    kin_df.columns = ['elev', 'shp', 'rie', 'elb', 'time']

    # Read mp file into a DataFrame
    mp_df = pd.read_csv(mp_file_path, sep=',', header=None)
    mp_df.columns = ['elev', 'shp', 'time', 'elb', 'rie']

    # rearrange columns in mp_df
    mp_df = mp_df[['elev', 'shp', 'rie', 'elb', 'time']]

    # Convert datetime format in kin_df
    kin_df['time'] = pd.to_datetime(kin_df['time'], format='%m-%d-%y-%H-%M-%S-%f')

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
    mp_df['images'] = mp_df.apply(
        lambda row: '{:02d}-{:02d}-{:04d}-{:02d}-{:02d}-{:02d}-{:03d}.jpg'.format(
            row['date'].year % 100, row['date'].month, row['date'].year, row['time'].hour, row['time'].minute,
            row['time'].second, row['time'].microsecond // 1000), axis=1
    )

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

def update_input_field(input_filed, value):
    input_filed.delete(0, tk.END)  # Clear existing text in the input field
    input_filed.insert(0, value)  # Insert selected folder address


# function to read a text file to get the default directory
def get_default_params():
    default_dir=''
    file_1=''
    file_2=''

    defaultDataDirectory_path = os.path.join(os.getcwd(), 'DefaultDataDirectory.txt')

    with open(defaultDataDirectory_path, 'r') as f:
        for line in f:
            match = re.match(r'(DEFAULT_DIR|FILE_1|FILE_2)=(.*)', line)
            if match:
                param_type, value = match.groups()
                value = value.strip()
                
                if param_type == 'DEFAULT_DIR':
                    default_dir = value
                elif param_type == 'FILE_1':
                    file_1 = value
                elif param_type == 'FILE_2':
                    file_2 = value
    
    return default_dir, file_1, file_2


def create_gui():
    global default_dir_input, file1_path, file2_path
    root = tk.Tk()
    root.title("My GUI")
    root.geometry(f"{screen_width}x{screen_height}")

    # Configure row spacing
    root.grid_rowconfigure([0, 1, 2, 3, 4], minsize=40)  # Add spacing after rows
    root.grid_columnconfigure(0, minsize=0)  # Add spacing after cols

    # Create labels and input fields
    # ROW 0
    default_dir_label = ttk.Label(root, text="Data Folder:")
    default_dir_label.grid(row=0, column=0, sticky="w", padx=padx)

    default_dir_input = ttk.Entry(root)
    default_dir_input.grid(row=0, column=1)

    default_dir_button = ttk.Button(root, text="Select Folder", command=lambda: select_path(default_dir_input, True))
    default_dir_button.grid(row=0, column=2, padx=5)

    # ROW 1
    file1_label = ttk.Label(root, text="Data File 1:")
    file1_label.grid(row=1, column=0, sticky="w", padx=padx)

    file1_var = tk.StringVar()
    file1_input = ttk.Entry(root, textvariable=file1_var)
    file1_input.grid(row=1, column=1)

    file1_button = ttk.Button(root, text="Select File 1", command=lambda: select_path(file1_input, False, "file1"))
    file1_button.grid(row=1, column=2, padx=5)

    # ROW 2
    file2_label = ttk.Label(root, text="Data File 2:")
    file2_label.grid(row=2, column=0, sticky="w", padx=padx)

    file2_var = tk.StringVar()
    file2_input = ttk.Entry(root, textvariable=file2_var)
    file2_input.grid(row=2, column=1)

    file2_button = ttk.Button(root, text="Select File 2", command=lambda: select_path(file2_input, False, "file2"))
    file2_button.grid(row=2, column=2, padx=5)

    # ROW 3
    # Create radio buttons
    selected_file_var = tk.IntVar(value=1)
    file1_radio = ttk.Radiobutton(root, text="File 1", variable=selected_file_var, value=1)
    file1_radio.grid(row=3, column=0, sticky="w", padx=padx)

    file2_radio = ttk.Radiobutton(root, text="File 2", variable=selected_file_var, value=2)
    file2_radio.grid(row=3, column=1, sticky="w")

    file3_radio = ttk.Radiobutton(root, text="File 1 and 2", variable=selected_file_var, value=3)
    file3_radio.grid(row=3, column=2, sticky="w")
    
    # ROW 5
    # Create plot button
    plot_button = ttk.Button(root, text="Plot", command=lambda: plot_selected_data(selected_file_var.get()))
    plot_button.grid(row=5, column=1)

    # if the default directory is not set, then set it to the current directory
    default_dir, file1_path, file2_path = get_default_params()
    update_input_field(default_dir_input, default_dir)
    update_input_field(file1_input, file1_path)
    update_input_field(file2_input, file2_path)

    # stop the program when the window is closed
    root.protocol("WM_DELETE_WINDOW", root.quit)

    root.mainloop()

create_gui()


























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

