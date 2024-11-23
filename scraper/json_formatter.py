import re
import os
import json
from tqdm import tqdm

# Directory containing plain text files converted from .tex
INPUT_DIR = "/Users/iamsergio/Desktop/arxiv/text/2307/converted_text"
OUTPUT_JSON = os.path.join(INPUT_DIR, "summarization_data.jsonl")

abstract_pattern = re.compile(r'(abstract|Abstract|ABSTRACT)[\s\n]*(.*?)(\n\s*\n|\Z)', re.DOTALL)

data = []

for filename in tqdm(os.listdir(INPUT_DIR), desc="Extracting abstracts"):
    file_path = os.path.join(INPUT_DIR, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the abstract
    match = abstract_pattern.search(content)
    if match:
        abstract = match.group(2).strip()
        data.append({
            "filename": filename,
            "abstract": abstract,
            "full_text": content
        })

# Save as JSON lines for easier handling
with open(OUTPUT_JSON, 'w', encoding='utf-8') as outfile:
    for entry in data:
        json.dump(entry, outfile)
        outfile.write("\n")

print(f"Summarization data saved to {OUTPUT_JSON}")
