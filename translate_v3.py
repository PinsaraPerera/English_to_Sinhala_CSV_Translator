import os
from google.cloud import translate_v3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve project ID from .env
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

if not PROJECT_ID:
    raise ValueError("The PROJECT_ID is not set. Please set it in the .env file.")

def translate_text(
    text: str = "Hello, how are you?",
    language_code: str = "fr",
):
    """Translating Text from English.
    Args:
        text: The content to translate.
        language_code: The language code for the translation.
            E.g. "fr" for French, "es" for Spanish, etc.
    """

    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{PROJECT_ID}/locations/global"

    # Translate text
    response = client.translate_text(
        contents=[text],
        target_language_code=language_code,
        parent=parent,
        mime_type="text/plain",  # Supported mime types: "text/plain", "text/html"
        source_language_code="en",
    )

    # Display translations
    for translation in response.translations:
        print(f"Translated text: {translation.translated_text}")

    return translation.translated_text


if __name__ == "__main__":
    result = translate_text("A female toddler in pigtails is trying to climb out of a green and white playpen", "si")
    with open("translated_text.txt", "a", encoding='utf-8-sig') as f:
        f.write(result)
