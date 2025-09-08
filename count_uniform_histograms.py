import os
from pathlib import Path
from PIL import Image
import numpy as np

def is_uniform_image(image_path, threshold=0.95):
    img = Image.open(image_path).convert('L')
    arr = np.array(img)
    values, counts = np.unique(arr, return_counts=True)
    max_ratio = counts.max() / arr.size
    return max_ratio >= threshold


def count_uniform_images(img_dir='Processed', threshold=0.99):
    img_dir = Path(img_dir)
    total = 0
    uniform = 0
    uniform_files = []
    for root, dirs, files in os.walk(img_dir):
        for file in files:
            if file.lower().endswith('.png'):
                total += 1
                img_path = Path(root) / file
                if is_uniform_image(img_path, threshold):
                    uniform += 1
                    uniform_files.append(str(img_path))
    print(f"Total PNG images: {total}")
    print(f"Uniform (>= {int(threshold*100)}% single value): {uniform}")
    if uniform_files:
        print("Sample uniform files:")
        for f in uniform_files[:10]:
            print(f"  {f}")
    return uniform, total, uniform_files


if __name__ == '__main__':
    count_uniform_images()
