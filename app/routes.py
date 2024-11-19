from app import app
from flask import render_template, request, jsonify

# Pretrained model-related imports
from model.model_loader import load_model
from scraper.url_scraper import fetch_url_text

@app.route('/')
def index():
    return render_template('index.html')

# This method is the API call to summarize the given URL from the user
@app.route('/summarize', methods=['POST'])
def summarize():
    # Grab the URL inputted by the user
    data = request.form
    url = data["url"]

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Users will be told to provide either the PDF link or the full-text link of the arXiv article.
    # Then using our scraper method, we will grab the text-content, if any.
    text_content = fetch_url_text(url)

    if text_content == 'No text content available.':
        return jsonify({"error": 'No text content available'}), 500

    # For testing, I will only print out 800 characters
    return jsonify({"summary": text_content[:800]}), 200