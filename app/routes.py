from transformers import LEDForConditionalGeneration
from app import app
from flask import render_template, request, jsonify
from scraper.url_scraper import fetch_url_text
import torch

# Use the model, tokenizer, and device loaded in __init__.py
from app import model, tokenizer, device

# Define the pretrained model directory
PRETRAINED_MODEL_DIR = "allenai/led-base-16384"
pretrained_model = LEDForConditionalGeneration.from_pretrained(PRETRAINED_MODEL_DIR).to(device)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        # Extract the URL from the request
        url = request.json.get('url')

        if not url:
            return jsonify({"error": "URL is required"}), 400

        # Fetch the text content from the URL
        text_content = fetch_url_text(url)

        if not text_content or "Error" in text_content:
            return jsonify({"error": "Failed to fetch text content from the URL."}), 500

        # Tokenize the input text
        inputs = tokenizer(
            text_content,
            return_tensors="pt",
            max_length=4096,
            truncation=True
        ).to(device)

        # Generate the summary using the primary model
        model.eval()
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=768,
                num_beams=4,
                early_stopping=True
            )

        # Generate the summary using the pretrained model for comparison
        pretrained_model.eval()
        with torch.no_grad():
            pretrained_outputs = pretrained_model.generate(
                **inputs,
                max_length=512,
                num_beams=4,
                early_stopping=True
            )

        # Decode the generated summaries
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        pretrained_summary = tokenizer.decode(pretrained_outputs[0], skip_special_tokens=True)

        # Return the summaries
        return jsonify({
            "summary": summary,
            "pretrained_summary": pretrained_summary
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
