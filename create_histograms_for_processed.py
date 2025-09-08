import os
from pathlib import Path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Source and destination directories
SRC_DIR = Path('Processed_filtered')
DST_DIR = Path('Processed_histograms')


def save_histogram(image_path, output_path):
    # Load image as grayscale
    img = Image.open(image_path).convert('L')
    arr = np.array(img)
    plt.figure(figsize=(2, 1))  # Smaller size: 2x1 inches
    plt.hist(arr.ravel(), bins=256, range=(0, 255), color='blue', alpha=0.7)
    plt.title('')
    plt.xlabel('')
    plt.ylabel('')
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout(pad=0)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=100, bbox_inches='tight', pad_inches=0)
    plt.close()


def process_all_images():
    for root, dirs, files in os.walk(SRC_DIR):
        for file in files:
            if file.lower().endswith('.png'):
                img_path = Path(root) / file
                rel_path = img_path.relative_to(SRC_DIR)
                hist_path = DST_DIR / rel_path.with_suffix('.hist.png')
                save_histogram(img_path, hist_path)
                print(f"Saved histogram for {img_path} -> {hist_path}")


if __name__ == '__main__':
    process_all_images()
