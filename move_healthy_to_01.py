import os
import shutil

def move_healthy_to_01():
    """
    Move PNG_Files/healthy to PNG_Files/01/healthy
    """
    source_path = "PNG_Files/healthy"
    dest_dir = "PNG_Files/01"
    dest_path = "PNG_Files/01/healthy"
    
    print("Moving healthy folder to 01 directory...")
    print("=" * 60)
    print(f"Source: {source_path}")
    print(f"Destination: {dest_path}")
    print("=" * 60)
    
    # Check if source exists
    if not os.path.exists(source_path):
        print(f"❌ Source folder does not exist: {source_path}")
        return False
    
    # Check if source is a directory
    if not os.path.isdir(source_path):
        print(f"❌ Source is not a directory: {source_path}")
        return False
    
    try:
        # Create destination directory if it doesn't exist
        if not os.path.exists(dest_dir):
            print(f"📁 Creating directory: {dest_dir}")
            os.makedirs(dest_dir)
        
        # Check if destination already exists
        if os.path.exists(dest_path):
            print(f"⚠️  Destination already exists: {dest_path}")
            response = input("Do you want to overwrite it? (yes/no): ").lower().strip()
            if response not in ['yes', 'y']:
                print("Operation cancelled.")
                return False
            
            # Remove existing destination
            print(f"🗑️  Removing existing destination: {dest_path}")
            shutil.rmtree(dest_path)
        
        # Move the folder
        print(f"📦 Moving {source_path} to {dest_path}")
        shutil.move(source_path, dest_path)
        
        print("✅ Successfully moved healthy folder to 01/healthy")
        return True
        
    except Exception as e:
        print(f"❌ Error moving folder: {str(e)}")
        return False

def main():
    """Main function to move healthy folder."""
    print("Healthy Folder Mover")
    print("=" * 60)
    print("This script will move PNG_Files/healthy to PNG_Files/01/healthy")
    print("=" * 60)
    
    # Check current structure
    print("Current PNG_Files structure:")
    if os.path.exists("PNG_Files"):
        for item in sorted(os.listdir("PNG_Files")):
            item_path = os.path.join("PNG_Files", item)
            if os.path.isdir(item_path):
                print(f"  📁 {item}")
            else:
                print(f"  📄 {item}")
    else:
        print("  PNG_Files directory not found")
        return
    
    print("\n" + "=" * 60)
    
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
    
    # Perform the move
    success = move_healthy_to_01()
    
    if success:
        print("\n" + "=" * 60)
        print("Final PNG_Files structure:")
        if os.path.exists("PNG_Files"):
            for item in sorted(os.listdir("PNG_Files")):
                item_path = os.path.join("PNG_Files", item)
                if os.path.isdir(item_path):
                    print(f"  📁 {item}")
                    # Show subdirectories
                    if item == "01" and os.path.exists("PNG_Files/01"):
                        for subitem in sorted(os.listdir("PNG_Files/01")):
                            print(f"    📁 {subitem}")
                else:
                    print(f"  📄 {item}")
        
        print("\n✅ Operation completed successfully!")
    else:
        print("\n❌ Operation failed. Check the errors above.")

if __name__ == "__main__":
    main()
