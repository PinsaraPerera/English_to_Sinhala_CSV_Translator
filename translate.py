import pandas as pd
import time
from googletrans import Translator

# Initialize the translator
translator = Translator()

# File paths
input_csv = 'English/images.csv'
output_csv = 'Translated/images.csv'  # Output CSV file

# Read the CSV file
try:
    df = pd.read_csv(input_csv)
    
    # Check if required columns exist
    if 'Column1' in df.columns and 'Column2' in df.columns:

        df = df.head(50) # Limit the number of rows to 50 for testing purposes  <--- remove this line to translate the entire file

        # Translate sentences in Column1 and Column2
        sinhala_col1 = []
        sinhala_col2 = []

        for sentence1, sentence2 in zip(df['Column1'], df['Column2']):
            try:
                # Translate Column1
                translation1 = translator.translate(sentence1, src='en', dest='si')
                sinhala_col1.append(translation1.text)
                time.sleep(1)  # Add a delay of 1 second
            except Exception as e:
                sinhala_col1.append("Error")
                print(f"Error translating Column1: {sentence1}\n{e}")
            
            try:
                # Translate Column2
                translation2 = translator.translate(sentence2, src='en', dest='si')
                sinhala_col2.append(translation2.text)
                time.sleep(1)  # Add a delay of 1 second
            except Exception as e:
                sinhala_col2.append("Error")
                print(f"Error translating Column2: {sentence2}\n{e}")
        
        # Add the translated columns to the DataFrame
        df['Sinhala_Column1'] = sinhala_col1
        df['Sinhala_Column2'] = sinhala_col2

        # Save the updated DataFrame to a new CSV file
        df.to_csv(output_csv, index=False, encoding='utf-8')
        print(f"Translation complete! Translated file saved as {output_csv}")
    else:
        print("The required columns 'Column1' and 'Column2' do not exist in the CSV file.")
except Exception as e:
    print(f"Error processing the file: {e}")
