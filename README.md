# Data Processing Scripts

This repository contains Python scripts for processing and organizing image data files. The scripts were created to handle TIFF to PNG conversion, folder organization, and file management tasks.

## Scripts Overview

### 1. `count_magnitute_folders.py`
**Purpose:** Count folders named "Magnitude" in the workspace
- Scans recursively through all directories
- Lists all found Magnitude folders with full paths
- Provides total count summary

### 2. `delete_magnitude_folders.py`
**Purpose:** Delete all folders named "Magnitude" and their contents
- **Safety Features:** Confirmation prompt, progress tracking, error handling
- **Successfully deleted:** 51 Magnitude folders
- Includes dry-run capability for testing

### 3. `count_phase_folders.py`
**Purpose:** Count folders named "Phase" in the workspace
- Similar functionality to magnitude counter
- Scans for Phase folders recursively

### 4. `delete_phase_folders.py`
**Purpose:** Delete all folders named "Phase" and their contents
- **Safety Features:** Confirmation prompt, progress tracking, error handling
- **Successfully deleted:** 51 Phase folders
- Includes dry-run capability for testing

### 5. `convert_tif_to_png.py`
**Purpose:** Convert TIFF files to PNG format
- **Key Features:**
  - Handles floating point mode 'F' TIFF files (converts to normalized grayscale)
  - Preserves transparency for RGBA/LA modes
  - Converts palette mode to RGBA
  - **Successfully converted:** 4,672 TIFF files to PNG
- **Dependencies:** PIL (Pillow), numpy

### 6. `test_convert.py`
**Purpose:** Minimal test script for TIFF to PNG conversion
- Tests conversion of individual files
- Shows image properties (mode, size, format)
- Handles floating point mode conversion

### 7. `separate_png_files.py`
**Purpose:** Move PNG files to separate folder while preserving directory structure
- **Features:**
  - Copies all PNG files to `PNG_Files/` directory
  - Maintains original folder hierarchy
  - Option to move or copy files
  - Fixed to handle nested folders properly

### 8. `delete_weight_files.py`
**Purpose:** Delete files containing "weight_2" or "weight_3" in their names
- **Safety Features:** Confirmation prompt, error handling
- Scans all file types recursively

### 9. `delete_mix_folders.py`
**Purpose:** Delete folders containing "Mix" in their names (case insensitive)
- **Safety Features:** Confirmation prompt, progress tracking
- Handles case-insensitive matching

### 10. `move_reflection_coefficient.py`
**Purpose:** Move files from "Reflection Coefficient" folders to parent directories
- **Features:**
  - Moves all files from Reflection Coefficient subfolders to parent
  - Deletes empty Reflection Coefficient folders
  - Handles filename conflicts with automatic renaming
  - Modified to work specifically on PNG_Files folder

### 11. `process_250521_folder.py`
**Purpose:** Process specific 250521 folder structure
- **Features:**
  - Removes existing 'images' folder
  - Renames '250521_CRC_Healthy' folder to 'images'
  - Handles folder conflicts and provides detailed progress
  - Works on specific hardcoded path

### 12. `delete_post_files.py`
**Purpose:** Delete files containing "__post" in their names from PNG_Files
- **Features:**
  - Scans PNG_Files directory recursively
  - Removes all files with "__post" in filename
  - Safety confirmation before deletion
  - Progress tracking and error handling

### 13. `print_folder_structure.py`
**Purpose:** Print beautiful tree-like folder structure
- **Features:**
  - Multiple display options (all files, folders only, specific file types)
  - Customizable depth limits
  - Tree visualization with emojis (📁 for folders, 📄 for files)
  - Interactive menu for different views

### 14. `rename_folders.py`
**Purpose:** Rename folders in PNG_Files directory
- **Features:**
  - Renames folders containing "tumor" to "tumour" (case insensitive)
  - Standardizes "healthy" folder names
  - Handles patterns like "241108_CRC_Tumour" → "tumour"
  - Works only within PNG_Files directory

