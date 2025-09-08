"""
Generic image divider: splits 128x128 PNGs into 16 pieces of 32x32.

Defaults:
  --src Processed_1858_filtered
  --dst Processed_1858_filtered_divided

Usage:
  python divide_images_generic.py
  python divide_images_generic.py --src Processed_1858 --dst Processed_1858_divided
"""

import os
import shutil
import argparse
from PIL import Image


def divide_image(image_path, output_dir, base_filename):
    try:
        img = Image.open(image_path)
        if img.size != (128, 128):
            img = img.resize((128, 128))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        os.makedirs(output_dir, exist_ok=True)
        piece_size = 32
        pieces_created = 0
        for row in range(4):
            for col in range(4):
                left = col * piece_size
                top = row * piece_size
                right = left + piece_size
                bottom = top + piece_size
                piece = img.crop((left, top, right, bottom))
                piece_filename = f"{base_filename}_piece_{row*4 + col + 1:02d}.png"
                piece.save(os.path.join(output_dir, piece_filename), 'PNG')
                pieces_created += 1
        return pieces_created
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return 0


def process_folder_structure(source_dir, target_dir):
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' not found!")
        return 0, 0
    if os.path.abspath(source_dir) == os.path.abspath(target_dir):
        print("Error: Source and target directories must be different.")
        return 0, 0
    if os.path.exists(target_dir):
        print(f"Target directory '{target_dir}' already exists. Removing...")
        shutil.rmtree(target_dir)
    os.makedirs(target_dir, exist_ok=True)

    categories = ['healthy', 'tumour']
    total_images = 0
    total_pieces = 0

    for category in categories:
        category_source = os.path.join(source_dir, category)
        category_target = os.path.join(target_dir, category)
        if not os.path.exists(category_source):
            print(f"Warning: Category '{category}' not found in source directory")
            continue
        os.makedirs(category_target, exist_ok=True)
        for root, dirs, files in os.walk(category_source):
            rel_path = os.path.relpath(root, category_source)
            target_subdir = category_target if rel_path == '.' else os.path.join(category_target, rel_path)
            os.makedirs(target_subdir, exist_ok=True)
            png_files = [f for f in files if f.lower().endswith('.png')]
            for png_file in png_files:
                source_path = os.path.join(root, png_file)
                base_filename = os.path.splitext(png_file)[0]
                pieces_created = divide_image(source_path, target_subdir, base_filename)
                if pieces_created > 0:
                    total_images += 1
                    total_pieces += pieces_created

    print(f"\nDivision completed!")
    print(f"Total images processed: {total_images}")
    print(f"Total pieces created: {total_pieces}")
    print(f"Average pieces per image: {total_pieces/total_images if total_images else 0:.1f}")
    return total_images, total_pieces


def parse_args():
    parser = argparse.ArgumentParser(description="Divide 128x128 PNG images into 16 pieces.")
    parser.add_argument("--src", default="Processed_1858_filtered", help="Source directory")
    parser.add_argument("--dst", default="Processed_1858_filtered_divided", help="Target directory")
    return parser.parse_args()


def main():
    args = parse_args()
    print("Image Division Script (Generic)")
    print("=" * 50)
    print(f"Source: {args.src}")
    print(f"Target: {args.dst}")
    process_folder_structure(args.src, args.dst)


if __name__ == "__main__":
    main()


