import os
from pathlib import Path
import fitz
from bs4 import BeautifulSoup

folder_pdf_path = Path(r'data/articles pdf 2018')
folder_html_path = Path(r'data/articles_html_2018')
folder_raw_txt_path = Path(r'data/articles_raw_txt_2018')
folder_raw_img_path = Path(r'data/articles_raw_img_2018')

'''1)if directory doesn't exist yet, program creates it
   2)if directory exists already, program doesn't show an Error message'''
for folder in (folder_html_path, folder_raw_txt_path, folder_raw_img_path):
    folder.mkdir(parents=True, exist_ok=True)

def pdf_to_html(pdf_files_path, html_folder):
    doc = fitz.open(pdf_files_path)
    html = "".join(page.get_text("html") for page in doc)
    out_html = html_folder / f"{pdf_files_path.stem}.html"
    with open(out_html, "w", encoding="utf-8") as file_html:
        file_html.write(html)
    return out_html

def html_to_txt(html_doc, txt_folder):
    with open(html_doc, "r", encoding="utf-8") as file_html:
        soup = BeautifulSoup(file_html, "html.parser")
    text = soup.get_text()
    out_txt = txt_folder / f"{html_doc.stem}.txt"
    with open(out_txt, "w", encoding="utf-8") as file_txt:
        file_txt.write(text)
    return out_txt

def extract_images(pdf_files_path, images_subfolder):
    doc = fitz.open(pdf_files_path)
    for page_idx, page in enumerate(doc, start=1):
        for img_idx, meta in enumerate(page.get_images(full=True), start=1):
            xref, smask = meta[0], meta[1]
            if smask != 0:  # skip masks
                continue
            img = doc.extract_image(xref)
            data, ext = img["image"], img["ext"]
            img_name = f"{pdf_files_path.stem}_p{page_idx}_i{img_idx}.{ext}"
            out  = images_subfolder / img_name
            with open(out, "wb") as f:
                f.write(data)

'''PDF cycle for extracting always new information into HTML and TXT folders'''
for pdf_files_path in folder_pdf_path.glob("*.pdf"):
    name = pdf_files_path.stem
    
    images_subfolder = folder_raw_img_path / pdf_files_path.stem
    images_subfolder.mkdir(parents=True, exist_ok=True)
    
    html_files_path = folder_html_path / f"{name}.html"
    txt_files_path  = folder_raw_txt_path  / f"{name}.txt"

    if html_files_path.exists() and txt_files_path.exists():
        print(f"Skipping {name}")
        continue

    print(f"Processing {name}…")
    
    ''''Run funcs'''
    html_file = pdf_to_html(pdf_files_path, folder_html_path)
    html_to_txt(html_file, folder_raw_txt_path)
    extract_images(pdf_files_path, images_subfolder)

