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
from Utils import resample_sine_waves, minimize_offset

screen_width = 640
screen_height = 480
padx = 50

default_dir_input = None  # Declare folder_input as a global variable
default_dir = None

def trim_selected_data(default_dir):
    print(f'PlotSelected')
    print(f'default_dir: {default_dir}')

    # find the .txt file path in the default directory "default_dir"
    kin_file_path = ''
    mp_file_path = ''
    for file in os.listdir(default_dir + "/analysis"):
        if file.endswith(".txt"):
            kin_file_path = default_dir + "/analysis/" + file
        elif file.endswith(".csv"):
            mp_file_path = default_dir + "/analysis/" + file
    
    print(f'kin_file_path: {kin_file_path}')
    print(f'mp_file_path: {mp_file_path}')

    # split the mp_file_path along the "/" and take the last element
    file_name = mp_file_path.split("/")[-1][:-4]

    print(f'mp_file_name: {file_name}')

    kin_df_new, mp_df_new =  Fix_time(kin_file_path, mp_file_path, plot=False)

    print()
    print(f'mp_df_new: {mp_df_new.head()}')
    print()
    print(f'kin_df_new: {kin_df_new.head()}')
    print()

    kin_dir, mp_dir = SaveData(kin_df_new, mp_df_new, default_dir, file_name=file_name)

    # create a new directory called "trimmed" if it doesn't exist
    new_dir = default_dir + "/analysis/trimmed"
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    # open all files in dir one by one and run GetPeaksAndTroughs on them
    fixedTime_dir = default_dir + "/analysis/fixedTime"
    for file in os.listdir(fixedTime_dir):
        if file.endswith(".csv"):

            print(f'file: {file}')
            file_path = fixedTime_dir + "/" + file
            print(f'file_path: {file_path}')
            df = pd.read_csv(file_path)
            print(f'df: {df.head()}')
            # change the column names time and elev to x and y
            df = df.rename(columns={"time": "x", "elev": "y"})
            print(f'default_dir: {default_dir}')
            peaks_troughs = GetPeaksAndTroughs(df, file_path, source_folder = default_dir, prox_threshold=0, save_images_bool = True)
            peaks_troughs.run()


def SaveData(kin_df, mp_df, directory="", file_name=""):
    # create a new folder in the directory called "fixedTime" if it doesn't exist
    new_dir = directory + "/analysis/fixedTime/"
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    kin_file_name = "kin"
    mp_file_name = "mp"
    if file_name != "":
        kin_file_name = "kin-" + file_name
        mp_file_name = "mp-" + file_name
    
    kin_dir = new_dir  + kin_file_name + ".csv"
    mp_dir = new_dir  + mp_file_name + ".csv"

    print(f'kin_dir: {kin_dir}')
    print(f'mp_dir: {mp_dir}')

    # save the dataframes in the new_dir
    kin_df.to_csv(kin_dir, sep=',', index=False)
    mp_df.to_csv(mp_dir, sep=',', index=False)

    print('Data saved successfully.')

    return kin_dir, mp_dir

def AlignData(default_dir, plot=False):
    # check if a folder called "trimmed" exists in the default directory
    new_dir = default_dir + "/analysis/trimmed"
    if os.path.exists(new_dir):
        # find the files in the trimmed folder
        kin_file_path = ''
        mp_file_path = ''
        for file in os.listdir(new_dir):
            if file == "kin.csv":
                kin_file_path = new_dir + "/" + file
            elif file == "mp.csv":
                mp_file_path = new_dir + "/" + file

        # create a new folder called "AlignedAndResampled" if it doesn't exist
        aligned_dir = default_dir + "/analysis/AlignedAndResampled"
        if not os.path.exists(aligned_dir):
            os.makedirs(aligned_dir)
        
        # get the dataframes from the trimmed folder
        kin_df = pd.read_csv(kin_file_path)
        mp_df = pd.read_csv(mp_file_path)
        # resample the data and then align it
        kin_df_new, mp_df_new = resample_sine_waves(kin_df, mp_df)
        kin_df_new, mp_df_new = minimize_offset(kin_df_new, mp_df_new)

        # save the dataframes in the aligned folder
        kin_df_new_path = aligned_dir + "/kin.csv"
        mp_df_new_path  = aligned_dir + "/mp.csv"

        # save the dataframes in the aligned folder
        kin_df_new.to_csv(kin_df_new_path, sep=',', index=False)
        mp_df_new.to_csv(mp_df_new_path, sep=',', index=False)

    else:
        print('No trimmed folder found. Please run the "Trim Data" function first.')



def select_path(input_field, is_folder, file=""):
    dialog_func = filedialog.askdirectory if is_folder else filedialog.askopenfilename
    selected_path = dialog_func(initialdir="", title="Select a folder") if is_folder else dialog_func(title="Select a file", filetypes=(("Numpy files", "*.npy"),("Text files", "*.txt"), ("Text files", "*.csv"), ("all files", "*.*")))
    
    if selected_path:
        input_field.delete(0, tk.END)
        input_field.insert(0, selected_path)
        # update the global variable
        global default_dir
        default_dir = selected_path

def update_input_field(input_field, value):
    input_field.delete(0, tk.END)  # Clear existing text in the input field
    input_field.insert(0, value)  # Insert selected folder address

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
            row['date'].month % 100, row['date'].day, row['date'].year, row['time'].hour, row['time'].minute,
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

# function to read a text file to get the default directory
def get_default_params():
    default_dir=''
    file_1=''
    file_2=''

    with open('DefaultDataDirectory.txt', 'r') as f:
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
    global default_dir_input, default_dir, file1_path, file2_path
    root = tk.Tk()
    root.title("Fix Time")
    root.geometry(f"{screen_width}x{screen_height}")

    # Configure row spacing
    root.grid_rowconfigure([0, 1, 2, 3, 4], minsize=40)  # Add spacing after rows
    root.grid_columnconfigure(0, minsize=0)  # Add spacing after cols

    # if the default directory is not set, then set it to the current directory
    default_dir, file1_path, file2_path = get_default_params()
    if default_dir == '':
        # get current directory
        default_dir = os.path.dirname(os.getcwd())

    # Create labels and input fields
    # ROW 0
    default_dir_label = ttk.Label(root, text="Data Folder:")
    default_dir_label.grid(row=0, column=0, sticky="w", padx=padx)

    default_dir_input = ttk.Entry(root)
    default_dir_input.grid(row=0, column=1)

    default_dir_button = ttk.Button(root, text="Select Folder", command=lambda: select_path(default_dir_input, True))
    default_dir_button.grid(row=0, column=2, padx=5)
    
    # ROW 5
    # Create plot button
    plot_button = ttk.Button(root, text="Trim Data", command=lambda: trim_selected_data(default_dir))
    plot_button.grid(row=5, column=1)

    # ROW 6
    align_button = ttk.Button(root, text="Align Data", command=lambda: AlignData(default_dir))
    align_button.grid(row=6, column=1)

    update_input_field(default_dir_input, default_dir)

    # stop the program when the window is closed
    root.protocol("WM_DELETE_WINDOW", root.quit)

    root.mainloop()

create_gui()
