import os
from PIL import Image
import numpy as np
import sys

def find_tif_files(root_path="."):
    """
    Find all .tif files in the given directory and its subdirectories.
    
    Args:
        root_path (str): The root directory to search in. Defaults to current directory.
    
    Returns:
        list: List of full paths to .tif files
    """
    tif_files = []
    
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.lower().endswith(('.tif', '.tiff')):
                full_path = os.path.join(root, file)
                tif_files.append(full_path)
    
    return tif_files

def convert_tif_to_png(tif_path, png_path):
    """
    Convert a single .tif file to .png format.
    
    Args:
        tif_path (str): Path to the input .tif file
        png_path (str): Path to the output .png file
    
    Returns:
        bool: True if conversion successful, False otherwise
    """
    try:
        with Image.open(tif_path) as img:
            # Handle floating point mode 'F' which PNG doesn't support
            if img.mode == 'F':
                # Convert to numpy array, normalize to 0-255, then back to PIL
                img_array = np.array(img)
                if img_array.size > 0:  # Check if array is not empty
                    img_array = ((img_array - img_array.min()) / (img_array.max() - img_array.min()) * 255).astype(np.uint8)
                    img = Image.fromarray(img_array, mode='L')
                else:
                    img = img.convert('L')
            # Convert to RGB if necessary (PNG doesn't support some TIFF modes)
            elif img.mode in ('RGBA', 'LA', 'P'):
                # Keep transparency for RGBA and LA modes
                img.save(png_path, 'PNG')
                return True
            elif img.mode == 'P':
                # Convert palette mode to RGBA to preserve transparency
                img = img.convert('RGBA')
                img.save(png_path, 'PNG')
                return True
            else:
                # Convert other modes to RGB
                img = img.convert('RGB')
            
            # Save the converted image
            img.save(png_path, 'PNG')
        return True
    except Exception as e:
        print(f"Error converting {tif_path}: {str(e)}")
        return False

def convert_all_tif_to_png(root_path=".", delete_original=False):
    """
    Convert all .tif files to .png format in the given directory and its subdirectories.
    
    Args:
        root_path (str): The root directory to search in. Defaults to current directory.
        delete_original (bool): If True, delete the original .tif files after conversion.
    
    Returns:
        tuple: (success_count, error_count, errors)
    """
    tif_files = find_tif_files(root_path)
    success_count = 0
    error_count = 0
    errors = []
    
    if not tif_files:
        print("No .tif files found.")
        return 0, 0, []
    
    print(f"Found {len(tif_files)} .tif files to convert.")
    print("=" * 60)
    
    for i, tif_path in enumerate(tif_files, 1):
        try:
            # Create the output .png path
            png_path = os.path.splitext(tif_path)[0] + '.png'
            
            # Convert the file
            if convert_tif_to_png(tif_path, png_path):
                print(f"[{i:4d}/{len(tif_files)}] Converted: {os.path.basename(tif_path)} -> {os.path.basename(png_path)}")
                success_count += 1
                
                # Delete original if requested
                if delete_original:
                    try:
                        os.remove(tif_path)
                        print(f"                    Deleted original: {os.path.basename(tif_path)}")
                    except Exception as e:
                        print(f"                    Warning: Could not delete original {tif_path}: {str(e)}")
            else:
                error_count += 1
                errors.append(f"Failed to convert: {tif_path}")
                
        except Exception as e:
            error_count += 1
            error_msg = f"Error processing {tif_path}: {str(e)}"
            errors.append(error_msg)
            print(f"[{i:4d}/{len(tif_files)}] ERROR: {error_msg}")
    
    return success_count, error_count, errors

def main():
    """Main function to convert .tif files to .png."""
    print("TIFF to PNG Conversion Tool")
    print("=" * 60)
    
    # Check if PIL is available
    try:
        from PIL import Image
    except ImportError:
        print("ERROR: PIL (Pillow) is not installed.")
        print("Please install it using: pip install Pillow")
        return
    
    # First, scan for .tif files
    print("1. Scanning for .tif files...")
    tif_files = find_tif_files("Convert raw data")
    
    if not tif_files:
        print("No .tif files found in 'Convert raw data' directory.")
        return
    
    print(f"Found {len(tif_files)} .tif files to convert.")
    print("\nFirst 10 files to be converted:")
    for i, file in enumerate(tif_files[:10], 1):
        print(f"  {i:2d}. {file}")
    if len(tif_files) > 10:
        print(f"  ... and {len(tif_files) - 10} more files")
    
    print("\n" + "=" * 60)
    print("CONVERSION OPTIONS:")
    print("1. Convert .tif to .png (keep original .tif files)")
    print("2. Convert .tif to .png (delete original .tif files)")
    print("3. Cancel")
    print("=" * 60)
    
    # Ask for conversion option
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            if choice == '1':
                delete_original = False
                break
            elif choice == '2':
                delete_original = True
                break
            elif choice == '3':
                print("Conversion cancelled.")
                return
            else:
                print("Please enter 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\nConversion cancelled.")
            return
    
    # Perform the conversion
    print(f"\n2. Converting .tif files to .png...")
    if delete_original:
        print("   (Original .tif files will be deleted after conversion)")
    print("=" * 60)
    
    success_count, error_count, errors = convert_all_tif_to_png("Convert raw data", delete_original)
    
    # Show results
    print("\n" + "=" * 60)
    print("CONVERSION SUMMARY:")
    print(f"Successfully converted: {success_count} files")
    print(f"Errors: {error_count} files")
    
    if errors:
        print(f"\nErrors encountered (showing first 10):")
        for error in errors[:10]:
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
    
    if success_count > 0:
        print(f"\n✓ Successfully converted {success_count} .tif files to .png!")
        if delete_original:
            print("✓ Original .tif files have been deleted.")
    
    if error_count > 0:
        print(f"\n⚠ {error_count} files could not be converted. Check the errors above.")

if __name__ == "__main__":
    main()
