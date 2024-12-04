import pandas as pd

# File paths
input_tsv = 'answer-answer.test.tsv'
output_csv = 'converted_file.csv'

# Read the TSV file
try:
    df = pd.read_csv(input_tsv, sep='\t', header=0)
    print("Column Names:")
    print(df.columns.tolist())
    
    # Save the DataFrame to a CSV file
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f".tsv file has been successfully converted to .csv and saved as {output_csv}")
except Exception as e:
    print(f"Error reading or converting the file: {e}")
