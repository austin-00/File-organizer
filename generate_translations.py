import os
import xml.etree.ElementTree as ET
from deep_translator import GoogleTranslator

# The languages we want to support
LANGUAGES = {
    "es": "spanish",
    "fr": "french",
    "de": "german",
    "zh-CN": "chinese (simplified)",
    "ar": "arabic",
    "hi": "hindi",
    "pt": "portuguese",
    "ru": "russian",
    "ja": "japanese",
    "it": "italian",
    "ko": "korean",
    "tr": "turkish",
    "nl": "dutch",
    "pl": "polish",
    "id": "indonesian",
    "vi": "vietnamese",
    "th": "thai",
    "sv": "swedish",
    "da": "danish"
}

def translate_text(text, target_lang):
    try:
        # Google Translate has a 5000 char limit per request, our strings are short so it's fine
        translated = GoogleTranslator(source='en', target=target_lang).translate(text)
        return translated
    except Exception as e:
        print(f"Error translating '{text}' to {target_lang}: {e}")
        return text # Fallback to English if it fails

def main():
    base_ts_path = "ui/translations/app_en.ts"
    if not os.path.exists(base_ts_path):
        print(f"Error: Could not find {base_ts_path}. Please run pyside6-lupdate first!")
        return

    # Parse the English .ts file
    tree = ET.parse(base_ts_path)
    root = tree.getroot()

    for lang_code, lang_name in LANGUAGES.items():
        print(f"\n--- Generating translations for: {lang_name} ({lang_code}) ---")
        
        # Update the language attribute in the XML
        root.set("language", lang_code)
        
        # Find all the text strings and translate them
        for context in root.findall("context"):
            for message in context.findall("message"):
                source = message.find("source").text
                translation_node = message.find("translation")
                
                if source:
                    print(f"Translating: {source} -> ...", end=" ")
                    translated_text = translate_text(source, lang_name.split(" ")[0])
                    translation_node.text = translated_text
                    print(translated_text)

        # Save the new .ts file
        output_path = f"ui/translations/app_{lang_code}.ts"
        tree.write(output_path, encoding="utf-8", xml_declaration=True)
        print(f"Saved: {output_path}")

if __name__ == "__main__":
    main()