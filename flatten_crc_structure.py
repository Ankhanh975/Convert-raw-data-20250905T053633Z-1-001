#!/usr/bin/env python3
"""
Script to flatten the deep nested CRC folder structure in Processed directory.
Removes duplicate folder names and the 'images' subfolder.
"""

import os
import shutil
from pathlib import Path

def flatten_crc_structure():
    """Flatten the CRC folder structure by removing duplicate folder names and 'images' subfolder"""
    
    processed_dir = Path("Processed")
    healthy_dir = processed_dir / "healthy"
    tumour_dir = processed_dir / "tumour"
    
    if not processed_dir.exists():
        print("Processed directory not found!")
        return
    
    print("Starting to flatten CRC folder structure...")
    
    # Function to flatten a directory structure
    def flatten_directory(base_dir):
        files_moved = 0
        
        # Walk through all directories
        for root, dirs, files in os.walk(base_dir):
            root_path = Path(root)
            
            # Skip the base directory itself
            if root_path == base_dir:
                continue
            
            # Check if this is a CRC folder with duplicate structure
            path_parts = root_path.relative_to(base_dir).parts
            
            # Look for patterns like: 240911_CRC/240911_CRC/images
            if len(path_parts) >= 3 and path_parts[0] == path_parts[1] and path_parts[2] == "images":
                # This is a duplicate CRC structure with images folder
                crc_name = path_parts[0]  # e.g., "240911_CRC"
                target_dir = base_dir / crc_name
                
                # Create target directory if it doesn't exist
                target_dir.mkdir(parents=True, exist_ok=True)
                
                # Move all PNG files from images folder to the CRC folder
                for file in files:
                    if file.lower().endswith('.png'):
                        source_file = root_path / file
                        target_file = target_dir / file
                        
                        # Handle filename conflicts
                        counter = 1
                        original_target = target_file
                        while target_file.exists():
                            name_parts = original_target.stem, original_target.suffix
                            target_file = target_dir / f"{name_parts[0]}_{counter}{name_parts[1]}"
                            counter += 1
                        
                        try:
                            shutil.move(str(source_file), str(target_file))
                            files_moved += 1
                            print(f"Moved: {source_file} -> {target_file}")
                        except Exception as e:
                            print(f"Error moving {source_file}: {e}")
        
        return files_moved
    
    # Flatten both healthy and tumour directories
    print("\nFlattening healthy directory...")
    healthy_files_moved = flatten_directory(healthy_dir)
    
    print("\nFlattening tumour directory...")
    tumour_files_moved = flatten_directory(tumour_dir)
    
    # Clean up empty directories
    print("\nCleaning up empty directories...")
    cleanup_empty_dirs(healthy_dir)
    cleanup_empty_dirs(tumour_dir)
    
    print(f"\nFlattening complete!")
    print(f"Healthy files moved: {healthy_files_moved}")
    print(f"Tumour files moved: {tumour_files_moved}")
    print(f"Total files moved: {healthy_files_moved + tumour_files_moved}")

def cleanup_empty_dirs(base_dir):
    """Remove empty directories"""
    for root, dirs, files in os.walk(base_dir, topdown=False):
        root_path = Path(root)
        
        # Skip the base directory itself
        if root_path == base_dir:
            continue
        
        # Check if directory is empty
        try:
            if not any(root_path.iterdir()):  # Directory is empty
                root_path.rmdir()
                print(f"Removed empty directory: {root_path}")
        except OSError:
            pass  # Directory not empty or other error

if __name__ == "__main__":
    flatten_crc_structure()
