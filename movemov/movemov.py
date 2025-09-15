import os
import shutil

def move_files(source_dir, dest_dir):
    # Ensure the destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Walk through the source directory
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".mov"):
                # Construct the full file path
                file_path = os.path.join(root, file)
                # Move the file to the destination directory
                shutil.move(file_path, dest_dir)
                print(f"Moved: {file_path} to {dest_dir}")

# Define your source directory and destination directory
source_directory = "C:/path/to/your/source_directory"
destination_directory = "C:/Users/YourUsername/Desktop/bucket"

# Run the function
move_files(source_directory, destination_directory)