import json
import torch
from transformers import LEDTokenizer, LEDForConditionalGeneration, Trainer, TrainingArguments
from datasets import Dataset

# Paths
JSON_FILE_NEW = "../data/new_summarization_data.json"
FINETUNED_MODEL_DIR = "./led-finetuned"
OUTPUT_DIR = "./led-finetuned-extended"

tokenizer = LEDTokenizer.from_pretrained(FINETUNED_MODEL_DIR)
model = LEDForConditionalGeneration.from_pretrained(FINETUNED_MODEL_DIR)

device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
model.to(device)

# Load new JSON data
with open(JSON_FILE_NEW, 'r') as f:
    new_data = json.load(f)

texts = [item['full_text'] for item in new_data]
summaries = [item['abstract'] for item in new_data]

# Change to number of articles
texts = texts[:300]
summaries = summaries[:300]

new_dataset = Dataset.from_dict({"text": texts, "summary": summaries})

def preprocess_function(examples):
    inputs = tokenizer(
        examples["text"],
        max_length=4096,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )
    labels = tokenizer(
        examples["summary"],
        max_length=1024,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )
    inputs["labels"] = labels["input_ids"]
    return inputs

new_dataset = new_dataset.map(preprocess_function, batched=True)

train_test_split = new_dataset.train_test_split(test_size=0.2)
train_dataset = train_test_split['train']
test_dataset = train_test_split['test']


training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    num_train_epochs=3,
    save_total_limit=2,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    load_best_model_at_end=True
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)

print("Starting additional training...")
trainer.train()

model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"Extended fine-tuning complete. Updated model saved to '{OUTPUT_DIR}'.")
