import os

# Find and delete files with weight_2 or weight_3
deleted_count = 0
for root, dirs, files in os.walk('.'):
    for file in files:
        if 'weight_2' in file or 'weight_3' in file:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f"Deleted: {file}")
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting {file}: {e}")

print(f"\nTotal deleted: {deleted_count} files")
