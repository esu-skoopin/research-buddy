from flask import Flask
from model.model_loader import load_model

app = Flask(__name__)

model_dir = "model/led-finetuned"
model, tokenizer, device = load_model(model_dir)

from app import routes
