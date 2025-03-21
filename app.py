import os
from flask import Flask, request, jsonify, render_template, send_file
from deep_translator import GoogleTranslator
from gtts import gTTS

app = Flask(__name__)

# Dictionary of supported languages
languages = {
    "hi": "Hindi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "gu": "Gujarati",
    "ur": "Urdu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "zh-CN": "Chinese (Simplified)",
    "ar": "Arabic",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
    "en": "English"
}

@app.route('/')
def home():
    return render_template('index.html', languages=languages)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text', '')
    target_lang = data.get('target_lang', 'en')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Translate the text
        translated_text = GoogleTranslator(source='auto', target=target_lang).translate(text)

        # Generate speech using gTTS
        tts = gTTS(text=translated_text, lang=target_lang)
        audio_path = "static/output.mp3"
        
        # Remove previous file to save memory
        if os.path.exists(audio_path):
            os.remove(audio_path)

        tts.save(audio_path)

        return jsonify({"translated_text": translated_text, "audio_url": audio_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render assigns a dynamic port
    app.run(host='0.0.0.0', port=port, debug=True)
