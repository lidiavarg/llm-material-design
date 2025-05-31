import os
from pathlib import Path
import fitz
from bs4 import BeautifulSoup

folder_pdf_path      = Path(r'data/articles pdf 2018')
folder_html_path     = Path(r'data/articles_html_2018')
folder_raw_txt_path  = Path(r'data/articles_raw_txt_2018')
folder_raw_img_path  = Path(r'data/articles_raw_img_2018')

for folder in (folder_html_path, folder_raw_txt_path, folder_raw_img_path):
    folder.mkdir(parents=True, exist_ok=True)

def pdf_to_html(pdf_path: Path, html_folder: Path) -> Path:
    doc = fitz.open(pdf_path)
    html = "".join(page.get_text("html") for page in doc)
    out_html = html_folder / f"{pdf_path.stem}.html"
    out_html.write_text(html, encoding="utf-8")
    return out_html

def html_to_txt(html_path: Path, txt_folder: Path) -> Path:
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    text = soup.get_text()
    out_txt = txt_folder / f"{html_path.stem}.txt"
    out_txt.write_text(text, encoding="utf-8")
    return out_txt

def extract_images(pdf_path: Path, images_subfolder: Path):
    doc = fitz.open(pdf_path)
    for page_idx, page in enumerate(doc, start=1):
        for img_idx, meta in enumerate(page.get_images(full = True), start = 1):
            xref, smask = meta[0], meta[1]
            if smask != 0:
                continue
            img = doc.extract_image(xref)
            data, ext = img["image"], img["ext"]
            img_name = f"{pdf_path.stem}_p{page_idx}_i{img_idx}.{ext}"
            (images_subfolder / img_name).write_bytes(data)

for pdf_path in folder_pdf_path.glob("*.pdf"):
    name = pdf_path.stem

    images_subfolder = folder_raw_img_path / name
    images_subfolder.mkdir(parents = True, exist_ok = True)

    html_file = folder_html_path / f"{name}.html"
    txt_file  = folder_raw_txt_path  / f"{name}.txt"

    if html_file.exists() and txt_file.exists():
        print(f"Skipping {name}")
        continue

    print(f"Processing {name}…")
    html_file = pdf_to_html(pdf_path, folder_html_path)
    txt_file  = html_to_txt(html_file, folder_raw_txt_path)
    extract_images(pdf_path, images_subfolder)
