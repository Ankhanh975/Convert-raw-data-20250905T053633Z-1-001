import os
import shutil

def find_reflection_coefficient_folders(root_path="."):
    """
    Find all folders named 'Reflection Coefficient'.
    
    Args:
        root_path (str): The root directory to search in. Defaults to current directory.
    
    Returns:
        list: List of full paths to 'Reflection Coefficient' folders
    """
    reflection_folders = []
    
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(root_path):
        # Check if 'Reflection Coefficient' is in the current directory's subdirectories
        for dir_name in dirs:
            if dir_name == "Reflection Coefficient":
                full_path = os.path.join(root, dir_name)
                reflection_folders.append(full_path)
    
    return reflection_folders

def move_files_from_reflection_coefficient(root_path=".", dry_run=True):
    """
    Move all files from 'Reflection Coefficient' folders to their parent directories.
    
    Args:
        root_path (str): The root directory to search in. Defaults to current directory.
        dry_run (bool): If True, only show what would be moved without actually moving.
    
    Returns:
        tuple: (success_count, error_count, errors)
    """
    reflection_folders = find_reflection_coefficient_folders(root_path)
    success_count = 0
    error_count = 0
    errors = []
    
    if not reflection_folders:
        print("No 'Reflection Coefficient' folders found.")
        return 0, 0, []
    
    print(f"Found {len(reflection_folders)} 'Reflection Coefficient' folders.")
    print("=" * 60)
    
    for i, folder_path in enumerate(reflection_folders, 1):
        try:
            parent_dir = os.path.dirname(folder_path)
            folder_name = os.path.basename(folder_path)
            
            # Get all files in the Reflection Coefficient folder
            files_in_folder = []
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    files_in_folder.append(file_path)
            
            if not files_in_folder:
                print(f"[{i:2d}/{len(reflection_folders)}] Empty folder: {folder_path}")
                continue
            
            print(f"[{i:2d}/{len(reflection_folders)}] Processing: {folder_path}")
            print(f"    Found {len(files_in_folder)} files to move to parent directory")
            
            if not dry_run:
                # Move each file to the parent directory
                for file_path in files_in_folder:
                    file_name = os.path.basename(file_path)
                    dest_path = os.path.join(parent_dir, file_name)
                    
                    # Handle filename conflicts
                    counter = 1
                    original_dest = dest_path
                    while os.path.exists(dest_path):
                        name, ext = os.path.splitext(original_dest)
                        dest_path = f"{name}_{counter}{ext}"
                        counter += 1
                    
                    shutil.move(file_path, dest_path)
                    print(f"    Moved: {file_name} -> {os.path.basename(dest_path)}")
                
                # Remove the empty Reflection Coefficient folder
                os.rmdir(folder_path)
                print(f"    Deleted empty folder: {folder_name}")
                success_count += 1
            else:
                # Dry run - just show what would happen
                for file_path in files_in_folder:
                    file_name = os.path.basename(file_path)
                    print(f"    [DRY RUN] Would move: {file_name}")
                print(f"    [DRY RUN] Would delete folder: {folder_name}")
                
        except Exception as e:
            error_count += 1
            error_msg = f"Error processing {folder_path}: {str(e)}"
            errors.append(error_msg)
            print(f"[{i:2d}/{len(reflection_folders)}] ERROR: {error_msg}")
    
    return success_count, error_count, errors

def main():
    """Main function to move files from Reflection Coefficient folders."""
    print("Reflection Coefficient Files Mover")
    print("=" * 60)
    
    # First, show what would be moved
    print("1. Scanning for 'Reflection Coefficient' folders in PNG_Files...")
    reflection_folders = find_reflection_coefficient_folders("PNG_Files")
    
    if not reflection_folders:
        print("No 'Reflection Coefficient' folders found in PNG_Files.")
        return
    
    print(f"Found {len(reflection_folders)} 'Reflection Coefficient' folders:")
    for i, folder in enumerate(reflection_folders, 1):
        print(f"  {i:2d}. {folder}")
    
    print("\n" + "=" * 60)
    print("WARNING: This will move all files from 'Reflection Coefficient' folders to their parent directories!")
    print("WARNING: This will delete the empty 'Reflection Coefficient' folders!")
    print("=" * 60)
    
    # Ask for confirmation
    while True:
        response = input("\nDo you want to proceed? (yes/no): ").lower().strip()
        if response in ['yes', 'y']:
            break
        elif response in ['no', 'n']:
            print("Operation cancelled.")
            return
        else:
            print("Please enter 'yes' or 'no'.")
    
    # Perform the operation
    print("\n2. Moving files from 'Reflection Coefficient' folders in PNG_Files...")
    print("=" * 60)
    
    success_count, error_count, errors = move_files_from_reflection_coefficient("PNG_Files", dry_run=False)
    
    # Show results
    print("\n" + "=" * 60)
    print("OPERATION SUMMARY:")
    print(f"Successfully processed: {success_count} folders")
    print(f"Errors: {error_count} folders")
    
    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f"  - {error}")
    
    if success_count > 0:
        print(f"\n✓ Successfully moved files from {success_count} 'Reflection Coefficient' folders!")
        print("✓ Empty 'Reflection Coefficient' folders have been deleted.")
    
    if error_count > 0:
        print(f"\n⚠ {error_count} folders could not be processed. Check the errors above.")

if __name__ == "__main__":
    main()
