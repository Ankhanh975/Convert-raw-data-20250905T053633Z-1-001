import os
import shutil

def find_mix_folders(root_path="."):
    """
    Find all folders containing 'Mix' in their names (case insensitive).
    
    Args:
        root_path (str): The root directory to search in. Defaults to current directory.
    
    Returns:
        list: List of full paths to folders with 'Mix' in name
    """
    mix_folders = []
    
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(root_path):
        # Check current directory's subdirectories
        for dir_name in dirs:
            if 'mix' in dir_name.lower():
                full_path = os.path.join(root, dir_name)
                mix_folders.append(full_path)
    
    return mix_folders

def delete_mix_folders(root_path=".", dry_run=True):
    """
    Delete all folders containing 'Mix' in their names (case insensitive).
    
    Args:
        root_path (str): The root directory to search in. Defaults to current directory.
        dry_run (bool): If True, only show what would be deleted without actually deleting.
    
    Returns:
        tuple: (success_count, error_count, errors)
    """
    mix_folders = find_mix_folders(root_path)
    success_count = 0
    error_count = 0
    errors = []
    
    if not mix_folders:
        print("No folders with 'Mix' found.")
        return 0, 0, []
    
    print(f"Found {len(mix_folders)} folders with 'Mix' in name.")
    print("=" * 60)
    
    for i, folder_path in enumerate(mix_folders, 1):
        try:
            if dry_run:
                print(f"[DRY RUN] Would delete: {folder_path}")
            else:
                # Check if folder exists before trying to delete
                if os.path.exists(folder_path):
                    shutil.rmtree(folder_path)
                    print(f"[{i:2d}/{len(mix_folders)}] Deleted: {folder_path}")
                    success_count += 1
                else:
                    print(f"[{i:2d}/{len(mix_folders)}] Not found: {folder_path}")
        except Exception as e:
            error_count += 1
            error_msg = f"Error deleting {folder_path}: {str(e)}"
            errors.append(error_msg)
            print(f"[{i:2d}/{len(mix_folders)}] ERROR: {error_msg}")
    
    return success_count, error_count, errors

def main():
    """Main function to delete folders with 'Mix' in name."""
    print("Mix Folders Deletion Tool")
    print("=" * 60)
    
    # First, show what would be deleted
    print("1. Scanning for folders with 'Mix' in name...")
    mix_folders = find_mix_folders()
    
    if not mix_folders:
        print("No folders with 'Mix' found.")
        return
    
    print(f"Found {len(mix_folders)} folders:")
    for i, folder in enumerate(mix_folders, 1):
        print(f"  {i:2d}. {folder}")
    
    print("\n" + "=" * 60)
    print("WARNING: This will permanently delete all folders with 'Mix' in their names!")
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
    print("\n2. Deleting folders with 'Mix' in name...")
    print("=" * 60)
    
    success_count, error_count, errors = delete_mix_folders(dry_run=False)
    
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
        print(f"\n✓ Successfully deleted {success_count} folders with 'Mix'!")
    
    if error_count > 0:
        print(f"\n⚠ {error_count} folders could not be deleted. Check the errors above.")

if __name__ == "__main__":
    main()
