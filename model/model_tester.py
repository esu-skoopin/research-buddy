import json
import torch
from transformers import LEDTokenizer, LEDForConditionalGeneration
from rouge_score import rouge_scorer

# Paths
JSON_FILE = "../data/converted_data.json"
PRETRAINED_MODEL_DIR = "allenai/led-base-16384"
FINETUNED_MODEL_DIR = "./led-finetuned"

# Load tokenizer and pre-trained model
tokenizer = LEDTokenizer.from_pretrained(PRETRAINED_MODEL_DIR)
pretrained_model = LEDForConditionalGeneration.from_pretrained(PRETRAINED_MODEL_DIR)

# Load fine-tuned model
finetuned_model = LEDForConditionalGeneration.from_pretrained(FINETUNED_MODEL_DIR)

device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")
pretrained_model.to(device)
finetuned_model.to(device)

# Load test data
with open(JSON_FILE, 'r') as f:
    data = json.load(f)

# Split data into test set
test_data = data[-60:]  # Assuming the last 60 samples are for testing

# Initialize ROUGE scorer
scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

def evaluate_model(model):
    rouge_scores = {'rouge1': [], 'rouge2': [], 'rougeL': []}
    for sample in test_data:
        full_text = sample['text']
        reference_summary = sample['abstract']

        inputs = tokenizer(
            full_text,
            return_tensors="pt",
            max_length=4096,
            truncation=True
        ).to(device)

        with torch.no_grad():
            outputs = model.generate(
                inputs["input_ids"],
                max_length=768,
                num_beams=4,
                early_stopping=True
            )

        generated_summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Calculate ROUGE scores
        scores = scorer.score(reference_summary, generated_summary)
        for key in rouge_scores:
            rouge_scores[key].append(scores[key].fmeasure)

    # Calculate average ROUGE scores
    average_rouge_scores = {key: sum(values) / len(values) for key, values in rouge_scores.items()}
    return average_rouge_scores

# Evaluate pre-trained model
average_rouge_scores_pretrained = evaluate_model(pretrained_model)
print("Average ROUGE scores (Pre-trained):", average_rouge_scores_pretrained)

# Evaluate fine-tuned model
average_rouge_scores_finetuned = evaluate_model(finetuned_model)
print("Average ROUGE scores (Fine-tuned):", average_rouge_scores_finetuned)

# Calculate percentage improvement
percentage_improvement = {}
for key in average_rouge_scores_pretrained:
    pretrained_score = average_rouge_scores_pretrained[key]
    finetuned_score = average_rouge_scores_finetuned[key]
    improvement = ((finetuned_score - pretrained_score) / pretrained_score) * 100
    percentage_improvement[key] = improvement

print("Percentage Improvement:", percentage_improvement)