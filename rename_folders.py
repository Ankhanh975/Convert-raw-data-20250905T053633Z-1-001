import os

def find_folders_to_rename(root_path="PNG_Files"):
    """
    Find all folders that need to be renamed.
    
    Args:
        root_path (str): The root directory to search in. Defaults to PNG_Files.
    
    Returns:
        list: List of tuples (old_path, new_path, rename_type)
    """
    folders_to_rename = []
    
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(root_path):
        for dir_name in dirs:
            old_path = os.path.join(root, dir_name)
            new_name = None
            rename_type = None
            
            # Check for "tumor" or "tumour" (case insensitive)
            if 'tumor' in dir_name.lower() or 'tumour' in dir_name.lower():
                # Check if it's a pattern like "241108_CRC_Tumour" and rename to just "tumour"
                if '_' in dir_name and ('tumor' in dir_name.lower() or 'tumour' in dir_name.lower()):
                    new_name = 'tumour'
                    rename_type = f"{dir_name} → tumour"
                else:
                    # Replace all variations of tumor with tumour (case insensitive)
                    new_name = dir_name
                    # Handle different cases
                    if 'Tumor' in dir_name:
                        new_name = new_name.replace('Tumor', 'Tumour')
                    if 'tumor' in dir_name:
                        new_name = new_name.replace('tumor', 'tumour')
                    if 'TUMOR' in dir_name:
                        new_name = new_name.replace('TUMOR', 'TUMOUR')
                    rename_type = "tumor → tumour"
            # Check for "healthy" (case insensitive) - standardize to lowercase
            elif 'healthy' in dir_name.lower() and dir_name.lower() != 'healthy':
                # Check if it's a pattern like "241108_CRC_Healthy" and rename to just "healthy"
                if '_' in dir_name and 'healthy' in dir_name.lower():
                    new_name = 'healthy'
                    rename_type = f"{dir_name} → healthy"
                else:
                    new_name = 'healthy'
                    rename_type = "healthy → healthy"
            
            if new_name and new_name != dir_name:
                new_path = os.path.join(root, new_name)
                folders_to_rename.append((old_path, new_path, rename_type))
    
    return folders_to_rename

def rename_folders(root_path="PNG_Files", dry_run=True):
    """
    Rename folders containing 'tumor' to 'tumour' and standardize 'healthy'.
    
    Args:
        root_path (str): The root directory to search in. Defaults to PNG_Files.
        dry_run (bool): If True, only show what would be renamed without actually renaming.
    
    Returns:
        tuple: (success_count, error_count, errors)
    """
    folders_to_rename = find_folders_to_rename(root_path)
    success_count = 0
    error_count = 0
    errors = []
    
    if not folders_to_rename:
        print("No folders found that need renaming.")
        return 0, 0, []
    
    print(f"Found {len(folders_to_rename)} folders to rename.")
    print("=" * 60)
    
    for i, (old_path, new_path, rename_type) in enumerate(folders_to_rename, 1):
        try:
            if dry_run:
                print(f"[DRY RUN] {rename_type}: {os.path.basename(old_path)} → {os.path.basename(new_path)}")
            else:
                # Check if old folder exists
                if os.path.exists(old_path):
                    # Check if new folder already exists
                    if os.path.exists(new_path):
                        print(f"[{i:2d}/{len(folders_to_rename)}] SKIP: {os.path.basename(new_path)} already exists")
                        continue
                    
                    # Rename the folder
                    os.rename(old_path, new_path)
                    print(f"[{i:2d}/{len(folders_to_rename)}] {rename_type}: {os.path.basename(old_path)} → {os.path.basename(new_path)}")
                    success_count += 1
                else:
                    print(f"[{i:2d}/{len(folders_to_rename)}] NOT FOUND: {old_path}")
        except Exception as e:
            error_count += 1
            error_msg = f"Error renaming {old_path}: {str(e)}"
            errors.append(error_msg)
            print(f"[{i:2d}/{len(folders_to_rename)}] ERROR: {error_msg}")
    
    return success_count, error_count, errors

def main():
    """Main function to rename folders."""
    print("Folder Renaming Tool")
    print("=" * 60)
    print("This script will:")
    print("• Rename folders containing 'tumor' to 'tumour'")
    print("• Standardize 'healthy' folder names")
    print("=" * 60)
    
    # First, show what would be renamed
    print("1. Scanning for folders to rename in PNG_Files...")
    folders_to_rename = find_folders_to_rename("PNG_Files")
    
    if not folders_to_rename:
        print("No folders found that need renaming in PNG_Files.")
        return
    
    print(f"Found {len(folders_to_rename)} folders to rename:")
    for i, (old_path, new_path, rename_type) in enumerate(folders_to_rename, 1):
        print(f"  {i:2d}. {rename_type}: {os.path.basename(old_path)} → {os.path.basename(new_path)}")
        print(f"      {old_path}")
    
    print("\n" + "=" * 60)
    print("WARNING: This will rename the folders permanently!")
    print("=" * 60)
    
    # Ask for confirmation
    while True:
        response = input("\nDo you want to proceed with renaming? (yes/no): ").lower().strip()
        if response in ['yes', 'y']:
            break
        elif response in ['no', 'n']:
            print("Renaming cancelled.")
            return
        else:
            print("Please enter 'yes' or 'no'.")
    
    # Perform the renaming
    print("\n2. Renaming folders in PNG_Files...")
    print("=" * 60)
    
    success_count, error_count, errors = rename_folders("PNG_Files", dry_run=False)
    
    # Show results
    print("\n" + "=" * 60)
    print("RENAMING SUMMARY:")
    print(f"Successfully renamed: {success_count} folders")
    print(f"Errors: {error_count} folders")
    
    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f"  - {error}")
    
    if success_count > 0:
        print(f"\n✓ Successfully renamed {success_count} folders!")
    
    if error_count > 0:
        print(f"\n⚠ {error_count} folders could not be renamed. Check the errors above.")

if __name__ == "__main__":
    main()
