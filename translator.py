import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "googletrans"])

from googletrans import Translator

translator = Translator()

text = input("Enter text to translate: ")
target_language = "es"

result = translator.translate(text, dest=target_language)
print(f"Translated to {target_language}: {result.text}")
