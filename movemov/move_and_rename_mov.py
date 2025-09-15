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
                # Get relative path from the source directory
                relative_path = os.path.relpath(root, source_dir)
                # Replace directory separators with underscores
                relative_path = relative_path.replace(os.sep, '_')
                # Construct the new file name
                new_file_name = f"{relative_path}_{file}"
                # Construct the full file path
                file_path = os.path.join(root, file)
                # Construct the destination file path
                dest_file_path = os.path.join(dest_dir, new_file_name)
                # Move the file to the destination directory with the new name
                shutil.move(file_path, dest_file_path)
                print(f"Moved: {file_path} to {dest_file_path}")

# Define your source directory and destination directory
source_directory = "C:/path/to/your/source_directory"
destination_directory = "C:/Users/YourUsername/Desktop/bucket"

# Run the function

move_files(source_directory, destination_directory)
