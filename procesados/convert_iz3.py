import pymupdf4llm
import os
import pathlib

def convert_pdf_to_md(pdf_path, output_path):
    print(f"Converting {pdf_path} to {output_path}...")
    md_text = pymupdf4llm.to_markdown(pdf_path)
    pathlib.Path(output_path).write_bytes(md_text.encode("utf-8"))
    print(f"Done: {output_path}")

if __name__ == "__main__":
    pdfs = [
        "Interface-Zero-30-players-guide-to-2095-v13.pdf",
        "Interface-Zero-30-The-Game-Master-s-Guide-to-2095.pdf",
        "SWIZ-01-Interface-Zero-3-digital-whkhpj.pdf"
    ]
    
    base_dir = r"d:\Rol\SWADE"
    
    for pdf in pdfs:
        full_path = os.path.join(base_dir, pdf)
        output_name = pdf.replace(".pdf", ".md")
        output_path = os.path.join(base_dir, output_name)
        
        if os.path.exists(output_path):
            print(f"Skipping {output_path} (already exists)")
            continue

        if os.path.exists(full_path):
            convert_pdf_to_md(full_path, output_path)
        else:
            print(f"File not found: {full_path}")
