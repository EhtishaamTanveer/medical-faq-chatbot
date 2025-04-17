# src/utils/document_processor.py
from PyPDF2 import PdfReader

class DocumentProcessor:
    def extract_text(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
