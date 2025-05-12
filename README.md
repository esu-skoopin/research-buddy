# <img height="30" alt="ResearchBuddy logo" src="https://github.com/user-attachments/assets/4a6fdead-9b7f-42c9-8d30-8893e5860a28"> &ThinSpace;ResearchBuddy

An AI-powered summarization tool designed to streamline the analysis of scholarly articles. This project leverages the Longformer Encoder-Decoder (LED) model to provide concise, context-rich summaries of academic research papers hosted on arXiv.

## Table of Contents
- [Project Overview](https://github.com/esu-skoopin/research-buddy?tab=readme-ov-file#project-overview)
- [Features](https://github.com/esu-skoopin/research-buddy?tab=readme-ov-file#features)
- [Technologies Used](https://github.com/esu-skoopin/research-buddy?tab=readme-ov-file#technologies-used)
- [Benefits of Using ResearchBuddy](https://github.com/esu-skoopin/research-buddy?tab=readme-ov-file#benefits-of-using-researchbuddy)
- [How to Set Up Project](https://github.com/esu-skoopin/research-buddy?tab=readme-ov-file#how-to-set-up-project)
- [Example Summary](https://github.com/esu-skoopin/research-buddy?tab=readme-ov-file#example-summary)
- [Results and Metrics](https://github.com/esu-skoopin/research-buddy?tab=readme-ov-file#results-and-metrics)
- [App Preview](https://github.com/esu-skoopin/research-buddy?tab=readme-ov-file#app-preview)

## Project Overview

ResearchBuddy is a web application that provides concise and accurate summaries of academic papers hosted on arXiv. This tool leverages advanced natural language processing (NLP) techniques and a fine-tuned transformer model to generate summaries, making it easier for researchers, students and professionals to quickly grasp the key points of lengthy and complex research papers.

### Diagram
<img width="1216" alt="Screenshot 2024-11-29 at 3 54 59 PM" src="https://github.com/user-attachments/assets/bc183e47-b342-4878-8c6f-42a8e608ad3c">

### Documentation
[[Download an in-depth paper of the implementation behind ResearchBuddy]](https://github.com/user-attachments/files/17963556/Scholarly.Article.AI.Summarizer.5.pdf)

## Features

- AI-powered summarization: Fine-tuned LED model for high-quality, domain-specific summaries of academic papers
- Bulk data processing: A pipeline to extract and preprocess scholarly data (PDF and LaTeX) from arXiv’s AWS S3 storage
- Real-time summarization API: Flask-based API to process arXiv URLs and return concise summaries with LaTeX rendering
- Productivity enhancement: Enables researchers and students to focus on analysis by reducing time spent reading full-length papers

## Technologies Used

<details>
<summary>Machine Learning</summary>
<p>

- Transformers (Hugging Face): Model and tokenizer for fine-tuning LED
- PyTorch: Deep learning framework for training and inference
- ROUGE Metrics: Evaluating summarization quality

</p>
</details>

<details>
<summary>Data Processing</summary>
<p>

- AWS S3: Bulk access to arXiv papers
- Pandoc: Conversion of LaTeX content to plain text
- TQDM: Monitoring pipeline progress

</p>
</details>

<details>
<summary>Backend</summary>
<p>

- Flask: A lightweight Python web framework for building the backend API
- Python: The primary programming language used for backend logic and model handling
- Requests: For making HTTP requests to fetch content from URLs

</p>
</details>

<details>
<summary>Frontend</summary>
<p>

- HTML/CSS: For structuring and styling the web pages
- Tailwind CSS: A utility-first CSS framework for styling the frontend
- JavaScript: For client-side scripting
- MathJax: For rendering LaTeX equations in the browser

</p>
</details>

## Benefits of Using ResearchBuddy

- Time-saving: Researchers and students often need to read through numerous papers to stay updated with the latest developments in their field. This tool saves time by providing quick summaries, allowing users to decide which papers are worth a deeper read.
- Accessibility: By summarizing complex papers into simpler, shorter texts, the tool makes cutting-edge research more accessible to a broader audience, including those who may not have a deep technical background
- Efficiency: The use of a fine-tuned transformer model ensures that the summaries are not only concise but also retain the essential information and context of the original paper
- Enhanced research workflow: Integrating this tool into the research workflow can significantly enhance productivity, enabling researchers to focus more on analysis and experimentation rather than spending excessive time on literature review

## How to Set Up Project
1. In your preferred terminal app, navigate to where you'd like for ResearchBuddy to be stored and clone the project using `git clone https://github.com/esu-skoopin/research-buddy.git`
2. Change directories into the project: `cd research-buddy`
3. Create a virtual environment for the project: `python3 -m venv venv`
4. Activate the virtual environment:
   - Mac or Linux: `source venv/bin/activate`
   - Windows Command Prompt: `venv\Scripts\activate`
   - Windows PowerShell: `venv\Scripts\Activate.ps1`
5. Install all Python dependencies: `pip install -r requirements.txt`
6. Install all Node.js dependencies: `npm install`
7. Generate styles for the project: `npx tailwindcss -i ./app/static/css/input.css -o ./app/static/css/output.css --watch`
8. The project is now ready to be run with `flask run`

## Example Summary

Input: [https://arxiv.org/pdf/2301.00001](https://arxiv.org/pdf/2301.00001)

Output generated using pre-trained model:
```
beta \left( \frac{\beta2}{\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-
\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-
\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-\gamma2}-
\gamma2}-\gamma2}-\gamma2}-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-
\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-
\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-
21\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-
\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-
\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-\gamma2-
\gamma2
```

Output generated using fine-tuned model:
```
We propose a Time-Orbiting Potential (TOP) trap for direct loading from an atom chip.
This trap can be produced by a single magnetic moment or by a single magnetic moment.
The trap can be made as small or large as desired simply by adjusting the chip size and
current amplitudes. The trap can be made as small or large as desired simply by adjusting
the chip size and current amplitudes. The trap can be made as small or large as desired
simply by adjusting the chip size and current amplitudes. The trap can be made as small
or large as desired simply by adjusting the chip size and current amplitudes. The trap
can be made as small or large as desired simply by adjusting the chip size and current
amplitudes. The trap can be made as small or large as desired simply by adjusting the
chip size and current amplitudes. The trap can be made as small or large as desired
simply by adjusting the chip size and current amplitudes. The trap can be made as small
or large as desired simply by adjusting the chip size and current amplitudes. The trap
can be made as small or large as desired simply by adjusting the chip size and current
amplitudes. The trap can be made as large or large as desired simply by adjusting the
chip size and current amplitudes.
```

## Results and Metrics

### ROUGE Scores
- Pre-trained model: ROUGE-1: 0.1138, ROUGE-2: 0.0241, ROUGE-L: 0.0653
- Fine-tuned model: ROUGE-1: 0.3232, ROUGE-2: 0.1126, ROUGE-L: 0.2115

Improvement: ~250%

## App Preview
<img width="1512" alt="Screenshot 2024-11-29 at 1 29 39 PM" src="https://github.com/user-attachments/assets/b7223fca-6724-4cdc-8111-c04a9cf61ccd">
<img width="1512" alt="Screenshot 2024-11-29 at 3 08 36 PM" src="https://github.com/user-attachments/assets/46742bea-1de7-4a98-bd34-0001646c87c1">
