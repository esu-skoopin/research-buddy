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
    try:
        os.makedirs(output_dir, exist_ok=True)

        response = requests.get(gz_url, stream=True)
        response.raise_for_status()

        gz_filename = os.path.join(output_dir, os.path.basename(gz_url))
        with open(gz_filename, "wb") as gz_file:
            for chunk in response.iter_content(chunk_size=8192):
                gz_file.write(chunk)

        if tarfile.is_tarfile(gz_filename):
            with tarfile.open(gz_filename, "r:gz") as tar:
                tar.extractall(path=output_dir)

            tex_files = glob.glob(os.path.join(output_dir, "**", "*.tex"), recursive=True)

            if tex_files:
                main_tex_file = max(tex_files, key=os.path.getsize)
                print(f"Main .tex file found: {main_tex_file}")
                return main_tex_file

            return "No .tex files found in the archive."

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
        if os.path.exists(gz_filename):
            os.remove(gz_filename)


def convert_tex_to_txt(tex_file, output_dir="./converted_text"):
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
            cleaned_text = result.stdout.replace("\n", " ").strip()
            with open(output_text_file, "w", encoding="utf-8") as f:
                f.write(cleaned_text)

            print(f"Converted: {tex_file} to {output_text_file}")

            os.remove(tex_file)
            print(f"Deleted .tex file: {tex_file}")

            return cleaned_text
        else:
            return f"Error during conversion: {result.stderr}"
    except subprocess.TimeoutExpired:
        return f"Timeout expired for {tex_file}. Skipping this file."
    finally:
        if os.path.exists(tex_file):
            os.remove(tex_file)
            print(f"Deleted .tex file (post-error): {tex_file}")


def fetch_pdf_text(pdf_url):
    paper_raw = requests.get(pdf_url).content  # Gets the raw bytes that make up the paper
    doc = pymupdf.open(stream=paper_raw, filetype='pdf')  # Interprets the paper as a PDF
    return pymupdf4llm.to_markdown(doc)  # Returns the paper in Markdown format


def fetch_url_text(url, output_dir="./tex_files"):
    try:
        if "arxiv.org/abs/" in url:
            tex_url = url.replace("abs", "src")
            tex_file = fetch_and_extract_tex(tex_url, output_dir)
            if os.path.exists(tex_file):
                text_content = convert_tex_to_txt(tex_file)
                if text_content and "Error" not in text_content:
                    return text_content

        if "arxiv.org/abs/" in url:
            pdf_url = url.replace("abs", "pdf") + ".pdf"
            return fetch_pdf_text(pdf_url)

        return "No valid TeX or PDF content available."

    except requests.exceptions.RequestException as e:
        return f"Error fetching content from {url}: {e}"
