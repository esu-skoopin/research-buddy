import json

file_name = "summarization_data_{}.json"

def merge_JsonFiles(filename):
    result = []
    for i in range(1, 3):  # Assuming you're merging two files
        curr = file_name.format(i)
        print(f"Processing file: {curr}")
        with open(curr, 'r') as infile:
            # Load the entire JSON array
            data = json.load(infile)
            result.extend(data)

    # Write the final merged JSON array to a file
    with open('summarization_data.json', 'w') as output_file:
        json.dump(result, output_file, indent=4)

merge_JsonFiles(file_name)
