import os
import shutil

def find_png_files(root_path="."):
    """
    Find all .png files in the given directory and its subdirectories.
    
    Args:
        root_path (str): The root directory to search in. Defaults to current directory.
    
    Returns:
        list: List of full paths to .png files
    """
    png_files = []
    
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.lower().endswith('.png'):
                full_path = os.path.join(root, file)
                png_files.append(full_path)
    
    return png_files

def create_destination_structure(source_path, dest_base_path):
    """
    Create the destination directory structure based on the source structure.
    
    Args:
        source_path (str): Source file path
        dest_base_path (str): Base destination directory
    
    Returns:
        str: Destination file path
    """
    # Get relative path from the source root
    rel_path = os.path.relpath(source_path, "Convert raw data")
    
    # Create destination path
    dest_path = os.path.join(dest_base_path, rel_path)
    
    # Create directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    
    return dest_path

def separate_png_files(source_root="Convert raw data", dest_root="PNG_Files"):
    """
    Separate all .png files into a new folder with the same structure.
    
    Args:
        source_root (str): Source directory to search for .png files
        dest_root (str): Destination directory for .png files
    
    Returns:
        tuple: (success_count, error_count, errors)
    """
    png_files = find_png_files(source_root)
    success_count = 0
    error_count = 0
    errors = []
    
    if not png_files:
        print("No .png files found.")
        return 0, 0, []
    
    print(f"Found {len(png_files)} .png files to separate.")
    print("=" * 60)
    
    # Create destination base directory
    os.makedirs(dest_root, exist_ok=True)
    
    for i, png_path in enumerate(png_files, 1):
        try:
            # Create destination path maintaining structure
            dest_path = create_destination_structure(png_path, dest_root)
            
            # Copy the file
            shutil.copy2(png_path, dest_path)
            print(f"[{i:4d}/{len(png_files)}] Copied: {os.path.relpath(png_path, source_root)}")
            success_count += 1
            
        except Exception as e:
            error_count += 1
            error_msg = f"Error copying {png_path}: {str(e)}"
            errors.append(error_msg)
            print(f"[{i:4d}/{len(png_files)}] ERROR: {error_msg}")
    
    return success_count, error_count, errors

def main():
    """Main function to separate .png files."""
    print("PNG File Separation Tool")
    print("=" * 60)
    
    # First, scan for .png files
    print("1. Scanning for .png files...")
    png_files = find_png_files("Convert raw data")
    
    if not png_files:
        print("No .png files found in 'Convert raw data' directory.")
        return
    
    print(f"Found {len(png_files)} .png files to separate.")
    print("\nFirst 10 files to be copied:")
    for i, file in enumerate(png_files[:10], 1):
        rel_path = os.path.relpath(file, "Convert raw data")
        print(f"  {i:2d}. {rel_path}")
    if len(png_files) > 10:
        print(f"  ... and {len(png_files) - 10} more files")
    
    print("\n" + "=" * 60)
    print("SEPARATION OPTIONS:")
    print("1. Copy .png files to 'PNG_Files' folder (keep originals)")
    print("2. Move .png files to 'PNG_Files' folder (delete originals)")
    print("3. Cancel")
    print("=" * 60)
    
    # Ask for separation option
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            if choice == '1':
                move_files = False
                break
            elif choice == '2':
                move_files = True
                break
            elif choice == '3':
                print("Separation cancelled.")
                return
            else:
                print("Please enter 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\nSeparation cancelled.")
            return
    
    # Perform the separation
    print(f"\n2. {'Moving' if move_files else 'Copying'} .png files to 'PNG_Files' folder...")
    print("=" * 60)
    
    success_count, error_count, errors = separate_png_files("Convert raw data", "PNG_Files")
    
    # If moving files, delete originals after successful copy
    if move_files and success_count > 0:
        print(f"\n3. Deleting original .png files...")
        print("=" * 60)
        
        deleted_count = 0
        for png_path in png_files:
            try:
                if os.path.exists(png_path):
                    os.remove(png_path)
                    deleted_count += 1
                    if deleted_count % 100 == 0:  # Show progress every 100 files
                        print(f"Deleted {deleted_count} original files...")
            except Exception as e:
                print(f"Warning: Could not delete {png_path}: {str(e)}")
        
        print(f"Deleted {deleted_count} original .png files.")
    
    # Show results
    print("\n" + "=" * 60)
    print("SEPARATION SUMMARY:")
    print(f"Successfully {'moved' if move_files else 'copied'}: {success_count} files")
    print(f"Errors: {error_count} files")
    print(f"Destination: PNG_Files/")
    
    if errors:
        print(f"\nErrors encountered (showing first 10):")
        for error in errors[:10]:
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
    
    if success_count > 0:
        print(f"\n✓ Successfully {'moved' if move_files else 'copied'} {success_count} .png files to PNG_Files/!")
        print("✓ Directory structure has been preserved.")
    
    if error_count > 0:
        print(f"\n⚠ {error_count} files could not be processed. Check the errors above.")

if __name__ == "__main__":
    main()
