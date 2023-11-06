
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from apps.user.models import Language


def load_languages():
    print("Loading languages...")
    languages = [
        "Albanian",
        "العربية (Arabic)",
        "Հայերեն (Armenian)",
        "বাংলা (Bengali)",
        "Bosnian",
        "Bulgarian",
        "မြန်မာ (Burmese)",
        "中文 (Mandarin)",
        "Danish",
        "German",
        "English",
        "فارسی (Persian)",
        "Finnish",
        "French",
        "ქართული (Georgian)",
        "Ελληνικά (Greek)",
        "עִבְרִית (Hebrew)",
        "हिन्दी (Hindi)",
        "Italian",
        "Indonesian",
        "日本語 (Japanese)",
        "ខ្មែរ (Khmer)",
        "한국어 (Korean)",
        "Croatian",
        "ລາວ (Lao)",
        "मराठी (Marathi)",
        "Maltese",
        "Macedonian",
        "Dutch",
        "Norwegian",
        "Polish",
        "Portuguese",
        "ਪੰਜਾਬੀ (Punjabi)",
        "Romanian",
        "Русский (Russian)",
        "Swedish",
        "Serbian",
        "Slovak",
        "Slovenian",
        "Spanish",
        "Swahili",
        "Tagalog",
        "ไทย (Thai)",
        "Czech",
        "Turkish",
        "Hungarian",
        "اردو (Urdu)",
        "Tiếng Việt (Vietnamese)",

    ]
    for lang in languages:
        Language.objects.create(lang=lang)
        print(f"Language {lang} loaded.")

if __name__ == "__main__":
    load_languages()
    
# python load_languages.py