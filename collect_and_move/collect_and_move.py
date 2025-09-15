# A simple script that will collect all .mov files from subdirectories 
# and move them to a new location.

import os
import shutil

def find_and_move_mov_files(source_directory, destination_directory):
    # Iterate through all subdirectories and files in the source directory
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.endswith(".mov"):
                # Construct the full path of the .mov file
                mov_file_path = os.path.join(root, file)
                
                # Move the .mov file to the destination directory
                shutil.move(mov_file_path, destination_directory)
                print(f"Moved: {mov_file_path} to {destination_directory}")

# Replace these paths with your source and destination directories
source_directory = "/path/to/source/directory"
destination_directory = "/path/to/destination/directory"

find_and_move_mov_files(source_directory, destination_directory)
