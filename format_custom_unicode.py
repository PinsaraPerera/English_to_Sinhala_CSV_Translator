import pandas as pd
import re

# File paths
input_xlsx = "Translated/sinhala_grade_9.xlsx" 
output_xlsx = "Excel_files/sinhala_grade_9.xlsx"  

# Function to split text into sentences using the custom delimiter
def split_text_to_sentences(text, delimiter="'"):
    # Use the custom delimiter to split the text
    sentences = re.split(re.escape(delimiter), str(text))
    # Remove empty sentences and strip extra whitespace
    return [sentence.strip() for sentence in sentences if sentence.strip()]

# Read the input Excel file
try:
    df = pd.read_excel(input_xlsx)

    column_name = df.columns[0] 
    all_sentences = []

    for row in df[column_name]:
        # Split the text in the row into sentences
        sentences = split_text_to_sentences(row)
        # Append each sentence to the list
        all_sentences.extend(sentences)

    # Create a new DataFrame with each sentence as a separate row
    output_df = pd.DataFrame(all_sentences, columns=["Sinhala Sentences"])

    # Write the new DataFrame to an Excel file
    output_df.to_excel(output_xlsx, index=False, engine="openpyxl")
    print(f"Processed sentences saved to {output_xlsx}")

except Exception as e:
    print(f"An error occurred: {e}")
