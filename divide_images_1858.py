"""
Image Division Script for 1858 Files
Divides 128x128 images from Processed_1858 folder into 16 pieces of 32x32 pixels each
Creates a new 'Processed_1858_divided' folder with the same structure
"""

import os
import shutil
from PIL import Image
import numpy as np

def divide_image(image_path, output_dir, base_filename):
    """
    Divide a 128x128 image into 16 pieces of 32x32 pixels
    
    Args:
        image_path: Path to the original image
        output_dir: Directory to save divided images
        base_filename: Base filename without extension
    """
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Ensure image is 128x128
        if img.size != (128, 128):
            print(f"Warning: {image_path} is not 128x128, resizing...")
            img = img.resize((128, 128))
        
        # Convert to RGB if needed (in case of grayscale)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Divide into 16 pieces (4x4 grid)
        piece_size = 32
        pieces = []
        
        for row in range(4):
            for col in range(4):
                # Calculate crop coordinates
                left = col * piece_size
                top = row * piece_size
                right = left + piece_size
                bottom = top + piece_size
                
                # Crop the piece
                piece = img.crop((left, top, right, bottom))
                
                # Create filename for this piece
                piece_filename = f"{base_filename}_piece_{row*4 + col + 1:02d}.png"
                piece_path = os.path.join(output_dir, piece_filename)
                
                # Save the piece
                piece.save(piece_path, 'PNG')
                pieces.append(piece_path)
        
        print(f"Divided {image_path} into 16 pieces")
        return len(pieces)
        
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return 0

def process_folder_structure():
    """
    Process the entire Processed_1858 folder structure and create Processed_1858_divided folder
    """
    source_dir = "Processed_1858"
    target_dir = "Processed_1858_divided"
    
    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' not found!")
        print("Please run the filter_1858_files.py script first to create Processed_1858 folder.")
        return
    
    # Create target directory
    if os.path.exists(target_dir):
        print(f"Target directory '{target_dir}' already exists. Removing...")
        shutil.rmtree(target_dir)
    
    os.makedirs(target_dir, exist_ok=True)
    print(f"Created target directory: {target_dir}")
    
    # Process each category (healthy, tumour)
    categories = ['healthy', 'tumour']
    total_images = 0
    total_pieces = 0
    
    for category in categories:
        category_source = os.path.join(source_dir, category)
        category_target = os.path.join(target_dir, category)
        
        if not os.path.exists(category_source):
            print(f"Warning: Category '{category}' not found in source directory")
            continue
        
        print(f"\nProcessing {category} category...")
        os.makedirs(category_target, exist_ok=True)
        
        # Walk through all subdirectories in the category
        for root, dirs, files in os.walk(category_source):
            # Calculate relative path from category source
            rel_path = os.path.relpath(root, category_source)
            
            # Create corresponding directory in target
            if rel_path != '.':
                target_subdir = os.path.join(category_target, rel_path)
                os.makedirs(target_subdir, exist_ok=True)
            else:
                target_subdir = category_target
            
            # Process all PNG files in current directory
            png_files = [f for f in files if f.lower().endswith('.png')]
            
            for png_file in png_files:
                source_path = os.path.join(root, png_file)
                
                # Create base filename without extension
                base_filename = os.path.splitext(png_file)[0]
                
                # Divide the image
                pieces_created = divide_image(source_path, target_subdir, base_filename)
                
                if pieces_created > 0:
                    total_images += 1
                    total_pieces += pieces_created
    
    print(f"\nDivision completed!")
    print(f"Total images processed: {total_images}")
    print(f"Total pieces created: {total_pieces}")
    print(f"Average pieces per image: {total_pieces/total_images if total_images > 0 else 0:.1f}")
    
    return total_images, total_pieces

def verify_division():
    """
    Verify that the division was successful by checking a few sample pieces
    """
    print("\nVerifying division...")
    
    divided_dir = "Processed_1858_divided"
    if not os.path.exists(divided_dir):
        print("Processed_1858_divided directory not found!")
        return
    
    # Check each category
    for category in ['healthy', 'tumour']:
        category_dir = os.path.join(divided_dir, category)
        if not os.path.exists(category_dir):
            continue
        
        print(f"\nChecking {category} category:")
        
        # Count pieces in each subdirectory
        for root, dirs, files in os.walk(category_dir):
            png_files = [f for f in files if f.lower().endswith('.png')]
            if png_files:
                rel_path = os.path.relpath(root, category_dir)
                print(f"  {rel_path}: {len(png_files)} pieces")
                
                # Check dimensions of first piece
                if png_files:
                    first_piece = os.path.join(root, png_files[0])
                    try:
                        img = Image.open(first_piece)
                        print(f"    Sample piece size: {img.size}")
                    except Exception as e:
                        print(f"    Error checking piece: {e}")

def main():
    """
    Main function to run the image division process
    """
    print("Image Division Script for 1858 Files")
    print("=" * 50)
    print("This script will divide 128x128 images into 16 pieces of 32x32 pixels each")
    print("Source: Processed_1858 folder")
    print("Target: Processed_1858_divided folder")
    print("=" * 50)
    
    # Process the folder structure
    total_images, total_pieces = process_folder_structure()
    
    # Verify the results
    verify_division()
    
    print(f"\nScript completed successfully!")
    print(f"Created Processed_1858_divided with {total_pieces} pieces from {total_images} images")

if __name__ == "__main__":
    main()
