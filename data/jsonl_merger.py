import json

file_name = "summarization_data_{}.jsonl"

def merge_JsonFiles(filename):
    result = []
    for i in range(1, 9):
        curr = file_name.format(i)
        print(f"Processing file: {curr}")
        with open(curr, 'r') as infile:
            for line in infile:
                result.append(json.loads(line.strip()))

    with open('summarization_data.json', 'w') as output_file:
        json.dump(result, output_file, indent=4)

merge_JsonFiles(file_name)
