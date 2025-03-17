import edge_tts
import pyttsx3
from gtts import gTTS


class SpeechSynthesizer:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        self.engine.setProperty("volume", 1.0)

    def synthesize_with_gtts(self, text, format="mp3", lang="ru"):
        output_file = f"static/output_gtts.{format}"
        tts = gTTS(text=text, lang=lang)
        tts.save(output_file)
        return output_file

    def synthesize_with_pyttsx3(self, text, format="wav"):
        output_file = f"static/output_pyttsx3.{format}"
        self.engine.save_to_file(text, output_file)
        self.engine.runAndWait()
        return output_file

    async def synthesize_with_edgetts(self, text, voice="ru-RU-SvetlanaNeural", format="mp3"):
        output_file = f"static/output_edgetts.{format}"
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        return output_file
