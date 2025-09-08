"""
Run uniform-image filtering on Processed_1858 with configurable options.

Usage examples:
  python filter_uniform_images_1858.py
  python filter_uniform_images_1858.py --src Processed_1858 --dst Processed_1858_filtered --threshold 0.995
"""

import argparse
from filter_uniform_images import filter_uniform_images


def parse_args():
    parser = argparse.ArgumentParser(description="Filter out uniform PNG images from a dataset.")
    parser.add_argument("--src", default="Processed_1858", help="Source directory containing images")
    parser.add_argument("--dst", default="Processed_1858_filtered", help="Destination directory for non-uniform images")
    parser.add_argument("--threshold", type=float, default=0.99, help="Uniformity threshold (0-1). Higher filters more.")
    return parser.parse_args()


def main():
    args = parse_args()
    filter_uniform_images(src_dir=args.src, dst_dir=args.dst, threshold=args.threshold)


if __name__ == "__main__":
    main()


