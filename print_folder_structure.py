import os

def print_folder_structure(root_path=".", max_depth=None, show_files=True, file_extensions=None):
    """
    Print the folder and subfolder structure.
    
    Args:
        root_path (str): The root directory to start from. Defaults to current directory.
        max_depth (int): Maximum depth to traverse. None for unlimited.
        show_files (bool): Whether to show files or just folders.
        file_extensions (list): List of file extensions to include. None for all.
    """
    def print_tree(path, prefix="", depth=0):
        if max_depth is not None and depth > max_depth:
            return
        
        try:
            items = sorted(os.listdir(path))
            dirs = []
            files = []
            
            # Separate directories and files
            for item in items:
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    dirs.append(item)
                elif show_files and os.path.isfile(item_path):
                    # Filter by file extensions if specified
                    if file_extensions is None or any(item.lower().endswith(ext.lower()) for ext in file_extensions):
                        files.append(item)
            
            # Print directories first
            for i, dir_name in enumerate(dirs):
                is_last_dir = (i == len(dirs) - 1) and len(files) == 0
                current_prefix = "└── " if is_last_dir else "├── "
                print(f"{prefix}{current_prefix}📁 {dir_name}")
                
                # Determine next prefix
                next_prefix = prefix + ("    " if is_last_dir else "│   ")
                
                # Recursively print subdirectory
                print_tree(os.path.join(path, dir_name), next_prefix, depth + 1)
            
            # Print files
            for i, file_name in enumerate(files):
                is_last_file = i == len(files) - 1
                current_prefix = "└── " if is_last_file else "├── "
                print(f"{prefix}{current_prefix}📄 {file_name}")
                
        except PermissionError:
            print(f"{prefix}└── ❌ Permission denied")
        except Exception as e:
            print(f"{prefix}└── ❌ Error: {str(e)}")

def main():
    """Main function to print folder structure."""
    print("Folder Structure Printer")
    print("=" * 60)
    
    # Get options from user
    print("Options:")
    print("1. Show all files and folders")
    print("2. Show only folders")
    print("3. Show only Python files")
    print("4. Show only image files (.png, .tiff, .tif)")
    print("5. Custom file extensions")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            if choice in ['1', '2', '3', '4', '5']:
                break
            else:
                print("Please enter 1, 2, 3, 4, or 5.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return
    
    # Set parameters based on choice
    if choice == '1':
        show_files = True
        file_extensions = None
        print("\nShowing all files and folders...")
    elif choice == '2':
        show_files = False
        file_extensions = None
        print("\nShowing only folders...")
    elif choice == '3':
        show_files = True
        file_extensions = ['.py']
        print("\nShowing only Python files...")
    elif choice == '4':
        show_files = True
        file_extensions = ['.png', '.tiff', '.tif']
        print("\nShowing only image files...")
    elif choice == '5':
        show_files = True
        extensions_input = input("Enter file extensions separated by commas (e.g., .py,.txt,.md): ").strip()
        file_extensions = [ext.strip() for ext in extensions_input.split(',') if ext.strip()]
        print(f"\nShowing files with extensions: {file_extensions}")
    
    # Ask for max depth
    while True:
        try:
            depth_input = input("\nEnter maximum depth (or press Enter for unlimited): ").strip()
            if depth_input == "":
                max_depth = None
                break
            else:
                max_depth = int(depth_input)
                if max_depth > 0:
                    break
                else:
                    print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return
    
    # Print the structure
    print("\n" + "=" * 60)
    print("FOLDER STRUCTURE:")
    print("=" * 60)
    
    root_name = os.path.basename(os.path.abspath("."))
    print(f"📁 {root_name}")
    
    print_tree(".", "", 0, max_depth, show_files, file_extensions)
    
    print("\n" + "=" * 60)
    print("Structure printed successfully!")

if __name__ == "__main__":
    main()
