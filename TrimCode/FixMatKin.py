import pandas as pd
import os

import pandas as pd

def swap_columns(csv_file):
    # Read CSV file into a dataframe
    df = pd.read_csv(csv_file, header=None, sep=',', index_col=False)

    # Swap column 3 with column 5
    df[df.columns[3]], df[df.columns[4]] = df[df.columns[4]].copy(), df[df.columns[3]].copy()

    # Save modified dataframe as a .txt file
    # txt_file = csv_file.replace('.csv', '.txt')
    # Add custom header
    header = ["elev", "shp", "time", "elb", "rie"]
    df.columns = header
    df.to_csv(csv_file, sep=',', index=False)

    # Return the resulting dataframe
    return df



cwd = os.getcwd()
print(f'Current working directory: {cwd}')


# matKinFile = os.path.join(cwd, 'TestCleanData/1/elbrest-abd-add-24-10-2022-19-09-37/analysis/')

# read the firs two lines of the file and print them

def RemoveFirstLine(matKinFile, newFilename="newFile.txt"):
    with open(matKinFile, 'r') as f:
        lines = f.readlines()

    # save lines as "newFile"

    with open(newFilename, 'w') as new_file:
        for i, line in enumerate(lines):
            if i < 2:
                if "Kinect_RightElbow_Ext.-Flex.," in line:
                    line_split = line.split("Kinect_RightElbow_Ext.-Flex.,")
                    new_file.write(line_split[-1])
                else:
                    new_file.write(line)
            else:
                new_file.write(line)


"Timestamp,Kinect_LeftShoulder_Ext.-Flex.,Kinect_LeftShoulder_Abd.-Add.,Kinect_LeftShoulder_Int.-Ext.,Kinect_LeftElbow_Ext.-Flex.,Kinect_RightShoulder_Ext.-Flex.,"
"Kinect_RightShoulder_Abd.-Add.,Kinect_RightShoulder_Int.-Ext.,Kinect_RightElbow_Ext.-Flex.,18.59,-17.99,19:09:45:687,666.00,19.27"
# print(os.listdir(matKinFile))
# iterate over files in a directory

def ModifyMatKinFiles(matKinFile):
    for filename in os.listdir(matKinFile):
        # print(filename)
        if filename.endswith(".txt") and filename.startswith("mat-kin"):
            # remove mat-kin- from the filename
            newFilename = filename.replace("mat-kin-", "kin-")
            print(f'newFilename: {newFilename}')
            print(f'new path {matKinFile + newFilename}')
            RemoveFirstLine(os.path.join(matKinFile + filename), os.path.join(matKinFile + newFilename))
            print(f'File: {filename} has been modified')

            swap_columns(os.path.join(matKinFile + newFilename))

# print sirectories in the userPath
# print(os.listdir(userPath))
# iterate over directories in the userPath
userPath = os.path.join(cwd, "TestCleanData")

for directory in os.listdir(userPath):
    # print(f'directory: {userPath + directory}')
    dir_path = os.path.join(userPath, directory)
    # iterate over files in the userPath + directory
    for exercise in os.listdir(dir_path):
        # print(f'filename: {userPath + directory + "/" + exercise}')
        exercise_path = os.path.join(userPath , directory , str(exercise), "analysis\\")
        ModifyMatKinFiles(exercise_path)
        # for filename in os.listdir(exercise_path):
        #     if filename.endswith(".txt") and filename.startswith("mat-kin"):
        #         # print(f'filename: {userPath + directory + "/" + exercise + "/analysis/" + filename}')
        #         file_path = os.path.join(exercise_path, filename)
                

    
    break
        

# result_df = swap_columns('data.csv')
# print(result_df)
