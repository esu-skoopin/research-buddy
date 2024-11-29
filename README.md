# Scholarly Article AI Summarizer

An AI-powered summarization tool designed to streamline the analysis of scholarly articles. This project leverages the Longformer Encoder-Decoder (LED) model to provide concise, context-rich summaries of academic research papers hosted on arXiv.

## Project Overview

The Scholarly Article AI Summarizer is a web application that provides concise and accurate summaries of academic papers hosted on arXiv. This tool leverages advanced natural language processing (NLP) techniques and a fine-tuned transformer model to generate summaries, making it easier for researchers, students, and professionals to quickly grasp the key points of lengthy and complex research papers.

## Features

- **AI-Powered Summarization**: Fine-tuned LED model for high-quality, domain-specific summaries of academic papers.
- **Bulk Data Processing**: A pipeline to extract and preprocess scholarly data (PDF and LaTeX) from arXiv’s AWS S3 storage.
- **Real-Time Summarization API**: Flask-based API to process arXiv URLs and return concise summaries with LaTeX rendering.
- **Productivity Enhancement**: Enables researchers and students to focus on analysis by reducing time spent reading full-length papers.

## Technologies Used

### Machine Learning
- **Transformers (Hugging Face)**: Model and tokenizer for fine-tuning LED.
- **PyTorch**: Deep learning framework for training and inference.
- **ROUGE Metrics**: Evaluating summarization quality.

### Data Processing
- **AWS S3**: Bulk access to arXiv papers.
- **Pandoc**: Conversion of LaTeX content to plain text.
- **TQDM**: Monitoring pipeline progress.

### Backend
- **Flask**: API for summarization.
- **BeautifulSoup**: Parsing HTML content from arXiv (if needed).

### Frontend
- **HTML/CSS**: Web interface for API usage.
- **MathJax**: Rendering LaTeX equations in the browser.

## Why It Is Helpful

- **Time-Saving**: Researchers and students often need to read through numerous papers to stay updated with the latest developments in their field. This tool saves time by providing quick summaries, allowing users to decide which papers are worth a deeper read.
- **Accessibility**: By summarizing complex papers into simpler, shorter texts, the tool makes cutting-edge research more accessible to a broader audience, including those who may not have a deep technical background.
- **Efficiency**: The use of a fine-tuned transformer model ensures that the summaries are not only concise but also retain the essential information and context of the original paper.
- **Enhanced Research Workflow**: Integrating this tool into the research workflow can significantly enhance productivity, enabling researchers to focus more on analysis and experimentation rather than spending excessive time on literature review.

## Example Summaries

### Input
[https://arxiv.org/abs/2301.00001](https://arxiv.org/abs/2301.00001)

### Output
```json
{
  "summary": "We propose a Time-Orbiting Potential (TOP) trap for direct loading from an atom chip. This design facilitates... [truncated for brevity]"
}
