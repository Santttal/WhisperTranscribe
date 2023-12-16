import os
import threading
import numpy as np
import sounddevice as sd
import wavio
import time
from datetime import datetime
from pydub import AudioSegment
from pynput import keyboard


from plyer import notification

# State to track the number of times Ctrl-Shift-A is pressed
press_count = 0
recording = False
sample_rate = 44100  # Sample rate in Hz


audio_buffer = []
start_time = 0

def play_system_sound():
    # Play a default system sound
    os.system('paplay /usr/share/sounds/freedesktop/stereo/dialog-warning.oga')


def get_file_path():
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_path = '/tmp/whisper'  # Update the base path here
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    return f'{base_path}/audio_recording_{current_time}.wav', f'{base_path}/audio_recording_{current_time}.mp3'

def record_audio():
    global recording, audio_buffer, sample_rate, start_time

    wav_file_path, mp3_file_path = get_file_path()

    with sd.InputStream(samplerate=sample_rate, channels=2, callback=callback):
        while recording:
            sd.sleep(1000)  # Sleeps for 1 second

        # Calculate the duration of the recording
        duration = time.time() - start_time
        print(f"Recording duration: {duration} seconds")

        # Save the recorded audio up to the duration
        num_frames = int(duration * sample_rate)
        audio_data = np.concatenate(audio_buffer, axis=0)[:num_frames]
        wavio.write(wav_file_path, audio_data, sample_rate, sampwidth=2)
        audio_buffer = []  # Clear the buffer

        # Convert WAV to MP3 and send the file name to the pipe
        convert_to_mp3_and_send_filename(wav_file_path, mp3_file_path)

def convert_to_mp3_and_send_filename(wav_path, mp3_path):
    audio = AudioSegment.from_wav(wav_path)
    audio.export(mp3_path, format="mp3")

    # Remove the WAV file after MP3 creation
    os.remove(wav_path)

    # Send the full path of the MP3 file to the pipe
    with open('/tmp/whisper_pipe', 'w') as pipe:
        pipe.write(mp3_path + '\n')


def callback(indata, frames, time, status):
    # This is called for each audio block from the microphone
    if status:
        print(status)
    audio_buffer.append(indata.copy())

def on_activate():
    global press_count, recording, start_time

    press_count += 1

    if press_count == 1:
        # print("Recording started")
        recording = True
        start_time = time.time()
        threading.Thread(target=record_audio).start()
    elif press_count == 2 and recording:
        # print("Recording stopped")
        recording = False
        press_count = 0  # Reset the counter

def for_canonical(f):
    return lambda k: f(l.canonical(k))

hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('<alt>+a'),
    on_activate
)

with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)) as l:
    l.join()
