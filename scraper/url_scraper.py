import glob
import os
import tarfile
import requests
import shutil
import gzip


def fetch_and_extract_tex(gz_url, output_dir="./tex_files"):
    """
    Downloads and extracts a .gz file, then identifies and reads the largest document file
    (e.g., .tex or other text-based files). Cleans up files afterward.
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
                with open(main_tex_file, "r", encoding="utf-8", errors="replace") as tex_file:
                    tex_content = tex_file.read()
                return tex_content

            # No .tex files found; check for other text-like files
            document_files = glob.glob(os.path.join(output_dir, "**", "*.*"), recursive=True)
            valid_files = [f for f in document_files if f.endswith((".txt", ".md", ".doc", ".rtf"))]

            if valid_files:
                main_doc_file = max(valid_files, key=os.path.getsize)
                with open(main_doc_file, "r", encoding="utf-8", errors="replace") as doc_file:
                    content = doc_file.read()
                return content

            extracted_files = os.listdir(output_dir)
            return f"No readable files (.tex, .txt, etc.) found in the archive. Extracted files: {extracted_files}"

        # Handle standalone .gz files (not tarballs)
        else:
            decompressed_file = os.path.join(output_dir, os.path.basename(gz_filename).replace(".gz", ""))
            with gzip.open(gz_filename, "rb") as gz_file:
                with open(decompressed_file, "wb") as out_file:
                    out_file.write(gz_file.read())

            # Read the decompressed file
            with open(decompressed_file, "r", encoding="utf-8", errors="replace") as decompressed:
                content = decompressed.read()
            return content

    except requests.exceptions.RequestException as e:
        return f"Error fetching .gz file: {e}"
    except tarfile.TarError as e:
        return f"Error extracting .gz file: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"
    finally:
        # Cleanup: remove downloaded and extracted files
        if os.path.exists(gz_filename):
            os.remove(gz_filename)
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)


def fetch_pdf_text(pdf_url):
    """
    TODO Method for PDF parsing (e.g., using PyPDF2 or pdfplumber).
    """
    return f"PDF scraping is not implemented yet. URL: {pdf_url}"


def fetch_url_text(url):
    """
    Fetch text content from a given arXiv URL, prioritizing TeX content from .gz archives.
    If no TeX is available, fallback to PDF scraping or scraping HTML content.
    """
    try:
        # Handle arXiv TeX source URL
        if "arxiv.org/abs/" in url:
            tex_url = url.replace("abs", "src")
            tex_content = fetch_and_extract_tex(tex_url)
            if "Error" not in tex_content:
                return tex_content

        # Handle arXiv PDF URL
        if "arxiv.org/abs/" in url:
            pdf_url = url.replace("abs", "pdf") + ".pdf"
            pdf_content = fetch_pdf_text(pdf_url)
            return pdf_content

        return "No TeX or PDF content available. Attempt another method."

    except requests.exceptions.RequestException as e:
        return f"Error fetching content from {url}: {e}"