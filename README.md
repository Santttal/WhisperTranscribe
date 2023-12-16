# Whisper Transcription Project

This project utilizes OpenAI's Whisper model for text-to-speech transcription. It includes two main components: a transcription script and an audio recording script with a hotkey-triggered interface.

## Prerequisites

Before running the scripts, ensure that you have the following installed:

- Python 3.8 or later
- Whisper
- Pyperclip
- SoundDevice
- Wavio
- Pydub
- Pynput
- Plyer

## Installation

Clone this repository to your local machine:

Install the required Python packages:
```
pip install whisper pyperclip sounddevice wavio pydub pynput plyer
```

## Setting Up the Environment
### Creating the Pipe Path
The transcription script communicates with the recording script via a named pipe. Create this pipe by running:
```
mkfifo /tmp/whisper_pipe
```
### Permissions
Ensure you have the necessary permissions to create the pipe and write files to /tmp/.

## Running the Scripts
### Transcription Script
To start the transcription script, run:
```
python whisper_transcriber.py
```
This script will listen to the named pipe for file paths to transcribed audio files and copy the transcribed text to the clipboard.
## Audio Recording Script
To start the audio recording script, run:
```
python audio_recorder.py
```
Press Alt+A to start and stop audio recording. The script will save the recording and send the file path to the transcription script via the named pipe.

## Notes
Ensure the Whisper model is compatible with your Python version.
Adjust the base path in audio_recorder.py if necessary.
The scripts are set up for a Unix-like environment (Linux, macOS). For Windows, some adjustments might be needed.