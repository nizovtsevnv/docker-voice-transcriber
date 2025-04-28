from flask import Flask, request, jsonify
import os
import logging
import time
import whisper

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

model = whisper.load_model("base")
AUDIO_INPUT_DIR = "/app/audio_input"

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        logger.error('No audio file provided in request')
        return jsonify('No audio file provided'), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        logger.error('Empty filename received')
        return jsonify('No audio file selected'), 400

    audio_path = os.path.join(AUDIO_INPUT_DIR, audio_file.filename)
    logger.info(f'Saving audio file to: {audio_path}')
    audio_file.save(audio_path)

    try:
        start_time = time.perf_counter()
        result = model.transcribe(audio_path, fp16=False)
        text = result["text"].strip()
        os.remove(audio_path)
        transcription_duration = time.perf_counter() - start_time
        logger.debug(f"'{audio_file.filename}' successfully transcribed by {transcription_duration:.1f}s: '{text}'")
        return jsonify(text)
    except Exception as e:
        logger.error(f'Error during transcription: {str(e)}')
        os.remove(audio_path)
        return jsonify(str(e)), 500

if __name__ == '__main__':
    logger.info('Starting Flask application')
    app.run(debug=False, host='0.0.0.0', port=8080)