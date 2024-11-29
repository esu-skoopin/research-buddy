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

### Frontend
- **HTML/CSS:** For structuring and styling the web pages.
- **Tailwind CSS:** A utility-first CSS framework for styling the frontend.
- **JavaScript:** For client-side scripting.
- **MathJax:** For rendering LaTeX equations in the browser.

### Backend
- **Flask:** A lightweight Python web framework for building the backend API.
- **Python:** The primary programming language used for backend logic and model handling.
- **Requests:** For making HTTP requests to fetch content from URLs.

## Why It Is Helpful

- **Time-Saving**: Researchers and students often need to read through numerous papers to stay updated with the latest developments in their field. This tool saves time by providing quick summaries, allowing users to decide which papers are worth a deeper read.
- **Accessibility**: By summarizing complex papers into simpler, shorter texts, the tool makes cutting-edge research more accessible to a broader audience, including those who may not have a deep technical background.
- **Efficiency**: The use of a fine-tuned transformer model ensures that the summaries are not only concise but also retain the essential information and context of the original paper.
- **Enhanced Research Workflow**: Integrating this tool into the research workflow can significantly enhance productivity, enabling researchers to focus more on analysis and experimentation rather than spending excessive time on literature review.

## Example Summaries

### Input
[https://arxiv.org/abs/2301.00001](https://arxiv.org/abs/2301.00001)

### New Output
```json
{
  "summary": "We propose a Time-Orbiting Potential (TOP) trap for direct loading from an
atom chip. This trap can be produced by a single magnetic moment or by a single magnetic
moment. The trap can be made as small or large as desired simply by adjusting the chip
size and current amplitudes. The trap can be made as small or large as desired simply by
adjusting the chip size and current amplitudes. The trap can be made as small or large as
desired simply by adjusting the chip size and current amplitudes. The trap can be made
as small or large as desired simply by adjusting the chip size and current amplitudes. The
trap can be made as small or large as desired simply by adjusting the chip size and current
amplitudes. The trap can be made as small or large as desired simply by adjusting the chip
size and current amplitudes. The trap can be made as small or large as desired simply by
adjusting the chip size and current amplitudes. The trap can be made as small or large as
desired simply by adjusting the chip size and current amplitudes. The trap can be made
as small or large as desired simply by adjusting the chip size and current amplitudes. The
trap can be made as large or large as desired simply by adjusting the chip size and current
amplitudes."
}
```

### Old Output
```json
{
  "summary": beta \left( \frac{\beta2}{\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-
\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-
\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-
\gamma2}-\gamma2}-\gamma2}-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-
\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-
\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-
21
\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-
\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-
\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-
\
}
```
