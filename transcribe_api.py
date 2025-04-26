from flask import Flask, request, jsonify
import whisper
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

model = whisper.load_model("tiny")
AUDIO_INPUT_DIR = "/app/audio_input"

@app.route('/transcribe', methods=['POST'])
def transcribe():
    logger.debug('Received transcription request')
    
    if 'audio' not in request.files:
        logger.error('No audio file provided in request')
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        logger.error('Empty filename received')
        return jsonify({'error': 'No audio file selected'}), 400

    audio_path = os.path.join(AUDIO_INPUT_DIR, audio_file.filename)
    logger.info(f'Saving audio file to: {audio_path}')
    audio_file.save(audio_path)

    try:
        logger.info('Starting transcription process')
        result = model.transcribe(audio_path, fp16=False)
        logger.debug('Transcription completed successfully')
        os.remove(audio_path)
        logger.info('Audio file removed after processing')
        return jsonify({'text': result["text"]})
    except Exception as e:
        logger.error(f'Error during transcription: {str(e)}')
        os.remove(audio_path)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info('Starting Flask application')
    app.run(debug=True, host='0.0.0.0', port=8080)