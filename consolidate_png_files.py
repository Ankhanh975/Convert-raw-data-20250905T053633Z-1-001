#!/usr/bin/env python3
"""
Script to consolidate PNG files from various folders into a single Processed folder
with only healthy and tumour subfolders, preserving the original folder structure.
"""

import os
import shutil
from pathlib import Path

def consolidate_png_files():
    """Consolidate all PNG files from PNG_Files into Processed/healthy and Processed/tumour
    while preserving the original folder structure within each category."""
    
    # Define source and destination paths
    source_dir = Path("PNG_Files")
    dest_dir = Path("Processed")
    healthy_dir = dest_dir / "healthy"
    tumour_dir = dest_dir / "tumour"
    
    # Create destination directories
    healthy_dir.mkdir(parents=True, exist_ok=True)
    tumour_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Created destination directories: {healthy_dir} and {tumour_dir}")
    
    # Counters for tracking
    healthy_files_copied = 0
    tumour_files_copied = 0
    
    # Function to copy files while preserving folder structure
    def copy_files_with_structure(source_path, source_dir, dest_base_dir, file_type):
        nonlocal healthy_files_copied, tumour_files_copied
        
        if source_path.is_file() and source_path.suffix.lower() == '.png':
            # Get the relative path from PNG_Files
            relative_path = source_path.relative_to(source_dir)
            
            # Find the position of 'healthy', 'tumour', or 'heathy' in the path
            path_parts = relative_path.parts
            category_index = -1
            
            for i, part in enumerate(path_parts):
                if part in ['healthy', 'tumour', 'heathy']:  # Include the typo
                    category_index = i
                    break
            
            if category_index == -1:
                print(f"Warning: Could not determine category for {source_path}")
                return
            
            # Get the folder structure before the category (healthy/tumour)
            folder_structure = path_parts[:category_index]
            
            # Get the path after the category
            remaining_path = path_parts[category_index + 1:]
            
            # Create the destination path
            if folder_structure:
                dest_folder = dest_base_dir / Path(*folder_structure)
            else:
                dest_folder = dest_base_dir
            
            # Add any remaining subfolders (like 'images')
            if remaining_path:
                dest_folder = dest_folder / Path(*remaining_path[:-1])  # Exclude filename
            
            # Create the destination directory
            dest_folder.mkdir(parents=True, exist_ok=True)
            
            # Copy the file
            dest_file_path = dest_folder / source_path.name
            
            try:
                shutil.copy2(source_path, dest_file_path)
                if file_type == "healthy":
                    healthy_files_copied += 1
                else:
                    tumour_files_copied += 1
                print(f"Copied: {source_path} -> {dest_file_path}")
            except Exception as e:
                print(f"Error copying {source_path}: {e}")
    
    # Walk through all directories in PNG_Files
    for root, dirs, files in os.walk(source_dir):
        root_path = Path(root)
        
        # Skip the root PNG_Files directory itself
        if root_path == source_dir:
            continue
            
        # Check if this directory contains PNG files
        png_files = [f for f in files if f.lower().endswith('.png')]
        
        if png_files:
            # Determine if this is a healthy or tumour directory
            if 'healthy' in root_path.parts:
                for png_file in png_files:
                    file_path = root_path / png_file
                    copy_files_with_structure(file_path, source_dir, healthy_dir, "healthy")
            elif 'tumour' in root_path.parts:
                for png_file in png_files:
                    file_path = root_path / png_file
                    copy_files_with_structure(file_path, source_dir, tumour_dir, "tumour")
            elif 'heathy' in root_path.parts:  # Handle the typo in folder name
                for png_file in png_files:
                    file_path = root_path / png_file
                    copy_files_with_structure(file_path, source_dir, healthy_dir, "healthy")
            else:
                # Debug: print any directories we might be missing
                print(f"Warning: Directory with PNG files but no category found: {root_path}")
                print(f"  Path parts: {root_path.parts}")
                print(f"  PNG files: {png_files}")
    
    print(f"\nConsolidation complete!")
    print(f"Healthy files copied: {healthy_files_copied}")
    print(f"Tumour files copied: {tumour_files_copied}")
    print(f"Total files processed: {healthy_files_copied + tumour_files_copied}")

if __name__ == "__main__":
    consolidate_png_files()
