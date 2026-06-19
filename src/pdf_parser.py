import pdfplumber  

#clean the data if needed
def clean(text):
    if not text:
        return ""
    #text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_pdf(path):
    pages = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = clean(page.extract_text())
            pages.append({"page": i+1, "text": text})
    return pages

