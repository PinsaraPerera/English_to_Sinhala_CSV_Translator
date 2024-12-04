# English to Sinhala CSV Translator

This project provides a Python script to translate English sentences from a CSV file to Sinhala using the Google Translate API (`googletrans` library). The script processes two columns (`Column1` and `Column2`) from the input file, translates the content into Sinhala, and saves the results to a new CSV file.

## Features
- Translates English sentences in `Column1` and `Column2` to Sinhala.
- Handles errors gracefully by skipping problematic rows.
- Includes a delay to prevent rate-limiting when making API calls.
- Can process large files or limit rows for testing.

## Requirements
- Python 3.7 or higher
- Dependencies listed in `requirements.txt`

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/PinsaraPerera/English_to_Sinhala_CSV_Translator.git
   cd English_to_Sinhala_CSV_Translator
   ```

2. Install the required Python libraries using `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Input File Format
- The input CSV file should have two columns: `Column1` and `Column2`, each containing English sentences.
- Example:
  ```csv
  Column1,Column2
  Hello, how are you?,I am fine, thank you.
  Have a great day!,See you tomorrow.
  ```

### Script Execution
1. Place the input CSV file (e.g., `sentences.csv`) in the project directory.
2. Run the script:
   ```bash
   python translate.py
   ```
3. For testing, the script processes only the first 50 rows. To process the entire dataset, modify the script by removing the line:
   ```python
   df = df.head(50)
   ```

### Output File
- The script creates a new CSV file (e.g., `translated_sentences.csv`) containing the original and translated sentences.
- Example output format:
  ```csv
  Column1,Column2,Sinhala_Column1,Sinhala_Column2
  Hello, how are you?,I am fine, thank you.,හෙලෝ, ඔබට කොහොමද?,මම සනීපෙන්, ඔබට ස්තුතියි.
  Have a great day!,See you tomorrow.,සුභ දවසක්!,හෙට හමු වේමු.
  ```

## Customization
- **Delay Between Translations:** Modify the delay (default: 1 second) to suit your needs:
  ```python
  time.sleep(1)
  ```
- **Input/Output Files:** Change the file paths in the script:
 

```python
  input_csv = 'English/your_input_file.csv'
  output_csv = 'Translated/your_output_file.csv'
  ```

## Limitations
- The `googletrans` library relies on Google's free translation API and may encounter rate-limiting for large datasets. Consider adding a longer delay or batching requests if this occurs.
- Accuracy of translations depends on Google Translate.

## Requirements File
The `requirements.txt` file includes all necessary dependencies for the project. To install them, simply run:
```bash
pip install -r requirements.txt
```

### Example `requirements.txt`
```plaintext
pandas==2.2.3
googletrans==4.0.0-rc1
```

## Contributions ❤️
Contributions are welcome! If you find a bug or want to add features, feel free to fork the repository and submit a pull request.

## License
This project is licensed under the `MIT` License.
