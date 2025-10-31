from flask import Flask, request, jsonify
import os
import tempfile
from faster_whisper import WhisperModel
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- Configuration ---
WHISPER_MODEL_OPTIONS = [
    "large-v3-turbo",
    "large-v3",
    "medium",
    "small",
    "tiny",
    "TheChola/whisper-large-v3-turbo-german-faster-whisper",
]
LANGUAGE_OPTIONS = {
    "German": "de",
    "English": "en",
    "Arabic": "ar",
}
GEMINI_MODEL_ALIASES = {
    "pro 2.5": "models/gemini-2.5-pro",
    "flash 2.5 (stable)": "models/gemini-2.5-flash",
    "flash 2.5 lite": "models/gemini-2.5-flash-lite",
}

# --- Whisper Model Caching ---
whisper_models = {}

def get_whisper_model(model_size):
    if model_size not in whisper_models:
        print(f"Loading Whisper model: {model_size}")
        whisper_models[model_size] = WhisperModel(model_size, device="cpu", compute_type="int8")
    return whisper_models[model_size]

# --- Gemini Model Initialization ---
try:
    # It's recommended to set the API key as an environment variable
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    print("GEMINI_API_KEY environment variable not set.")
    # Handle the absence of the API key as you see fit
    # For example, disable Gemini functionality or exit
    # For now, we'll just print a warning
    pass

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    model_size = request.form.get('model', 'tiny')
    language_name = request.form.get('language', 'English')
    language_code = LANGUAGE_OPTIONS.get(language_name)

    if not language_code:
        return jsonify({"error": f"Invalid language: {language_name}"}), 400

    if model_size not in WHISPER_MODEL_OPTIONS:
        return jsonify({"error": f"Invalid model: {model_size}"}), 400

    whisper_model = get_whisper_model(model_size)


    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        audio_file.save(temp_audio.name)
        temp_audio_path = temp_audio.name

    try:
        segments, info = whisper_model.transcribe(temp_audio_path, beam_size=5, language=language_code)
        transcription = "".join(segment.text for segment in segments)
        return jsonify({"transcription": transcription})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(temp_audio_path)

@app.route('/generate', methods=['POST'])
def generate_response():
    data = request.get_json()
    if 'transcription' not in data:
        return jsonify({"error": "No transcription provided"}), 400
    if 'model' not in data:
        return jsonify({"error": "No model specified"}), 400

    transcription = data['transcription']
    model_alias = data['model']
    model_name = GEMINI_MODEL_ALIASES.get(model_alias)

    if not model_name:
        return jsonify({"error": f"Invalid model alias: {model_alias}"}), 400

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(transcription)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
