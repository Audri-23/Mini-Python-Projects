import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "gTTS"])

from gtts import gTTS


text = input("Enter the text: ")

tts = gTTS(text=text, lang="en")

tts.save(f"{input("Enter filename to save: ")}.mp3")

print("Audio saved successfully!!")