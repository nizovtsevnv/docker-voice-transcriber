FROM python:3.9-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg
RUN pip install --upgrade pip
RUN pip install openai-whisper flask
RUN mkdir -p /app/audio_input

COPY transcribe_api.py .

CMD ["python", "transcribe_api.py"]