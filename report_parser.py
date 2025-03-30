# report_parser.py
import pdfplumber
import docx

def parse_pdf_report(file_path):
    """
    Parse a PDF report and extract text.
    Additional NLP processing can be added here to extract emissions data.
    """
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        text = "Error parsing PDF."
    return text

def parse_docx_report(file_path):
    """
    Parse a DOCX report and extract text.
    Additional NLP processing can be added here to extract emissions data.
    """
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        text = "Error parsing DOCX."
    return text
