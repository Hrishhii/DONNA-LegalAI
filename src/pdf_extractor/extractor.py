import fitz
import os

INPUT_DIR = "input_pdfs"
OUTPUT_DIR = "extracted_texts"

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            full_text += f"\n\n-- Page {page_num}--\n{text}"
        return full_text.strip()
    
    except Exception as e:
        print(f"[ERROR] Failed to extract text: {e}")
        return None
    
def save_text(text, output_path):
    with open(output_path, 'w', encoding="utf-8") as f:
        f.write(text)

def main():
    print("[DEBUG] Looking for PDFs...")
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
    print(f"[DEBUG] Found PDFs: {pdf_files}")
    if not pdf_files:
        print("[INFO] No PDF files found in input_pdfs/. Please add one PDF to process.")
        return
    elif len(pdf_files) > 1:
        print("[WARNING] Multiple PDF files found in input_pdfs/. Please ensure only one PDF is present.")
        return
    
    pdf_file = pdf_files[0]
    input_path = os.path.join(INPUT_DIR, pdf_file)
    output_path = os.path.join(OUTPUT_DIR, pdf_file.replace('.pdf', '.txt'))
    
    print(f"[INFO] Extracting text from: {pdf_file}")
    extracted_text = extract_text_from_pdf(input_path)
    
    if extracted_text:
        save_text(extracted_text, output_path)
        print(f"[SUCCESS] Text saved to: {output_path}")
    else:
        print("[ERROR] Extraction failed.")
        
        

main()