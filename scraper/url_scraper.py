import os
import glob
import tarfile

import pymupdf
import pymupdf4llm
import requests
import shutil
import gzip
import subprocess

def fetch_and_extract_tex(gz_url, output_dir="./tex_files"):
    """
    Downloads and extracts a .gz file, then identifies and reads the largest .tex document.
    Cleans up files afterward.
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Download the .gz file
        response = requests.get(gz_url, stream=True)
        response.raise_for_status()

        gz_filename = os.path.join(output_dir, os.path.basename(gz_url))
        with open(gz_filename, "wb") as gz_file:
            for chunk in response.iter_content(chunk_size=8192):
                gz_file.write(chunk)

        # Check if it's a tar.gz file
        if tarfile.is_tarfile(gz_filename):
            with tarfile.open(gz_filename, "r:gz") as tar:
                tar.extractall(path=output_dir)

            tex_files = glob.glob(os.path.join(output_dir, "**", "*.tex"), recursive=True)

            if tex_files:
                # Find the largest .tex file
                main_tex_file = max(tex_files, key=os.path.getsize)
                print(f"Main .tex file found: {main_tex_file}")
                return main_tex_file

            # No .tex files found
            return "No .tex files found in the archive."

        # Handle standalone .gz files (not tarballs)
        else:
            decompressed_file = os.path.join(output_dir, os.path.basename(gz_filename).replace(".gz", ""))
            with gzip.open(gz_filename, "rb") as gz_file:
                with open(decompressed_file, "wb") as out_file:
                    out_file.write(gz_file.read())
            return decompressed_file

    except requests.exceptions.RequestException as e:
        return f"Error fetching .gz file: {e}"
    except tarfile.TarError as e:
        return f"Error extracting .gz file: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"
    finally:
        # Cleanup: remove downloaded files
        if os.path.exists(gz_filename):
            os.remove(gz_filename)


def convert_tex_to_txt(tex_file, output_dir="./converted_text"):
    """
    Converts a .tex file to plain text using Pandoc and returns the plain text content.
    """
    if not os.path.exists(tex_file):
        return f"Error: .tex file does not exist: {tex_file}"

    os.makedirs(output_dir, exist_ok=True)
    output_text_file = os.path.join(output_dir, os.path.basename(tex_file).replace(".tex", ".txt"))

    print(f"Converting {tex_file} to plain text...")
    try:
        result = subprocess.run(['pandoc', tex_file, '-t', 'plain'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, timeout=15)
        if result.returncode == 0:
            # Remove newlines and save the converted text to a file
            cleaned_text = result.stdout.replace("\n", " ").strip()
            with open(output_text_file, "w", encoding="utf-8") as f:
                f.write(cleaned_text)

            print(f"Converted: {tex_file} to {output_text_file}")

            # Return the cleaned text content directly
            return cleaned_text
        else:
            return f"Error during conversion: {result.stderr}"
    except subprocess.TimeoutExpired:
        return f"Timeout expired for {tex_file}. Skipping this file."


def fetch_pdf_text(pdf_url):
    """
    Dummy method for PDF parsing (to be implemented using PyPDF2 or pdfplumber).
    """
    paper_raw = requests.get(pdf_url).content  # Gets the raw bytes that make up the paper
    doc = pymupdf.open(stream=paper_raw, filetype='pdf')  # Interprets the paper as a PDF
    return pymupdf4llm.to_markdown(doc)  # Returns the paper in Markdown format


def fetch_url_text(url, output_dir="./tex_files"):
    """
    Fetch text content from a given arXiv URL, prioritizing TeX content from .gz archives.
    If no TeX is available, fallback to PDF scraping or scraping HTML content.
    """
    try:
        # Handle arXiv TeX source URL
        if "arxiv.org/abs/" in url:
            tex_url = url.replace("abs", "src")
            tex_file = fetch_and_extract_tex(tex_url, output_dir)
            if os.path.exists(tex_file):
                # Convert the TeX file to plain text and return its content
                text_content = convert_tex_to_txt(tex_file)
                if text_content and "Error" not in text_content:
                    return text_content

        # Handle arXiv PDF URL
        if "arxiv.org/abs/" in url:
            pdf_url = url.replace("abs", "pdf") + ".pdf"
            return fetch_pdf_text(pdf_url)

        return "No valid TeX or PDF content available."

    except requests.exceptions.RequestException as e:
        return f"Error fetching content from {url}: {e}"
