import pyttsx3
from gtts import gTTS

class SpeechSynthesizer:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        self.engine.setProperty("volume", 1.0)

    def synthesize_with_gtts(self, text, format="mp3"): # Синтез gTTS
        output_file = f"static/output_gtts.{format}"
        tts = gTTS(text=text, lang="ru")
        tts.save(output_file)
        return output_file

    def synthesize_with_pyttsx3(self, text, format="wav"): # Синтез pyttsx3
        output_file = f"static/output_pyttsx3.{format}"
        self.engine.save_to_file(text, output_file)
        self.engine.runAndWait()
        return output_file