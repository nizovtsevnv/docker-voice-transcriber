FROM python:3.9-slim-buster

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install openai-whisper flask
RUN mkdir -p /app/audio_input

COPY transcribe_api.py .

CMD ["python", "transcribe_api.py"]