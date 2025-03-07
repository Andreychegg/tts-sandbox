from flask import Flask, request, jsonify, send_from_directory
from speech.synthesizer import SpeechSynthesizer
import os
import time

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

    if not text:
        return jsonify({"error": "Текст не должен быть пустым"}), 400

    if method == "gtts":
        file_path = synthesizer.synthesize_with_gtts(text, format)
    else:
        file_path = synthesizer.synthesize_with_pyttsx3(text, format)

    timestamp = int(time.time())
    audio_url = f"/{file_path}?t={timestamp}"

    return jsonify({"audio_url": audio_url})

if __name__ == "__main__":
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(debug=True)