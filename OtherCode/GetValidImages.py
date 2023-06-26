import os
import pandas as pd
import shutil

def copy_images(df, source_folder, destination_folder):
    """
    Copies images from the source folder to the destination folder based on the paths specified in the "images" column of the DataFrame.
    
    Args:
        df (DataFrame): The DataFrame containing the "images" column.
        source_folder (str): The path of the source folder.
        destination_folder (str): The path of the destination folder.
    """
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Get the image path from the "images" column
        image_path = row["images"]
        
        # Construct the source and destination paths
        source_path = os.path.join(source_folder, image_path)
        destination_path = os.path.join(destination_folder, image_path)
        
        # Create the necessary directories in the destination path if they don't exist
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        
        # Copy the image from source to destination
        shutil.copy2(source_path, destination_path)
