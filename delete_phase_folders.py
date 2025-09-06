import os
import shutil

def find_phase_folders(root_path="."):
    """
    Find all subfolders named 'Phase' in the given directory and its subdirectories.
    
    Args:
        root_path (str): The root directory to search in. Defaults to current directory.
    
    Returns:
        list: List of full paths to Phase folders
    """
    phase_folders = []
    
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(root_path):
        # Check if 'Phase' is in the current directory's subdirectories
        for dir_name in dirs:
            if dir_name == "Phase":
                full_path = os.path.join(root, dir_name)
                phase_folders.append(full_path)
    
    return phase_folders

def delete_phase_folders(root_path=".", dry_run=True):
    """
    Delete all subfolders named 'Phase' in the given directory and its subdirectories.
    
    Args:
        root_path (str): The root directory to search in. Defaults to current directory.
        dry_run (bool): If True, only show what would be deleted without actually deleting.
    
    Returns:
        tuple: (success_count, error_count, errors)
    """
    phase_folders = find_phase_folders(root_path)
    success_count = 0
    error_count = 0
    errors = []
    
    if not phase_folders:
        print("No Phase folders found.")
        return 0, 0, []
    
    print(f"Found {len(phase_folders)} Phase folders.")
    print("=" * 60)
    
    for i, folder_path in enumerate(phase_folders, 1):
        try:
            if dry_run:
                print(f"[DRY RUN] Would delete: {folder_path}")
            else:
                # Check if folder exists before trying to delete
                if os.path.exists(folder_path):
                    shutil.rmtree(folder_path)
                    print(f"[{i:2d}/{len(phase_folders)}] Deleted: {folder_path}")
                    success_count += 1
                else:
                    print(f"[{i:2d}/{len(phase_folders)}] Not found: {folder_path}")
        except Exception as e:
            error_count += 1
            error_msg = f"Error deleting {folder_path}: {str(e)}"
            errors.append(error_msg)
            print(f"[{i:2d}/{len(phase_folders)}] ERROR: {error_msg}")
    
    return success_count, error_count, errors

def main():
    """Main function to delete Phase folders."""
    print("Phase Folder Deletion Tool")
    print("=" * 60)
    
    # First, show what would be deleted
    print("1. Scanning for Phase folders...")
    phase_folders = find_phase_folders()
    
    if not phase_folders:
        print("No Phase folders found.")
        return
    
    print(f"Found {len(phase_folders)} Phase folders:")
    for i, folder in enumerate(phase_folders, 1):
        print(f"  {i:2d}. {folder}")
    
    print("\n" + "=" * 60)
    print("WARNING: This will permanently delete all Phase folders and their contents!")
    print("=" * 60)
    
    # Ask for confirmation
    while True:
        response = input("\nDo you want to proceed with deletion? (yes/no): ").lower().strip()
        if response in ['yes', 'y']:
            break
        elif response in ['no', 'n']:
            print("Deletion cancelled.")
            return
        else:
            print("Please enter 'yes' or 'no'.")
    
    # Perform the deletion
    print("\n2. Deleting Phase folders...")
    print("=" * 60)
    
    success_count, error_count, errors = delete_phase_folders(dry_run=False)
    
    # Show results
    print("\n" + "=" * 60)
    print("DELETION SUMMARY:")
    print(f"Successfully deleted: {success_count} folders")
    print(f"Errors: {error_count} folders")
    
    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f"  - {error}")
    
    if success_count > 0:
        print(f"\n✓ Successfully deleted {success_count} Phase folders!")
    
    if error_count > 0:
        print(f"\n⚠ {error_count} folders could not be deleted. Check the errors above.")

if __name__ == "__main__":
    main()
