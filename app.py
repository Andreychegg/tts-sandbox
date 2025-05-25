from flask import Flask, request, jsonify, send_from_directory
from speech.synthesizer import SpeechSynthesizer
from speech.analyzer import SpeechAnalyzer
import os
import time
import asyncio

app = Flask(__name__)
synthesizer = SpeechSynthesizer()
analyzer = SpeechAnalyzer()

@app.route("/")
def index():
    return send_from_directory("", "index.html")


@app.route("/synthesize", methods=["POST"])
def synthesize():
    start_time = time.time()

    data = request.json
    text = data.get("text", "")
    method = data.get("method", "gtts")
    format = data.get("format", "mp3")
    language = data.get("language", "ru") if method == "gtts" else "ru"
    voice = data.get("voice", "ru-RU-SvetlanaNeural")

    if not text:
        return jsonify({"error": "Текст не должен быть пустым"}), 400

    try:
        if method == "gtts":
            file_path = synthesizer.synthesize_with_gtts(text, format, language)
        elif method == "pyttsx3":
            file_path = synthesizer.synthesize_with_pyttsx3(text, format)
        elif method == "edgetts":
            file_path = asyncio.run(synthesizer.synthesize_with_edgetts(text, voice, format))
        else:
            return jsonify({"error": "Неподдерживаемый метод синтеза"}), 400

        synthesis_time = time.time() - start_time
        timestamp = int(time.time())
        audio_url = f"/{file_path}?t={timestamp}"

        return jsonify({
            "audio_url": audio_url,
            "synthesis_time": round(synthesis_time, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/clean-audio", methods=["POST"])
def clean_audio():
    data = request.json
    audio_url = data.get("audio_url", "")

    if not audio_url:
        return jsonify({"error": "Не указан URL аудиофайла"}), 400

    try:
        input_path = audio_url.split('?')[0].lstrip('/')
        output_path = input_path.replace(".", "_clean.")

        success = synthesizer.reduce_noise(input_path, output_path)

        if success:
            timestamp = int(time.time())
            return jsonify({
                "cleaned_audio_url": f"/{output_path}?t={timestamp}",
                "original_audio_url": audio_url
            })
        return jsonify({"error": "Не удалось обработать аудио"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/analyze", methods=["POST"])
def analyze_audio():
    data = request.json
    audio_url = data.get("audio_url", "")

    if not audio_url:
        return jsonify({"error": "Не указан URL аудиофайла"}), 400

    try:
        parts = audio_url.split('?')[0].split('/')
        file_path = '/'.join(parts[3:5])
        analysis_results = analyzer.analyze_audio(file_path)
        return jsonify(analysis_results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(debug=True)