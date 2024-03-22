""" 
Created on : 20/03/24 8:38am
@author : ds  
"""
from pprint import pprint

from PyPDF2 import PdfReader
from transformers import BartForConditionalGeneration, BartTokenizer
from typing import Optional
from fastapi import UploadFile
import os

UPLOAD_DIR = "policies"


def process_pdf(file: UploadFile) -> Optional[str]:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    print(file_path)

    # Check if the file is PDF
    if not file.filename.lower().endswith(".pdf"):
        return None

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    # Load PDF and extract text
    reader = PdfReader(file_path)
    num_pages = len(reader.pages)
    policy_text = ""
    for page_number in range(num_pages):
        page = reader.pages[page_number]
        policy_text += page.extract_text()

    # Load BART model and tokenizer
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

    # Summarize the text
    inputs = tokenizer(
        policy_text, return_tensors="pt", max_length=1024, truncation=True
    )
    summary_ids = model.generate(
        inputs.input_ids,
        num_beams=4,
        min_length=30,
        max_length=150,
        early_stopping=True,
    )
    summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary_text
