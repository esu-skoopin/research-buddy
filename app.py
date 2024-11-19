import torch
from flask import Flask, render_template, request, jsonify
from model.model_loader import load_model
from scraper.url_scraper import fetch_url_text

app = Flask(__name__)

# Load the fine-tuned model
MODEL_DIR = "./led-finetuned"  # Path to your fine-tuned model
model, tokenizer, device = load_model(MODEL_DIR)

# This method is the API call to summarize the given URL from the user.
@app.route('/summarize', methods=['POST'])
def summarize():
    # Grab the URL inputted by the user
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Fetch the text content from the URL
    text_content = fetch_url_text(url)

    if text_content == 'No text content available.':
        return jsonify({"error": 'No text content found at the provided URL.'}), 500

    try:
        # Tokenize the extracted text
        inputs = tokenizer(text_content, return_tensors="pt", max_length=4096, truncation=True)
        inputs = {key: val.to(device) for key, val in inputs.items()}

        # Generate the summary
        model.eval()
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=512, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Return the generated summary
        return jsonify({"summary": summary}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)