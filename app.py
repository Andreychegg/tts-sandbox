from flask import Flask, request, jsonify, send_from_directory
import os
import pyttsx3
from gtts import gTTS

app = Flask(__name__)

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

synthesizer = SpeechSynthesizer()

@app.route("/")
def index():
    return send_from_directory("", "index.html")

@app.route("/synthesize", methods=["POST"])
def synthesize():
    data = request.json
    text = data.get("text", "")
    method = data.get("method", "gtts")

    if not text:
        return jsonify({"error": "Текст не должен быть пустым"}), 400

    if method == "gtts":
        file_path = synthesizer.synthesize_with_gtts(text)
    else:
        file_path = synthesizer.synthesize_with_pyttsx3(text)

    return jsonify({"audio_url": "/" + file_path})

if __name__ == "__main__":
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(debug=True)