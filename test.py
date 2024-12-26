from googletrans import Translator, LANGUAGES
import pandas as pd
import time

# Initialize the translator
translator = Translator()

input_csv = 'standard/complete_sinhala_and_tamil.xlsx'
output_csv = 'standard/complete_sinhala_and_tamil_translated.csv'

try:
    df = pd.read_excel(input_csv)

    if 'Sentences' in df.columns:

        df = df.head(20)

        english_col = df['Sentences'].tolist()
        sinhala_col = []

        for sentence in english_col:
            try:
                translation = translator.translate(sentence, src='en', dest='si')
                sinhala_col.append(translation.text)
                time.sleep(1)
            except Exception as e:
                sinhala_col.append("Error")
                print(f"Error translating sentence: {sentence}\n{e}")

        df_new = pd.DataFrame({'English': english_col, 'Sinhala': sinhala_col})
        df_new.to_csv(output_csv, index=False, encoding='utf-8-sig')

    else:
        print("The required column 'Sentences' does not exist in the CSV file.")


except Exception as e:
    print(f"An error occurred: {e}")