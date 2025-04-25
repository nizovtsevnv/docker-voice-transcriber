from flask import Flask, request, jsonify
import whisper
import os

app = Flask(__name__)
model = whisper.load_model("base")
AUDIO_INPUT_DIR = "/app/audio_input"

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'No audio file selected'}), 400

    audio_path = os.path.join(AUDIO_INPUT_DIR, audio_file.filename)
    audio_file.save(audio_path)

    try:
        result = model.transcribe(audio_path)
        os.remove(audio_path)
        return jsonify({'text': result["text"]})
    except Exception as e:
        os.remove(audio_path)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)