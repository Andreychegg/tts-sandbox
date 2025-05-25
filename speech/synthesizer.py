import onnxruntime as ort
import numpy as np
import torch
import edge_tts
import pyttsx3
from gtts import gTTS
import os
import noisereduce as nr
from scipy.io import wavfile
from pydub import AudioSegment
import os

class SpeechSynthesizer:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        self.engine.setProperty("volume", 1.0)

    def reduce_noise(self, input_path, output_path):
        """Подавление шума в аудиофайле"""
        try:
            audio = AudioSegment.from_file(input_path)
            temp_path = "temp_clean.wav"
            audio.export(temp_path, format="wav")

            rate, data = wavfile.read(temp_path)

            if len(data.shape) > 1:
                data = data[:, 0]

            reduced = nr.reduce_noise(y=data, sr=rate)
            wavfile.write(output_path, rate, reduced)

            os.remove(temp_path)
            return True
        except Exception as e:
            print(f"Ошибка при подавлении шума: {str(e)}")
            return False

    def _save_audio(self, audio, path, sample_rate, format):
        """Сохранение аудио в файл"""
        if format == 'wav':
            import soundfile as sf
            sf.write(path, audio[0], sample_rate)
        elif format == 'mp3':
            from pydub import AudioSegment
            audio_segment = AudioSegment(
                audio[0].tobytes(),
                frame_rate=sample_rate,
                sample_width=audio[0].dtype.itemsize,
                channels=1
            )
            audio_segment.export(path, format="mp3")
        else:
            raise ValueError(f"Неподдерживаемый формат: {format}")

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