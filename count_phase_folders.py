import os

def count_phase_folders(root_path="."):
    """
    Count the number of subfolders named 'Phase' in the given directory and its subdirectories.
    
    Args:
        root_path (str): The root directory to search in. Defaults to current directory.
    
    Returns:
        int: The count of folders named 'Phase'
    """
    count = 0
    phase_folders = []
    
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(root_path):
        # Check if 'Phase' is in the current directory's subdirectories
        for dir_name in dirs:
            if dir_name == "Phase":
                count += 1
                full_path = os.path.join(root, dir_name)
                phase_folders.append(full_path)
                print(f"Found Phase folder: {full_path}")
    
    return count, phase_folders

def main():
    """Main function to count and display Phase folders."""
    print("Searching for folders named 'Phase' in the current workspace...")
    print("=" * 60)
    
    # Get the current working directory
    current_dir = os.getcwd()
    print(f"Searching in: {current_dir}")
    print()
    
    # Count the folders
    count, folders = count_phase_folders()
    
    print("=" * 60)
    print(f"Total number of 'Phase' folders found: {count}")
    
    if count > 0:
        print("\nList of all Phase folders:")
        for i, folder in enumerate(folders, 1):
            print(f"{i}. {folder}")
    else:
        print("No folders named 'Phase' were found.")

if __name__ == "__main__":
    main()
