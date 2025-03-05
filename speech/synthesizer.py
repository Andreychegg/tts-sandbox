import pyttsx3
from gtts import gTTS

class SpeechSynthesizer:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        self.engine.setProperty("volume", 1.0)

    def synthesize_with_gtts(self, text): # Синтез gTTS
        output_file = "static/output_gtts.mp3"
        tts = gTTS(text=text, lang="ru")
        tts.save(output_file)
        return output_file

    def synthesize_with_pyttsx3(self, text): # Синтез pyttsx3
        output_file = "static/output_pyttsx3.wav"
        self.engine.save_to_file(text, output_file)
        self.engine.runAndWait()
        return output_file