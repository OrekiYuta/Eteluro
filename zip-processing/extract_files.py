import os
import shutil

# Read source directory from a text file
with open("extract_file_path.txt", "r", encoding="utf-8") as f:
    base_dir = f.readline().strip()

# Define target directory inside the source directory
target_dir = os.path.join(base_dir, "load")

# Create target directory if it doesn't exist
os.makedirs(target_dir, exist_ok=True)

# Traverse source directory and its subdirectories
for root, _, files in os.walk(base_dir):
    for file in files:
        source_file = os.path.join(root, file)
        target_file = os.path.join(target_dir, file)

        # Skip if the file is already in the target directory
        if source_file == target_file or os.path.exists(target_file):
            continue

        # Move the file to the target directory
        shutil.move(source_file, target_file)
        print(f'Moved: {source_file} -> {target_file}')

print("All files have been moved.")
