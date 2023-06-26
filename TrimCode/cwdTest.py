import os

cwd = os.getcwd()
# print(f'cwd: {cwd}')
# get one directory up from cwd
main_path = os.path.dirname(cwd)
# print(f'main_path: {main_path}')

main_path = main_path.replace('\\', '/')
# print(f'cwd: {cwd}')

# mp_source_folder = main_path + "/DataFolder/mpFiles/elbrest-abd-add-06-04-2023-15-17-34/"
mp_source_folder = main_path + "/DataFolder/mpFiles/14/"
kin_source_folder = main_path + "/DataFolder/kinFiles/14/"

kin_csv_path = kin_source_folder + "/kin-elbrest-abd-add-06-04-23-07-17-44.txt"
mp_csv_path =  mp_source_folder + "/analysis/elbrest-abd-add-06-04-2023-15-17-34.csv"



# iterate through all folders in mp_sorce_folder
for folder in os.listdir(mp_source_folder):
    print(f'folder: {folder}')
    # get the path of the folder
    folder_path = mp_source_folder + folder
    print(f'folder_path: {folder_path}')
    # iterate through all files in the folder

    if folder == "analysis":
        for file in os.listdir(folder_path):
            print(f'file: {file}')
            # get the path of the file
            file_path = folder_path + "/" + file
            print(f'file_path: {file_path}')