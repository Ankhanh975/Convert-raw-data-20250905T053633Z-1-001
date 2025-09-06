import os

def find_weight_files(root_path="."):
    """
    Find all files containing 'weight_2' or 'weight_3' in their names.
    
    Args:
        root_path (str): The root directory to search in. Defaults to current directory.
    
    Returns:
        list: List of full paths to files with weight_2 or weight_3 in name
    """
    weight_files = []
    
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if 'weight_2' in file or 'weight_3' in file:
                full_path = os.path.join(root, file)
                weight_files.append(full_path)
    
    return weight_files

def delete_weight_files(root_path=".", dry_run=True):
    """
    Delete all files containing 'weight_2' or 'weight_3' in their names.
    
    Args:
        root_path (str): The root directory to search in. Defaults to current directory.
        dry_run (bool): If True, only show what would be deleted without actually deleting.
    
    Returns:
        tuple: (success_count, error_count, errors)
    """
    weight_files = find_weight_files(root_path)
    success_count = 0
    error_count = 0
    errors = []
    
    if not weight_files:
        print("No files with 'weight_2' or 'weight_3' found.")
        return 0, 0, []
    
    print(f"Found {len(weight_files)} files with 'weight_2' or 'weight_3' in name.")
    print("=" * 60)
    
    for i, file_path in enumerate(weight_files, 1):
        try:
            if dry_run:
                print(f"[DRY RUN] Would delete: {file_path}")
            else:
                # Check if file exists before trying to delete
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"[{i:3d}/{len(weight_files)}] Deleted: {os.path.basename(file_path)}")
                    success_count += 1
                else:
                    print(f"[{i:3d}/{len(weight_files)}] Not found: {file_path}")
        except Exception as e:
            error_count += 1
            error_msg = f"Error deleting {file_path}: {str(e)}"
            errors.append(error_msg)
            print(f"[{i:3d}/{len(weight_files)}] ERROR: {error_msg}")
    
    return success_count, error_count, errors

def main():
    """Main function to delete files with weight_2 or weight_3 in name."""
    print("Weight Files Deletion Tool")
    print("=" * 60)
    
    # First, show what would be deleted
    print("1. Scanning for files with 'weight_2' or 'weight_3' in name...")
    weight_files = find_weight_files()
    
    if not weight_files:
        print("No files with 'weight_2' or 'weight_3' found.")
        return
    
    print(f"Found {len(weight_files)} files:")
    for i, file in enumerate(weight_files, 1):
        print(f"  {i:3d}. {file}")
    
    print("\n" + "=" * 60)
    print("WARNING: This will permanently delete all files with 'weight_2' or 'weight_3' in their names!")
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
    print("\n2. Deleting files with 'weight_2' or 'weight_3' in name...")
    print("=" * 60)
    
    success_count, error_count, errors = delete_weight_files(dry_run=False)
    
    # Show results
    print("\n" + "=" * 60)
    print("DELETION SUMMARY:")
    print(f"Successfully deleted: {success_count} files")
    print(f"Errors: {error_count} files")
    
    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f"  - {error}")
    
    if success_count > 0:
        print(f"\n✓ Successfully deleted {success_count} files with 'weight_2' or 'weight_3'!")
    
    if error_count > 0:
        print(f"\n⚠ {error_count} files could not be deleted. Check the errors above.")

if __name__ == "__main__":
    main()
