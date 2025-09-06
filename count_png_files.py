#!/usr/bin/env python3
"""
Script to count PNG files in both original PNG_Files and Processed directories
to ensure no files were missed during consolidation and flattening.
"""

import os
from pathlib import Path
from collections import defaultdict

def count_png_files():
    """Count PNG files in both directories and compare"""
    
    print("Counting PNG files in original PNG_Files directory...")
    original_counts = count_directory_files("PNG_Files")
    
    print("\nCounting PNG files in Processed directory...")
    processed_counts = count_directory_files("Processed")
    
    print("\n" + "="*60)
    print("COMPARISON RESULTS")
    print("="*60)
    
    # Compare total counts
    original_total = sum(original_counts.values())
    processed_total = sum(processed_counts.values())
    
    print(f"Original PNG_Files total: {original_total}")
    print(f"Processed total: {processed_total}")
    print(f"Difference: {processed_total - original_total}")
    
    if original_total == processed_total:
        print("✅ SUCCESS: All files were copied correctly!")
    else:
        print("❌ WARNING: File count mismatch!")
    
    print("\n" + "="*60)
    print("DETAILED BREAKDOWN")
    print("="*60)
    
    # Show breakdown by category
    print("\nOriginal files by category:")
    for category, count in sorted(original_counts.items()):
        print(f"  {category}: {count}")
    
    print("\nProcessed files by category:")
    for category, count in sorted(processed_counts.items()):
        print(f"  {category}: {count}")
    
    # Check for missing categories
    missing_in_processed = set(original_counts.keys()) - set(processed_counts.keys())
    if missing_in_processed:
        print(f"\n❌ Categories missing in Processed: {missing_in_processed}")
    
    extra_in_processed = set(processed_counts.keys()) - set(original_counts.keys())
    if extra_in_processed:
        print(f"\n⚠️  Extra categories in Processed: {extra_in_processed}")

def count_directory_files(directory):
    """Count PNG files in a directory and categorize them"""
    counts = defaultdict(int)
    total_files = 0
    
    if not Path(directory).exists():
        print(f"Directory {directory} does not exist!")
        return counts
    
    for root, dirs, files in os.walk(directory):
        root_path = Path(root)
        
        # Skip the root directory itself
        if root_path == Path(directory):
            continue
        
        # Count PNG files in this directory
        png_files = [f for f in files if f.lower().endswith('.png')]
        if png_files:
            # Determine category based on path
            relative_path = root_path.relative_to(Path(directory))
            path_parts = relative_path.parts
            
            # Find the category (healthy/tumour)
            category = "unknown"
            for part in path_parts:
                if part in ['healthy', 'tumour', 'heathy']:  # heathy is the typo
                    category = part
                    break
            
            # Get the folder name for more detailed categorization
            if len(path_parts) > 0:
                folder_name = path_parts[0]
                category_key = f"{category}_{folder_name}"
            else:
                category_key = category
            
            counts[category_key] += len(png_files)
            total_files += len(png_files)
            
            print(f"  {root_path}: {len(png_files)} PNG files")
    
    print(f"\nTotal PNG files found: {total_files}")
    return counts

if __name__ == "__main__":
    count_png_files()
