

from pathlib import Path
from typing import List

from PyPDF2 import PdfReader


def load_text_file(path: Path) -> str:
    """Load and return the content of a text file."""
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

def load_pdf(path: Path) -> str:
    """ Extract and return text from a PDF file. """
    text = ""
    reader = PdfReader(str(path))
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def load_documents(paths: List[str])->List[dict]:
    """
    Load documents from given file paths. Supports .txt and .pdf files.
    """
    docs = []
    for p in paths:
        path = Path(p)
        if not path.exists():
            continue
        ext = path.suffix.lower()
        if ext in [".txt", ".md"]:
            content = load_text_file(path)
        elif ext == ".pdf":
            content = load_pdf(path)
        else:
            continue
        docs.append({"file_path": str(path), "content": content})
    return docs