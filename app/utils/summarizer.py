import requests
import pymupdf
import pymupdf4llm
from bs4 import BeautifulSoup
from transformers import pipeline

def parse_html(url):
	paper_raw = ''  # Placeholder for HTML-parsing code

def parse_pdf(url):
	paper_raw = requests.get(url).content  # Gets the raw bytes that make up the paper
	doc = pymupdf.open(stream=paper_raw, filetype='pdf')  # Interprets the paper as a PDF
	return pymupdf4llm.to_markdown(doc)  # Returns the paper in Markdown format

def summarize_text_from_url(url):
	parsed_text = ''
	if 'html' in url.lower():
		parsed_text = parse_html(url)
	elif 'pdf' in url.lower():
		parsed_text = parse_pdf(url)
	elif 'abs' in url.lower():
		page_raw = requests.get(url).content
		page_html = BeautifulSoup(page_raw, 'html.parser')
		html_link_element = page_html.find('a', id='latexml-download-link')
		pdf_link_element = page_html.find('a', class_='abs-button download-pdf')
		if html_link_element:
			parsed_text = parse_html(url.replace('abs', 'html'))
		elif pdf_link_element:
			parsed_text = parse_pdf(url.replace('abs', 'pdf'))
		else:
			return('Summarization is only supported for papers available in HTML or PDF file formats at the moment')
	else:
		return('Please give a link to the landing page for a paper or the direct link to the HTML or PDF version of a paper on arxiv.org')
	summarizer = pipeline('summarization', model='allenai/led-base-16384')
	return {'thing': '', 'summary': summarizer(parsed_text, min_length=150, max_length=300, truncation=True, do_sample=False)[0]['summary_text']}