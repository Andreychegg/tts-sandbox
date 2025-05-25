import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment
import nltk
from nltk.tokenize import word_tokenize
import warnings
import os
from statistics import mean

from pydub.silence import detect_silence

warnings.filterwarnings("ignore")
nltk.download('punkt', quiet=True)


class SpeechAnalyzer:
    def __init__(self):
        self.vowels = "аеёиоуыэюяaeiouy"

    def analyze_audio(self, audio_path):
        """Основная функция анализа аудио"""
        if not os.path.exists(audio_path):
            return {"error": f"Файл {audio_path} не найден"}

        try:
            y, sr = librosa.load(audio_path, sr=None)
            duration = librosa.get_duration(y=y, sr=sr)
        except Exception as e:
            return {"error": f"Ошибка загрузки аудиофайла: {str(e)}"}

        results = {
            "basic_metrics": self._analyze_basic_metrics(y, sr, duration),
            "pauses": self._analyze_pauses(y, sr),
            "pitch": self._analyze_pitch(y, sr),
            "quality": self._analyze_quality(y, sr)
        }

        return results

    def _analyze_basic_metrics(self, y, sr, duration):
        """Анализ базовых метрик"""
        energy = librosa.feature.rms(y=y)[0]
        return {
            "duration": duration,
            "sample_rate": sr,
            "energy": {
                "mean": float(np.mean(energy)),
                "std": float(np.std(energy)),
                "dynamic_range": float(np.max(energy) - np.min(energy))
            },
            "speech_rate": self._estimate_speech_rate(y, sr, duration)
        }

    def _analyze_pauses(self, y, sr):
        """Анализ пауз"""
        audio_seg = AudioSegment(
            y.tobytes(),
            frame_rate=sr,
            sample_width=y.dtype.itemsize,
            channels=1
        )

        silence = detect_silence(audio_seg, min_silence_len=200, silence_thresh=-40)
        pause_durs = [(end - start) / 1000 for start, end in silence]

        return {
            "count": len(pause_durs),
            "total_duration": sum(pause_durs),
            "average_duration": mean(pause_durs) if pause_durs else 0
        }

    def _analyze_pitch(self, y, sr):
        """Анализ тона"""
        f0, voiced_flag, _ = librosa.pyin(y, fmin=80, fmax=400, sr=sr)
        f0_values = f0[voiced_flag]

        if len(f0_values) > 0:
            return {
                "mean": float(np.mean(f0_values)),
                "std": float(np.std(f0_values)),
                "range": float(np.max(f0_values) - np.min(f0_values))
            }
        return {"error": "Не удалось определить тон"}

    def _analyze_quality(self, y, sr):
        """Анализ качества"""
        mfccs = librosa.feature.mfcc(y=y, sr=sr)
        return {
            "mfcc_stability": float(np.mean(np.std(mfccs, axis=1))),
            "harmonicity": float(librosa.effects.harmonic(y).mean())
        }

    def _estimate_speech_rate(self, y, sr, duration):
        """Оценка скорости речи"""
        speech_frames = librosa.effects.split(y, top_db=30)
        speech_duration = sum(end - start for start, end in speech_frames) / sr
        return {
            "speech_ratio": speech_duration / duration if duration > 0 else 0,
            "estimated_wpm": (len(speech_frames) / duration) * 60 if duration > 0 else 0
        }