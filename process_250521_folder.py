import os
import shutil

def process_250521_folder():
    """
    Process the specific 250521 folder:
    1. Remove the 'images' folder if it exists
    2. Rename '250521_CRC_Healthy' folder to 'images'
    """
    base_path = r"C:\Users\Admin\Downloads\Convert raw data-20250905T053633Z-1-001\PNG_Files\250521\250521_CRC\healthy"
    
    print("Processing 250521 folder...")
    print(f"Target path: {base_path}")
    print("=" * 60)
    
    # Check if the base path exists
    if not os.path.exists(base_path):
        print(f"ERROR: Path does not exist: {base_path}")
        return False
    
    # List current contents
    print("Current folder contents:")
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path):
            print(f"  📁 {item}")
        else:
            print(f"  📄 {item}")
    
    print("\n" + "=" * 60)
    
    success_count = 0
    error_count = 0
    
    # Step 1: Remove 'images' folder if it exists
    images_folder = os.path.join(base_path, "images")
    if os.path.exists(images_folder):
        try:
            shutil.rmtree(images_folder)
            print("✅ Removed 'images' folder")
            success_count += 1
        except Exception as e:
            print(f"❌ Error removing 'images' folder: {e}")
            error_count += 1
    else:
        print("ℹ️  'images' folder not found (nothing to remove)")
    
    # Step 2: Rename '250521_CRC_Healthy' to 'images'
    old_folder = os.path.join(base_path, "250521_CRC_Healthy")
    new_folder = os.path.join(base_path, "images")
    
    if os.path.exists(old_folder):
        try:
            # Check if 'images' already exists after removal
            if os.path.exists(new_folder):
                print(f"⚠️  'images' folder already exists, removing it first...")
                shutil.rmtree(new_folder)
            
            os.rename(old_folder, new_folder)
            print("✅ Renamed '250521_CRC_Healthy' to 'images'")
            success_count += 1
        except Exception as e:
            print(f"❌ Error renaming folder: {e}")
            error_count += 1
    else:
        print("❌ '250521_CRC_Healthy' folder not found")
        error_count += 1
    
    # Show final results
    print("\n" + "=" * 60)
    print("Final folder contents:")
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path):
            print(f"  📁 {item}")
        else:
            print(f"  📄 {item}")
    
    print("\n" + "=" * 60)
    print("PROCESSING SUMMARY:")
    print(f"✅ Successful operations: {success_count}")
    print(f"❌ Errors: {error_count}")
    
    if success_count > 0 and error_count == 0:
        print("\n🎉 Folder processing completed successfully!")
    elif success_count > 0:
        print("\n⚠️  Folder processing completed with some issues.")
    else:
        print("\n❌ Folder processing failed.")
    
    return error_count == 0

def main():
    """Main function to process the 250521 folder."""
    print("250521 Folder Processor")
    print("=" * 60)
    print("This script will:")
    print("1. Remove the 'images' folder (if it exists)")
    print("2. Rename '250521_CRC_Healthy' folder to 'images'")
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
    
    # Process the folder
    success = process_250521_folder()
    
    if success:
        print("\n✅ All operations completed successfully!")
    else:
        print("\n❌ Some operations failed. Check the output above for details.")

if __name__ == "__main__":
    main()
