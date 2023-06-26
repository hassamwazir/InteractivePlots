import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from tkinter import filedialog
import numpy as np
import re
import createInteractivePlot as cip

screen_width = 640
screen_height = 480
padx = 50

default_dir_input = None  # Declare folder_input as a global variable
file1_input = None
file2_input = None
file1_path = None
file2_path = None


def plot_selected_data(selected_file):
    print(f'{selected_file=}')
    if selected_file == 3:
        file_data1 = np.load(file1_path)
        file_data2 = np.load(file2_path)

        # plot both as scatter plots
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(file_data1[:, 0], file_data1[:, 1], s=5, picker=True)
        ax.scatter(file_data2[:, 0], file_data2[:, 1], s=5, picker=True)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(f'File {selected_file}')
    else:   
        if selected_file == 1:
            file_data = np.load(file1_path)
            scatter = cip.CreateInteractivePlot(file_data, file1_path=file1_path)
        elif selected_file == 2:
            file_data = np.load(file2_path)
            scatter = cip.CreateInteractivePlot(file_data, file2_path=file2_path)
    plt.show()

        # everytime i run the function, i want to open a new plot
        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # ax.scatter(file_data[:, 0], file_data[:, 1], s=5, picker=True)
        # ax.set_xlabel('X')
        # ax.set_ylabel('Y')
        # ax.set_title(f'File {selected_file}')
        # plt.show()


def select_path(input_field, is_folder, file=""):
    dialog_func = filedialog.askdirectory if is_folder else filedialog.askopenfilename
    selected_path = dialog_func(initialdir="", title="Select a folder") if is_folder else dialog_func(title="Select a file", filetypes=(("Numpy files", "*.npy"),("Text files", "*.txt"), ("all files", "*.*")))
    
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


def update_input_field(input_filed, value):
    input_filed.delete(0, tk.END)  # Clear existing text in the input field
    input_filed.insert(0, value)  # Insert selected folder address


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
