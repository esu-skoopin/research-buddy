from app import app
from flask import render_template, request, jsonify
from scraper.url_scraper import fetch_url_text
import torch

# Use the model, tokenizer, and device loaded in __init__.py
from app import model, tokenizer, device

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.form
        url = data.get("url", "").strip()

        if not url:
            return jsonify({"error": "URL is required"}), 400

        text_content = fetch_url_text(url)

        if not text_content or "Error" in text_content:
            return jsonify({"error": "Failed to fetch text content from the URL."}), 500

        inputs = tokenizer(
            text_content,
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

        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return jsonify({"summary": summary}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500