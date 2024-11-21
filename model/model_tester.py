import json
import torch
from transformers import LEDTokenizer, LEDForConditionalGeneration

# Paths
JSON_FILE = "../data/summarization_data.json"
PRETRAINED_MODEL_DIR = "allenai/led-base-16384"
FINETUNED_MODEL_DIR = "./led-finetuned"

tokenizer = LEDTokenizer.from_pretrained(PRETRAINED_MODEL_DIR)
pretrained_model = LEDForConditionalGeneration.from_pretrained(PRETRAINED_MODEL_DIR)
finetuned_model = LEDForConditionalGeneration.from_pretrained(FINETUNED_MODEL_DIR)

device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")
pretrained_model.to(device)
finetuned_model.to(device)

with open(JSON_FILE, 'r') as f:
    data = json.load(f)

article_index = 1
selected_article = data[article_index]
full_text = selected_article['full_text']

if not full_text.strip():
    raise ValueError("Selected article has no text.")

print("\n--- Debug: Article Info ---")
print(f"Article Index: {article_index}")
print(f"Full text length: {len(full_text)}")
print(f"Full text (first 500 chars): {full_text[:500]}")

inputs = tokenizer(
    full_text,
    return_tensors="pt",
    max_length=4096,
    truncation=True
)
inputs = {key: val.to(device) for key, val in inputs.items()}

print("\n--- Debug: Tokenized Inputs ---")
print(inputs)

# Pre-trained model
pretrained_model.eval()
with torch.no_grad():
    pretrained_outputs = pretrained_model.generate(
        **inputs,
        max_length=512,
        num_beams=4,
        early_stopping=True
    )
pretrained_summary = tokenizer.decode(pretrained_outputs[0], skip_special_tokens=True)
print("\n--- Debug: Pre-trained Model Output ---")
print(pretrained_summary)

# Fine-tuned model
finetuned_model.eval()
with torch.no_grad():
    finetuned_outputs = finetuned_model.generate(
        **inputs,
        max_length=768,
        num_beams=4,
        early_stopping=True
    )
finetuned_summary = tokenizer.decode(finetuned_outputs[0], skip_special_tokens=True)
print("\n--- Debug: Fine-Tuned Model Output ---")
print(finetuned_summary)