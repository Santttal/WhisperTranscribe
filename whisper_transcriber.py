import os
import subprocess
import whisper
import pyperclip

class WhisperTranscriber:
    def __init__(self):
        self.model = whisper.load_model("medium")
        print("Whisper model loaded.")

    def transcribe(self, audio_path):
        result = self.model.transcribe(audio_path)
        return result['text']

def send_notification(title, message):
    subprocess.run(['notify-send', title, message])

def main(pipe_path):
    transcriber = WhisperTranscriber()

    if not os.path.exists(pipe_path):
        os.mkfifo(pipe_path)

    while True:
        with open(pipe_path, 'r') as pipe:
            for line in pipe:
                file_path = line.strip()
                if file_path:
                    print(f"Transcribing: {file_path}")
                    text = transcriber.transcribe(file_path)
                    pyperclip.copy(text)
                    print(f"Transcribed text for {file_path} copied to clipboard.")
                    send_notification("Transcription Complete", f"ctrl+V")

if __name__ == "__main__":
    pipe_path = "/tmp/whisper_pipe"
    main(pipe_path)
