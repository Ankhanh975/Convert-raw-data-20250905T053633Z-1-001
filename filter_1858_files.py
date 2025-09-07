"""
Filter 1858 Files Script
Copies files containing "1858" in their names from PNG_Files to PNG_Files_1858
Maintains the same folder structure
"""

import os
import shutil
from pathlib import Path

def filter_files_with_1858(source_dir="Processed", target_dir="Processed_1858"):
    """
    Copy files containing "1858" in their names from source to target directory
    
    Args:
        source_dir: Source directory to search
        target_dir: Target directory to create
    """
    
    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' not found!")
        return
    
    # Create target directory
    if os.path.exists(target_dir):
        print(f"Target directory '{target_dir}' already exists. Removing...")
        shutil.rmtree(target_dir)
    
    os.makedirs(target_dir, exist_ok=True)
    print(f"Created target directory: {target_dir}")
    
    # Statistics
    total_files_found = 0
    total_files_copied = 0
    files_by_category = {}
    
    # Walk through all files in source directory
    for root, dirs, files in os.walk(source_dir):
        # Calculate relative path from source directory
        rel_path = os.path.relpath(root, source_dir)
        
        # Create corresponding directory in target
        if rel_path != '.':
            target_subdir = os.path.join(target_dir, rel_path)
            os.makedirs(target_subdir, exist_ok=True)
        else:
            target_subdir = target_dir
        
        # Process all PNG files in current directory
        png_files = [f for f in files if f.lower().endswith('.png')]
        
        for png_file in png_files:
            total_files_found += 1
            
            # Check if filename contains "1858"
            if "1858" in png_file:
                source_path = os.path.join(root, png_file)
                target_path = os.path.join(target_subdir, png_file)
                
                try:
                    # Copy the file
                    shutil.copy2(source_path, target_path)
                    total_files_copied += 1
                    
                    # Track by category (healthy/tumour)
                    if 'healthy' in rel_path:
                        category = 'healthy'
                    elif 'tumour' in rel_path:
                        category = 'tumour'
                    else:
                        category = 'other'
                    
                    if category not in files_by_category:
                        files_by_category[category] = 0
                    files_by_category[category] += 1
                    
                    print(f"Copied: {rel_path}/{png_file}")
                    
                except Exception as e:
                    print(f"Error copying {source_path}: {e}")
    
    # Print summary
    print(f"\nFiltering completed!")
    print(f"Total PNG files found: {total_files_found}")
    print(f"Files with '1858' copied: {total_files_copied}")
    print(f"Filtering ratio: {total_files_copied/total_files_found*100:.1f}%")
    
    print(f"\nFiles by category:")
    for category, count in files_by_category.items():
        print(f"  {category}: {count} files")
    
    return total_files_copied, files_by_category

def verify_filtered_files(target_dir="Processed_1858"):
    """
    Verify the filtered files and show directory structure
    """
    print(f"\nVerifying filtered files in '{target_dir}'...")
    
    if not os.path.exists(target_dir):
        print(f"Target directory '{target_dir}' not found!")
        return
    
    # Count files in each subdirectory
    total_files = 0
    for root, dirs, files in os.walk(target_dir):
        png_files = [f for f in files if f.lower().endswith('.png')]
        if png_files:
            rel_path = os.path.relpath(root, target_dir)
            print(f"  {rel_path}: {len(png_files)} files")
            total_files += len(png_files)
    
    print(f"\nTotal files in filtered directory: {total_files}")
    
    # Show some sample filenames
    print(f"\nSample filenames:")
    sample_count = 0
    for root, dirs, files in os.walk(target_dir):
        png_files = [f for f in files if f.lower().endswith('.png')]
        for png_file in png_files[:3]:  # Show first 3 files from each directory
            rel_path = os.path.relpath(root, target_dir)
            print(f"  {rel_path}/{png_file}")
            sample_count += 1
            if sample_count >= 10:  # Limit to 10 samples
                break
        if sample_count >= 10:
            break

def main():
    """
    Main function to run the filtering process
    """
    print("Filter 1858 Files Script")
    print("=" * 50)
    print("This script will copy files containing '1858' in their names")
    print("Source: Processed folder")
    print("Target: Processed_1858 folder")
    print("=" * 50)
    
    # Filter the files
    total_copied, category_counts = filter_files_with_1858()
    
    # Verify the results
    verify_filtered_files()
    
    print(f"\nScript completed successfully!")
    print(f"Created Processed_1858 with {total_copied} filtered files")

if __name__ == "__main__":
    main()
