from app import app
from flask import render_template, request, jsonify

# Pretrained model-related imports
from model.model_loader import load_model
from scraper.url_scraper import fetch_url_text
from app.utils.summarizer import summarize_text_from_url

@app.route('/')
def index():
    return render_template('index.html')

# This method is the API call to summarize the given URL from the user
@app.route('/summarize', methods=['POST'])
def summarize():
    # Grab the URL inputted by the user
    url = request.json.get('url')

	# Validate URL
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # Users will be told to provide either the PDF link or the full-text link of the arXiv article.
    # Then using our scraper method, we will grab the text-content, if any.
    summary = summarize_text_from_url(url)

    if summary == 'Summarization is only supported for papers available in HTML or PDF file formats at the moment':
        return jsonify({'error': summary}), 500
	
    return jsonify({'summary': summary}), 200