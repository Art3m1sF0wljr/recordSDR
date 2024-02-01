import subprocess
import schedule
import time
from datetime import datetime
from pydub import AudioSegment
import os

current_recording_timestamp = None  # Variable to store the current recording timestamp

def record():
    global current_recording_timestamp  # Use the global variable
    now = datetime.now()
    current_recording_timestamp = now.strftime("%Y%m%d_%H%M%S")  # Store the current timestamp
    filename = f"{current_recording_timestamp}_sound.wav"
    
    command = f"rtl_fm -f 145575000 -s 12500 -g 35 -p 1 -M fm | sox -t raw -r 12500 -e signed -b 16 -c 1 - -t wav -r 12500 -e signed -b 16 -c 1 {filename}"
    subprocess.Popen(command, shell=True)

def stop_recording():
    global current_recording_timestamp  # Use the global variable
    now = datetime.now()
    input_file_path = f"{current_recording_timestamp}_sound.wav"  # Use the same timestamp for input filename
    output_file_path = f"{current_recording_timestamp}_output.wav"
    
    sound_file = AudioSegment.from_wav(input_file_path)
    sound_dBFS = sound_file.dBFS
    stripped_audio = AudioSegment.strip_silence(
        sound_file, silence_len=1100, silence_thresh=sound_dBFS - 4.15, padding=200)
    stripped_audio.export(output_file_path, format='wav')

    print("input dBFS: {}".format(sound_dBFS))  
    input_file_size = get_file_size_in_megabytes(input_file_path)
    output_file_size = get_file_size_in_megabytes(output_file_path)
    diff_size = input_file_size - output_file_size
    print('input: {:.2f}mb, output: {:.2f}mb, diff: {:.2f}mb'.format(input_file_size, output_file_size, diff_size))
    print("input length: {:.2f} seconds".format(get_audio_duration_in_seconds(sound_file)))  
    print("output length: {:.2f} seconds".format(get_audio_duration_in_seconds(stripped_audio)))  

def get_file_size_in_megabytes(file_path):
    size = os.path.getsize(file_path)
    return size / (1024 * 1024)

def get_audio_duration_in_seconds(sound_file):
    return len(sound_file) / 1000

# Schedule the job to start at 12:01 PM
schedule.every().day.at("12:01:00").do(record)
schedule.every().day.at("18:59:59").do(stop_recording)
schedule.every().day.at("23:30:00").do(record)
schedule.every().day.at("23:59:59").do(stop_recording)

while True:
    schedule.run_pending()
    time.sleep(1)
