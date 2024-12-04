import pandas as pd
from googletrans import Translator

# Initialize the translator
translator = Translator()

# File paths
input_file = 'answer-answer.test.tsv'
output_file = 'translated_sentences.csv'

# Read the TSV file (preserve leading/trailing spaces)
df = pd.read_csv(input_file, sep='\t', header=None, quoting=3, keep_default_na=False)
df.columns = ['English']

# Clean up any leading/trailing spaces
df['English'] = df['English'].str.strip()

# Translate each line
translated_sentences = []
for line in df['English']:
    try:
        # Translate the full line
        translation = translator.translate(line, src='en', dest='si')
        translated_sentences.append(translation.text)
    except Exception as e:
        # Append "Error" for failed translations and log the issue
        translated_sentences.append("Error")
        print(f"Error translating line: {line}\n{e}")


df['Sinhala'] = translated_sentences

# Save to CSV
df.to_csv(output_file, index=False, encoding='utf-8')
print(f"Translation complete! Translated file saved to {output_file}")
