import os
import shutil

def move_files_to_top_level(target_directory):
    """
    Moves all files from subdirectories to the top-level directory.

    :param target_directory: The root directory to search for files.
    """
    if not os.path.exists(target_directory):
        print(f"The directory '{target_directory}' does not exist.")
        return
    
    for root, _, files in os.walk(target_directory):
        # Skip the top-level directory itself
        if root == target_directory:
            continue

        for file in files:
            source_file = os.path.join(root, file)
            destination_file = os.path.join(target_directory, file)

            # Handle duplicate filenames
            if os.path.exists(destination_file):
                base, ext = os.path.splitext(file)
                counter = 1
                while os.path.exists(destination_file):
                    destination_file = os.path.join(
                        target_directory, f"{base}_{counter}{ext}"
                    )
                    counter += 1

            try:
                shutil.move(source_file, destination_file)
                print(f"Moved: {source_file} -> {destination_file}")
            except Exception as e:
                print(f"Error moving {source_file}: {e}")

    # Optional: Remove empty folders
    for root, dirs, _ in os.walk(target_directory, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                os.rmdir(dir_path)
                print(f"Removed empty folder: {dir_path}")
            except OSError as e:
                print(f"Error removing folder {dir_path}: {e}")

# Example usage
if __name__ == "__main__":
    target_dir = input("Enter the target directory: ").strip()
    move_files_to_top_level(target_dir)
