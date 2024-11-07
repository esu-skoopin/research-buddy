from flask import Flask, render_template, request, redirect, url_for, jsonify
# for pretrained model:
from model.model_loader import load_model
from scraper.url_scraper import fetch_url_text

app = Flask(__name__)

# This method is the API call to summarize the given url from the user.
@app.route('/summarize', methods=['POST'])
def summarize():
    # Grab the url inputted by the user
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Users will be told to provide either the pdf link or the full-text link of the Internet Scholar Archive article.
    # Then using our scraper method, we will grab the text-content, if any.
    text_content = fetch_url_text(url)

    if text_content == 'No text content available.':
        return jsonify({"error": '...'}), 500

    # For testing, i will only print out 800 characters
    return jsonify({"summary": text_content[:800]}), 200