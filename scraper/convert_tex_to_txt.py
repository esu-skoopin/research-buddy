import os
import re
import subprocess
import json
from tqdm import tqdm

# Base directory where your extracted files are located
BASE_DIR = "/Users/iamsergio/Desktop/arxiv/text/2305"  # Update this to the full path

# Path to the final JSON file
OUTPUT_JSON_PATH = os.path.join(BASE_DIR, "converted_data.json")

# Pattern to find the abstract
abstract_pattern = re.compile(
    r'\\begin\s*\{abstract\}(.*?)\\end\s*\{abstract\}', re.DOTALL | re.IGNORECASE
)

def find_main_tex_file(directory):
    main_file_candidates = ["main.tex", "index.tex"]
    for root, _, files in os.walk(directory):
        # Check for prioritized filenames
        for file in files:
            if file in main_file_candidates:
                return os.path.join(root, file)
        # If no prioritized file is found, return the first .tex file
        for file in files:
            if file.endswith(".tex"):
                return os.path.join(root, file)
    return None

def read_file_with_fallback(file_path):
    """
    Reads a file with fallback to different encodings if UTF-8 fails.
    """
    encodings = ['utf-8', 'latin-1', 'iso-8859-1']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    print(f"Failed to decode {file_path} with supported encodings.")
    return None

def convert_tex_to_txt(tex_content, timeout_sec=10):
    """
    Converts a string containing LaTeX content to plain text using Pandoc.
    """
    try:
        result = subprocess.run(
            ['pandoc', '-f', 'latex', '-t', 'plain'],
            input=tex_content,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout_sec
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Pandoc conversion failed: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        print(f"Pandoc conversion timeout expired.")
        return None

def extract_abstract_and_text(tex_content):
    """
    Extracts the abstract and removes it from the LaTeX content.
    """
    abstract_match = abstract_pattern.search(tex_content)
    if abstract_match:
        abstract = abstract_match.group(1).strip()
        text_without_abstract = abstract_pattern.sub("", tex_content).strip()
        return abstract, text_without_abstract
    else:
        return None, tex_content

# Initialize a list to hold all valid entries
data_list = []

# Loop through each subdirectory in the base directory
for subdir in tqdm(os.listdir(BASE_DIR), desc="Processing folders"):
    subdir_path = os.path.join(BASE_DIR, subdir)
    if os.path.isdir(subdir_path):
        main_tex_file = find_main_tex_file(subdir_path)
        if main_tex_file:
            tex_content = read_file_with_fallback(main_tex_file)
            if tex_content is None:
                print(f"Skipping {main_tex_file} due to encoding issues.")
                continue

            # Extract abstract and text without abstract
            abstract, text_without_abstract = extract_abstract_and_text(tex_content)

            # Check if both abstract and text are present
            if not abstract or not text_without_abstract:
                print(f"Skipping {subdir} as it lacks an abstract or text content.")
                continue

            # Convert the abstract and text to plain text
            abstract_txt = convert_tex_to_txt(abstract)
            text_txt = convert_tex_to_txt(text_without_abstract)

            if not abstract_txt or not text_txt:
                print(f"Skipping {subdir} due to failed Pandoc conversion.")
                continue

            # Remove newlines from the converted text
            abstract_txt = abstract_txt.replace("\n", " ")
            text_txt = text_txt.replace("\n", " ")

            # Add valid data to the list
            data_list.append({
                "id": subdir,
                "abstract": abstract_txt,
                "text": text_txt
            })
            print(f"Added data for {subdir}")
        else:
            print(f"No main .tex file found in {subdir_path}")

# Save all valid data to a single JSON file
if data_list:
    with open(OUTPUT_JSON_PATH, 'w', encoding='utf-8') as json_file:
        json.dump(data_list, json_file, ensure_ascii=False, indent=4)
    print(f"Saved all data to {OUTPUT_JSON_PATH}")
else:
    print("No valid data to save.")
