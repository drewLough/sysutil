import os

def delete_files_with_suffix(target_directory, suffix=" - Copy"):
    """
    Deletes files that end with the specified suffix (before the file extension)
    in the target directory and its subdirectories.

    :param target_directory: The root directory to search for files.
    :param suffix: The suffix of the files to delete (before the extension).
    """
    if not os.path.exists(target_directory):
        print(f"The directory '{target_directory}' does not exist.")
        return
    
    for root, _, files in os.walk(target_directory):
        for file in files:
            # Split the file into name and extension
            filename, ext = os.path.splitext(file)
            
            # Check if the base filename ends with the suffix
            if filename.endswith(suffix):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

# Example usage
if __name__ == "__main__":
    target_dir = input("Enter the target directory: ").strip()
    delete_files_with_suffix(target_dir)
