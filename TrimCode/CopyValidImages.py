import os
import pandas as pd
import shutil

def CopyValidImages(df, source_folder, destination_folder):
    """
    Copies images from the source folder to the destination folder based on the paths specified in the "images" column of the DataFrame.
    
    Args:
        df (DataFrame): The DataFrame containing the "images" column.
        source_folder (str): The path of the source folder.
        destination_folder (str): The path of the destination folder.
    """

    # convert df column to list
    # df = df['images'].tolist()

    print(df)

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        image_path = str(row['images'])    
        # Construct the source and destination paths
        # if the path exists

        # source_path = os.path.join(source_folder, str(image_path))
        # destination_path = os.path.join(destination_folder, str(image_path))
        source_path = source_folder + "images/" + image_path
        destination_path = destination_folder + "images/" + image_path
        

        print(f'source_path: {source_path}')
        print(f'destination_path: {destination_path}')
        
        # Copy the image from source to destination
        shutil.copy2(source_path, destination_path)
