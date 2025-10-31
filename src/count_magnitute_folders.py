import os

def count_magnitude_folders(root_path="."):
    """
    Count the number of subfolders named 'Magnitude' in the given directory and its subdirectories.
    
    Args:
        root_path (str): The root directory to search in. Defaults to current directory.
    
    Returns:
        int: The count of folders named 'Magnitude'
    """
    count = 0
    magnitude_folders = []
    
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(root_path):
        # Check if 'Magnitude' is in the current directory's subdirectories
        for dir_name in dirs:
            if dir_name == "Magnitude":
                count += 1
                full_path = os.path.join(root, dir_name)
                magnitude_folders.append(full_path)
                print(f"Found Magnitude folder: {full_path}")
    
    return count, magnitude_folders

def main():
    """Main function to count and display Magnitude folders."""
    print("Searching for folders named 'Magnitude' in the current workspace...")
    print("=" * 60)
    
    # Get the current working directory
    current_dir = os.getcwd()
    print(f"Searching in: {current_dir}")
    print()
    
    # Count the folders
    count, folders = count_magnitude_folders()
    
    print("=" * 60)
    print(f"Total number of 'Magnitude' folders found: {count}")
    
    if count > 0:
        print("\nList of all Magnitude folders:")
        for i, folder in enumerate(folders, 1):
            print(f"{i}. {folder}")
    else:
        print("No folders named 'Magnitude' were found.")

if __name__ == "__main__":
    main()
