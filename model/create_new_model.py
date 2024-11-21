import json
from transformers import LEDTokenizer, LEDForConditionalGeneration, Trainer, TrainingArguments
from datasets import Dataset

JSON_FILE = "../data/summarization_data.json"  # Replace with your actual file path

with open(JSON_FILE, 'r') as f:
    data = json.load(f)

texts = [item['full_text'] for item in data]
summaries = [item['abstract'] for item in data]

texts = texts[:300]
summaries = summaries[:300]

dataset = Dataset.from_dict({"text": texts, "summary": summaries})

train_test_split = dataset.train_test_split(test_size=0.2)
train_dataset = train_test_split['train']
test_dataset = train_test_split['test']

tokenizer = LEDTokenizer.from_pretrained("allenai/led-base-16384") ## Specific for LED Model

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
        max_length=768,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )
    inputs["labels"] = labels["input_ids"]
    return inputs

train_dataset = train_dataset.map(preprocess_function, batched=True)
test_dataset = test_dataset.map(preprocess_function, batched=True)

model = LEDForConditionalGeneration.from_pretrained("allenai/led-base-16384")

training_args = TrainingArguments(
    output_dir="./results",
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

trainer.train()

model.save_pretrained("./led-finetuned")
tokenizer.save_pretrained("./led-finetuned")

print("Fine-tuning complete. Model saved to './led-finetuned'.")