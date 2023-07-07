import os
import datetime
import shutil

def add_hours_to_filenames(directoryB, directoryC, hours_to_add):
    # Create the destination directory if it doesn't exist
    if not os.path.exists(directoryC):
        os.makedirs(directoryC)

    for file in os.listdir(directoryB):
        if file.endswith('.txt'):
            # Parse the information from the file name
            file_name_parts = file[:-4]
            # print(f'file_name_parts: {file_name_parts}')
            date_time = file_name_parts[-17:]
            # print(f'date_time: {date_time}')
            date = datetime.datetime.strptime(date_time, '%d-%m-%y-%H-%M-%S').date()
            # print(f'date: {date}')
            file_time = datetime.datetime.strptime(date_time, '%d-%m-%y-%H-%M-%S').time()
            # print(f'file_time: {file_time}')

            # Add the specified number of hours
            new_file_time = (datetime.datetime.combine(date, file_time) + datetime.timedelta(hours=hours_to_add)).time()
            # print(f'new_file_time: {new_file_time}')

            # print(f'first_part: {file_name_parts[:-17]}')

            # Create the new file name
            new_file_name = file_name_parts[:-17] + date.strftime('%d-%m-%Y') + '-' + new_file_time.strftime('%H-%M-%S') + '.txt'

            # Generate the source and destination paths
            source_path = os.path.join(directoryB, file)
            destination_path = os.path.join(directoryC, new_file_name)

            # Copy the file to the destination directory with the new name
            shutil.copy(source_path, destination_path)
            print(f"Copied '{file}' to '{destination_path}'")


# MATCHING WITH FOLDER NAME
# def place_file_in_matching_folder(directoryA, directoryB, file_extension='.txt'):
#     # Get a list of all folders in DirectoryA
#     folders = [folder for folder in os.listdir(directoryA) if os.path.isdir(os.path.join(directoryA, folder))]
#     count = 0
#     for file in os.listdir(directoryB):
#         if file.endswith(file_extension):
#             # Parse the information from the text file name in DirectoryB
#             file_name_parts = file[:-4]
#             experiment_name = file_name_parts[4:-20]
#             print(f'experiment_name: {experiment_name}')
#             # date = datetime.datetime.strptime(file_name_parts[3], '%m-%d-%y-%H-%M-%S').date()
#             # file_time = datetime.datetime.strptime(file_name_parts[4], '%H-%M-%S').time()
#             file_name_parts = file[:-4]
#             date_time = file_name_parts[-19:]
#             # print(f'date_time: {date_time}')
#             file_date = datetime.datetime.strptime(date_time, '%d-%m-%Y-%H-%M-%S').date()
#             # print(f'date: {date}')
#             file_time = datetime.datetime.strptime(date_time, '%d-%m-%Y-%H-%M-%S').time()
#             print(f'date: {file_date}')
#             print(f'file_time: {file_time}')
#             # break
#             # Initialize variables to track the closest matching folder
#             closest_folder = None
#             closest_time_difference = None

#             # Iterate through each folder in DirectoryA
#             for folder in folders:
#                 # Parse the information from the folder name in DirectoryA
#                 folder_name_parts = folder
#                 folder_experiment_name = folder_name_parts[:-20]
#                 # print(f'folder_experiment_name: {folder_experiment_name}')
#                 # break
#                 folder_date_time = folder_name_parts[-19:]
#                 # print(f'folder_date_time: {folder_date_time}')
                
#                 folder_date = datetime.datetime.strptime(folder_date_time, '%d-%m-%Y-%H-%M-%S').date()
#                 folder_time = datetime.datetime.strptime(folder_date_time, '%d-%m-%Y-%H-%M-%S').time()
#                 # print(f'folder_date: {folder_date}')
#                 # print(f'folder_time: {folder_time}')
#                 # break
#                 # Compare the sensor name, experiment name, and date
#                 if experiment_name == folder_experiment_name and file_date == folder_date:
#                     # Calculate the time difference between the file and folder
#                     time_difference = abs((datetime.datetime.combine(file_date, file_time) - datetime.datetime.combine(folder_date, folder_time)).total_seconds())
#                     # print(f'time_difference: {time_difference}')

#                     # Update the closest folder if it's the first iteration or if the current folder has a closer time
#                     if closest_folder is None or time_difference < closest_time_difference:
#                         closest_folder = folder + "/analysis"
#                         closest_time_difference = time_difference


#             # Place the file from DirectoryB into the closest matching folder
#             if closest_folder is not None:
#                 source_path = os.path.join(directoryB, file)
#                 destination_path = os.path.join(directoryA, closest_folder, file)
#                 # os.rename(source_path, destination_path)
#                 shutil.copy2(source_path, destination_path)
#                 print(f"Moved '{file}' to folder '{closest_folder}'")
#             # break
#                 count += 1
#     print(f'count: {count}')

