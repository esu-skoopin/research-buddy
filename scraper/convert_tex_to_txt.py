import os
import subprocess
from tqdm import tqdm
import time

# Base directory where your extracted files are located
BASE_DIR = "/Users/iamsergio/Desktop/arxiv/text/2305"  # Update this to the full path

# Directory to save converted text files
OUTPUT_DIR = os.path.join(BASE_DIR, "converted_text")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def find_main_tex_file(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".tex"):
                return os.path.join(root, file)
    return None

def convert_tex_to_txt(tex_file, output_path, timeout_sec=10):
    """
    Converts a .tex file to plain text using Pandoc with a timeout.
    """
    try:
        result = subprocess.run(['pandoc', tex_file, '-t', 'plain'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, timeout=timeout_sec)
        if result.returncode == 0:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            print(f"Converted: {tex_file} to {output_path}")
        else:
            print(f"Failed to convert {tex_file}: {result.stderr}")
    except subprocess.TimeoutExpired:
        print(f"Timeout expired for {tex_file}. Skipping this file.")

# Loop through each subdirectory in the base directory
for subdir in tqdm(os.listdir(BASE_DIR), desc="Processing folders"):
    subdir_path = os.path.join(BASE_DIR, subdir)
    if os.path.isdir(subdir_path):
        main_tex_file = find_main_tex_file(subdir_path)
        if main_tex_file:
            output_text_file = os.path.join(OUTPUT_DIR, f"{subdir}.txt")
            convert_tex_to_txt(main_tex_file, output_text_file)
        else:
            print(f"No main .tex file found in {subdir_path}")
