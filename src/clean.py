import os
import re

INPUT_FILE = "data/raw_txt/acs.jpcc.8b02699-support.txt"
OUTPUT_FILE = "data/articles_clean_txt_2018/article_cleaned.txt"
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)


#Replace Figure S<number> references and captions
def remove_figure_sections(text):
    pattern_caption = r"(Figure S\d+:.*?)(?=\n\S|\Z)"
    text = re.sub(pattern_caption, "[FIGURE]", text, flags=re.DOTALL)
    
    pattern_inline = r"\bFigure S\d+\b"
    text = re.sub(pattern_inline, "[FIGURE]", text)

    return text


#Replace numbered references like "(1)", "[2]", or "Ref. 3"
def remove_inline_references(text):
    text = re.sub(r"\(\s*\d+\s*\)", "[REF]", text)
    text = re.sub(r"\[\s*\d+\s*\]", "[REF]", text)
    text = re.sub(r"Ref\.?\s*\d+", "[REF]", text)

    return text


def clean_article(text):
    parts = re.split(r"\bMETHODS\b", text, maxsplit=1)
    if len(parts) > 1:
        text = parts[1]
    else:
        text = parts[0]
    text = re.sub(r"\bREFERENCES\b.*", "", text, flags=re.DOTALL)
    text = re.sub(r"\S+@\S+", "", text)
    text = re.sub(r"http\S+", "", text)

    #Remove page numbers on lines by themselves
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)
    text = remove_figure_sections(text)
    text = remove_inline_references(text)

    '''Remove any characters that are not letters, numbers, whitespace, or
    common scientific symbols (e.g., °, µ, ±, ×, %, /, <, >, =, etc.)'''
    allowed_pattern = r"[^a-zA-Z0-9\s\.\,\:\;\%\(\)\[\]\-\±×°µμ\/\\<>=\+\–eVnm]"
    text = re.sub(allowed_pattern, "", text)

    '''Join lines inside paragraphs:
    Replace single newlines (not preceded or followed by another newline) with a space'''
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    text = re.sub(r"\n{2,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw_text = f.read()
    
cleaned_text = clean_article(raw_text)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(cleaned_text)

print("Cleaning complete. Result saved to:", OUTPUT_FILE)