### 15. `consolidate_png_files.py`
**Purpose:** Consolidate PNG files from various folders into a single Processed folder
- **Features:**
  - Creates Processed/healthy and Processed/tumour directories
  - Preserves original folder structure within each category
  - Handles CRC folders with nested structures (e.g., 240911_CRC/240911_CRC/healthy/images/)
  - Handles the "heathy" typo in folder names
  - Copies all PNG files while maintaining folder hierarchy
  - Provides detailed progress tracking and error handling

### 16. `flatten_crc_structure.py`
**Purpose:** Flatten the deep nested CRC folder structure in Processed directory
- **Features:**
  - Removes duplicate folder names (e.g., 240911_CRC/240911_CRC → 240911_CRC)
  - Removes the "images" subfolder and moves files up one level
  - Handles filename conflicts with automatic renaming
  - Cleans up empty directories after flattening
  - Works on both healthy and tumour directories

### 17. `count_png_files.py`
**Purpose:** Count PNG files in both original PNG_Files and Processed directories
- **Features:**
  - Compares file counts to ensure no files were missed during processing
  - Provides detailed breakdown by category and folder
  - Identifies missing or extra categories
  - Shows comprehensive comparison results
  - Helps verify data integrity after consolidation and flattening

## Usage Examples

### Convert TIFF to PNG
```bash
python convert_tif_to_png.py
```

### Delete specific folders
```bash
python delete_magnitude_folders.py
python delete_phase_folders.py
```

### Organize PNG files
```bash
python separate_png_files.py
```

### Move files from subfolders
```bash
python move_reflection_coefficient.py
```

### Process specific folder
```bash
python process_250521_folder.py
```

### Delete specific files
```bash
python delete_post_files.py
```

### Print folder structure
```bash
python print_folder_structure.py
```

### Rename folders
```bash
python rename_folders.py
```

### Consolidate PNG files
```bash
python consolidate_png_files.py
```

### Flatten CRC structure
```bash
python flatten_crc_structure.py
```

### Count and verify files
```bash
python count_png_files.py
```

## Dependencies

- **PIL (Pillow)** - Image processing
- **numpy** - Array operations for floating point conversion
- **os** - File system operations
- **shutil** - File operations

## Safety Features

All deletion and modification scripts include:
- **Confirmation prompts** before destructive operations
- **Progress tracking** with file counts
- **Error handling** with detailed error messages
- **Dry-run capabilities** for testing (where applicable)

## Results Summary

- **102 folders deleted** (51 Magnitude + 51 Phase)
- **4,672 files converted** from TIFF to PNG format
- **All PNG files organized** into PNG_Files directory structure
- **Folder structure cleaned** with standardized naming (tumour/healthy)
- **Specific folder processing** for 250521 directory
- **Post files removed** from PNG_Files
- **Repository cleaned up** with proper .gitignore

## Total Scripts Created

**17 Python scripts** for comprehensive data processing and organization:
1. `count_magnitute_folders.py` - Count Magnitude folders
2. `delete_magnitude_folders.py` - Delete Magnitude folders
3. `count_phase_folders.py` - Count Phase folders
4. `delete_phase_folders.py` - Delete Phase folders
5. `convert_tif_to_png.py` - Convert TIFF to PNG
6. `test_convert.py` - Test conversion
7. `separate_png_files.py` - Organize PNG files
8. `delete_weight_files.py` - Delete weight files
9. `delete_mix_folders.py` - Delete Mix folders
10. `move_reflection_coefficient.py` - Move Reflection Coefficient files
11. `process_250521_folder.py` - Process specific folder
12. `delete_post_files.py` - Delete post files
13. `print_folder_structure.py` - Print folder structure
14. `rename_folders.py` - Rename folders
15. `consolidate_png_files.py` - Consolidate PNG files into Processed folder
16. `flatten_crc_structure.py` - Flatten CRC folder structure
17. `count_png_files.py` - Count and verify PNG files

## File Structure

```
├── Convert raw data/          # Original data directory
├── PNG_Files/                # Separated PNG files
├── *.py                      # Processing scripts
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## Notes

- All scripts are designed to be run from the project root directory
- Scripts include comprehensive error handling and user feedback
- The conversion process properly handles floating point TIFF data by normalizing to 0-255 range
- Directory structures are preserved during file operations
