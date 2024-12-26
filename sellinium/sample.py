import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome WebDriver
service = Service(executable_path="sellinium/chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

driver = webdriver.Chrome(service=service, options=options)

def translate_text(driver, text):
    """
    Translates a given text using Google Translate and returns the translated result.
    """
    try:
        # Open Google Translate page
        driver.get("https://translate.google.com/?sl=en&tl=si")  # English to Sinhala
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[jsname='BJE2fc']"))
        )

        # Input the text to translate
        input_box = driver.find_element(By.CSS_SELECTOR, "textarea[jsname='BJE2fc']")
        input_box.clear()
        input_box.send_keys(text)

        # Wait for the translation to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span[jsname='W297wb']"))
        )
        translated_text = driver.find_element(By.CSS_SELECTOR, "span[jsname='W297wb']").text
        return translated_text
    except Exception as e:
        print(f"Error translating text: {text} -> {e}")
        return None

def translate_csv(input_file, output_file):
    """
    Translates the content of a CSV file and saves the translations to a new CSV file.
    """
    try:
        # Load the input CSV
        data = pd.read_excel(input_file)
        if 'Sentences' not in data.columns:
            print("The input CSV must have a 'Sentences' column.")
            return
        
        data = data.head(5)
        
        # Prepare a new column for translations
        sinhala = []
        english = data['Sentences'].tolist()

        
        for text in data['Sentences']:
            print(f"Translating: {text}")
            translated_text = translate_text(driver, text)
            sinhala.append(translated_text)
            time.sleep(5)  # Prevent getting blocked by Google
            
        # Save the translations back to a new CSV
        new_df = pd.DataFrame({'Sentences': english, 'Sinhala': sinhala})
        new_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"Translations saved to {output_file}")
    except Exception as e:
        print(f"Error processing CSV: {e}")

if __name__ == "__main__":
    input_csv = 'standard/complete_sinhala_and_tamil.xlsx'
    output_csv = 'standard/complete_sinhala_and_tamil_translated.csv'
    try:
        translate_csv(input_csv, output_csv)
    finally:
        driver.quit()
        print("Done")