# MATCH WITH FILE NAME
def place_file_in_matching_folder(directoryA, directoryB, file_extension='.txt'):
    # Get a list of all folders in DirectoryA
    folders = [folder for folder in os.listdir(directoryA) if os.path.isdir(os.path.join(directoryA, folder))]
    count = 0
    for file in os.listdir(directoryB):
        if file.endswith(file_extension):
            # Parse the information from the text file name in DirectoryB

            file_name_parts = file[:-4]
            experiment_name = file_name_parts[4:-20]
            print(f'experiment_name: {experiment_name}')

            file_name_parts = file[:-4]
            date_time = file_name_parts[-19:]
            file_date = datetime.datetime.strptime(date_time, '%d-%m-%Y-%H-%M-%S').date()
            file_time = datetime.datetime.strptime(date_time, '%d-%m-%Y-%H-%M-%S').time()
            print(f'date: {file_date}')
            print(f'file_time: {file_time}')

            # Initialize variables to track the closest matching folder
            closest_folder = None
            closest_time_difference = None

            # Iterate through each folder in DirectoryA
            for folder in folders:
                analysis_folder = os.path.join(directoryA, folder, 'analysis')
                if not os.path.exists(analysis_folder):
                    continue

                # Get the list of CSV files in the analysis folder
                analysis_files = [f for f in os.listdir(analysis_folder) if f.endswith('.csv')]
                if not analysis_files:
                    continue

                # Iterate through each CSV file in the analysis folder
                for analysis_file in analysis_files:
                    # Parse the information from the folder name in DirectoryA
                    analysis_file_name_parts = analysis_file[:-4]
                    analysis_experiment_name = analysis_file_name_parts[:-20]
                    # print(f'folder_experiment_name: {folder_experiment_name}')
                    # break
                    analysis_date_time = analysis_file_name_parts[-19:]
                    # print(f'folder_date_time: {folder_date_time}')
                    analysis_date = datetime.datetime.strptime(analysis_date_time, '%d-%m-%Y-%H-%M-%S').date()
                    analysis_time = datetime.datetime.strptime(analysis_date_time, '%d-%m-%Y-%H-%M-%S').time()

                    # Compare the experiment name and date
                    if experiment_name == analysis_experiment_name and file_date == analysis_date:
                        # Calculate the time difference between the file and analysis file
                        time_difference = abs((datetime.datetime.combine(file_date, file_time) - datetime.datetime.combine(analysis_date, analysis_time)).total_seconds())

                        # Update the closest folder if it's the first iteration or if the current folder has a closer time
                        if closest_folder is None or time_difference < closest_time_difference:
                            closest_folder = analysis_folder
                            closest_time_difference = time_difference

            # Place the file from DirectoryB into the closest matching folder
            if closest_folder is not None:
                source_path = os.path.join(directoryB, file)
                destination_path = os.path.join(closest_folder, file)
                shutil.copy2(source_path, destination_path)
                print(f"Moved '{file}' to folder '{closest_folder}'")
                count += 1

    print(f'count: {count}')

# function to delete .txt files in folders in the directoryA
def delete_txt_files(directoryA):
    # Get a list of all folders in DirectoryA
    folders = [folder + "/analysis/" for folder in os.listdir(directoryA) if os.path.isdir(os.path.join(directoryA, folder))]
    count = 0
    for folder in folders:
        for file in os.listdir(os.path.join(directoryA, folder)):
            if file.endswith('.txt'):
                os.remove(os.path.join(directoryA, folder, file))
                print(f"Deleted '{file}' from folder '{folder}'")
                count += 1
    print(f'count: {count}')

# function to print names of all empty text files in directoryB
def print_empty_txt_files(directoryB):
    for file in os.listdir(directoryB):
        if file.endswith('.txt'):
            if os.stat(os.path.join(directoryB, file)).st_size == 0:
                print(file)

cwd = os.getcwd()
# replace \\ with / for Windows
cwd = cwd.replace('\\', '/')
# print(f'cwd: {cwd}')
# get one directory up from cwd
main_path = os.path.dirname(cwd)
# print(f'main_path: {main_path}')

hours_to_add = 8
# # Example usage
directoryA = main_path + '/pythonTest/DirectoryA'
directoryB = main_path + '/pythonTest/DirectoryB'
directoryC = main_path + '/pythonTest/DirectoryC'
testA = main_path + '/pythonTest/testA'

# add_hours_to_filenames(directoryB, directoryC, hours_to_add)

place_file_in_matching_folder(directoryA, directoryC, file_extension='.txt')
#
# delete_txt_files(directoryA)

# print_empty_txt_files(directoryB)
