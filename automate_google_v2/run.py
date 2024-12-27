import os
import json
import pandas as pd
from google.cloud import translate_v2 as translate

# Google Translate API function
def translate_text(target: str, text: str) -> str:
    """Translates text into the target language using Google Translate API."""
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target)
    return result["translatedText"]

def get_last_index(json_file: str) -> int:
    """Reads the last translated index from the JSON file."""
    if os.path.exists(json_file):
        with open(json_file, "r") as f:
            data = json.load(f)
        return data.get("last_index", 0)
    return 0

def update_last_index(json_file: str, index: int):
    """Updates the last translated index in the JSON file."""
    with open(json_file, "w") as f:
        json.dump({"last_index": index}, f)

def translate_xlsx_to_csv(input_xlsx: str, output_csv: str, json_file: str, column_name: str, limit: int = 10):
    """Translates sentences in the XLSX file and appends results to a CSV file."""
    # Load Excel data
    df = pd.read_excel(input_xlsx)
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the Excel file.")

    # Get the last translated index
    start_index = get_last_index(json_file)
    end_index = min(start_index + limit, len(df))

    if start_index >= len(df):
        print("All rows have been translated.")
        return

    # Prepare the rows to translate
    rows_to_translate = df.iloc[start_index:end_index]

    # Translate and collect results
    translated_data = []
    for index, row in rows_to_translate.iterrows():
        english_text = row[column_name]
        if isinstance(english_text, str):  # Ensure it's a valid string
            sinhala_translation = translate_text("si", english_text)
            translated_data.append({"English": english_text, "Sinhala": sinhala_translation})

    # Save results to CSV
    output_df = pd.DataFrame(translated_data)
    if os.path.exists(output_csv):
        output_df.to_csv(output_csv, mode="a", index=False, header=False, encoding="utf-8-sig")
    else:
        output_df.to_csv(output_csv, index=False, encoding="utf-8-sig")

    # Update the last translated index
    update_last_index(json_file, end_index)
    print(f"Translated rows {start_index} to {end_index - 1}. Results saved to {output_csv}.")

if __name__ == "__main__":
    # File paths
    input_xlsx = "automate_google_v2/to_process.xlsx"  # Input XLSX file with English sentences
    output_csv = "automate_google_v2/translated_sentences.csv"  # Output CSV file with translations
    json_file = "automate_google_v2/progress.json"  # JSON file to track progress
    column_name = "Sentences"  # Column name with English sentences
    limit = 100  # Number of rows to translate per run

    translate_xlsx_to_csv(input_xlsx, output_csv, json_file, column_name, limit)
