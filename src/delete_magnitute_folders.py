#!/usr/bin/env python3
"""
Recursively delete all folders named 'magnitute' (case-insensitive).
"""

import os
import shutil
import sys

def find_magnitute_folders_recursive(directory):
    """Recursively search and print paths of 'magnitute' folders."""
    found_count = 0
    
    if not os.path.exists(directory):
        return found_count
    
    try:
        items = os.listdir(directory)
        
        for item in items:
            item_path = os.path.join(directory, item)
            
            if os.path.isdir(item_path):
                if item.lower() == "magnitute":
                    print(item_path)
                    found_count += 1
                else:
                    found_count += find_magnitute_folders_recursive(item_path)
    
    except:
        pass
    
    return found_count

def main():
    search_path = sys.argv[1] if len(sys.argv) > 1 else "."
    
    if not os.path.exists(search_path):
        return
    
    found = find_magnitute_folders_recursive(search_path)
    print(f"Total: {found}")

if __name__ == "__main__":
    main()