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
- **Repository cleaned up** with proper .gitignore

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
