import re
import os
import json
from tqdm import tqdm

# Directory containing plain text files converted from .tex
INPUT_DIR = "/Users/iamsergio/Desktop/arxiv/text/2302/converted_text"
OUTPUT_JSON = os.path.join(INPUT_DIR, "summarization_data.jsonl")

# Regex to capture abstracts
abstract_pattern = re.compile(
    r'\\begin\s*\{abstract\}(.*?)\\end\s*\{abstract\}', re.DOTALL | re.IGNORECASE
)

data = []

for filename in tqdm(os.listdir(INPUT_DIR), desc="Extracting abstracts"):
    file_path = os.path.join(INPUT_DIR, filename)
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        # Find the abstract
        match = abstract_pattern.search(content)
        if match:
            abstract = match.group(1).strip()
            data.append({
                "filename": filename,
                "abstract": abstract,
                "full_text": content
            })
        else:
            print(f"No abstract found in file: {filename}")
    except Exception as e:
        print(f"Error processing file {filename}: {e}")

# Verify if data is captured
if not data:
    print("No data to save. Ensure abstracts were extracted correctly.")
else:
    try:
        # Save as JSON lines
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as outfile:
            for entry in data:
                json.dump(entry, outfile)
                outfile.write("\n")
        print(f"Summarization data saved to {OUTPUT_JSON}")
    except Exception as e:
        print(f"Error saving JSON data: {e}")
