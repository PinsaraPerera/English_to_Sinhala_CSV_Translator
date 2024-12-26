import pdfplumber
import pandas as pd
import re

# File paths
input_pdf = "Books/sinhalaG9.pdf"
output_exel = "Translated/sinhala_grade_9.xlsx"

def extract_sentences(text):
    """
    Split text into sentences based on common punctuation marks.
    """
    # Use regex to split text by full stops, question marks, exclamation points
    sentences = re.split(r'[.!?]\s', text)

    # Remove empty strings and strip extra spaces
    return [sentence.strip() for sentence in sentences if sentence.strip()]

# Initialize a list to hold sentences
sinhala_sentences = []

try:
    with pdfplumber.open(input_pdf) as pdf:
        # Iterate through all pages
        for page in pdf.pages:
            # Extract text from the page
            text = page.extract_text()
            if text:
                # Extract Sinhala sentences
                sentences = extract_sentences(text)
                sinhala_sentences.extend(sentences)
    
    # Create a DataFrame from the sentences
    df = pd.DataFrame(sinhala_sentences, columns=["Sinhala Sentences"])
    
    # Save to a CSV file
    # df.to_csv(output_csv, index=False, encoding='utf-8')
    df.to_excel(output_exel, index=False, engine='openpyxl')
    print(f"Sinhala sentences extracted and saved to {output_exel}")

except Exception as e:
    print(f"An error occurred: {e}")
