import os
from pathlib import Path
from PIL import Image
import numpy as np
import shutil

def is_uniform_image(image_path, threshold=0.99):
    img = Image.open(image_path).convert('L')
    arr = np.array(img)
    values, counts = np.unique(arr, return_counts=True)
    max_ratio = counts.max() / arr.size
    return max_ratio >= threshold


def filter_uniform_images(src_dir='Processed', dst_dir='Processed_filtered', threshold=0.99):
    src_dir = Path(src_dir)
    dst_dir = Path(dst_dir)
    filtered_count = 0
    total = 0
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.lower().endswith('.png'):
                total += 1
                src_path = Path(root) / file
                if not is_uniform_image(src_path, threshold):
                    rel_path = src_path.relative_to(src_dir)
                    dst_path = dst_dir / rel_path
                    dst_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_path, dst_path)
                    filtered_count += 1
    print(f"Total PNG images processed: {total}")
    print(f"Non-uniform images copied to {dst_dir}: {filtered_count}")
    print(f"Uniform images (filtered out): {total - filtered_count}")


if __name__ == '__main__':
    filter_uniform_images()
