import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# Set up Chrome WebDriver
service = Service(executable_path="sellinium/chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Optional: Run in headless mode (disable if debugging)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--incognito')  # Use incognito mode
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')

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

        # Simulate typing character by character
        for char in text:
            input_box.send_keys(char)
            time.sleep(0.1)  # Add a slight delay between key presses

        # Wait for the translation to appear and stabilize
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "span[jsname='W297wb']"), "")
        )
        time.sleep(2)  # Allow extra time for the translation to stabilize

        translated_text = driver.find_element(By.CSS_SELECTOR, "span[jsname='W297wb']").text

        # Check if translation is complete
        for _ in range(3):
            time.sleep(1)  # Wait to ensure translation is fully updated
            new_text = driver.find_element(By.CSS_SELECTOR, "span[jsname='W297wb']").text
            if new_text != translated_text:
                translated_text = new_text
            else:
                break

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

        data = data.head(5)  # For testing, limit to 5 rows

        # Prepare a new column for translations
        sinhala = []
        english = data['Sentences'].tolist()

        for text in english:
            print(f"Translating: {text}")
            translated_text = translate_text(driver, text)
            sinhala.append(translated_text)
            time.sleep(5)  # Add a delay to prevent getting flagged as a bot

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
