from flask import Flask, request, jsonify, send_from_directory
from speech.synthesizer import SpeechSynthesizer
import os
import time
import asyncio

app = Flask(__name__)
synthesizer = SpeechSynthesizer()

@app.route("/")
def index():
    return send_from_directory("", "index.html")

@app.route("/synthesize", methods=["POST"])
def synthesize():
    data = request.json
    text = data.get("text", "")
    method = data.get("method", "gtts")
    format = data.get("format", "mp3")
    language = data.get("language", "ru") if method == "gtts" else "ru"
    voice = data.get("voice", "ru-RU-SvetlanaNeural")

    if not text:
        return jsonify({"error": "Текст не должен быть пустым"}), 400

    if method == "gtts":
        file_path = synthesizer.synthesize_with_gtts(text, format, language)
    elif method == "pyttsx3":
        file_path = synthesizer.synthesize_with_pyttsx3(text, format)
    elif method == "edgetts":
        file_path = asyncio.run(synthesizer.synthesize_with_edgetts(text, voice, format))
    else:
        return jsonify({"error": "Неподдерживаемый метод синтеза"}), 400

    timestamp = int(time.time())
    audio_url = f"/{file_path}?t={timestamp}"

    return jsonify({"audio_url": audio_url})

if __name__ == "__main__":
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(debug=True)