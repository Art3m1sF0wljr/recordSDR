import subprocess
import schedule
import time
from datetime import datetime

def record():
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_sound.wav"
    
    # Replace this command with your original command
    command = f"rtl_fm -f 145575000 -s 12500 -g 35 -p 1 -M fm | sox -t raw -r 12500 -e signed -b 16 -c 1 - -t wav -r 12500 -e signed -b 16 -c 1 {filename}"
    subprocess.Popen(command, shell=True)

def stop_recording():
    # This command will kill all processes containing the specified keywords
    # Adjust it according to your system and processes
    subprocess.run("pkill -f 'rtl_fm|sox'", shell=True)

def job():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Job started at", current_time)
    record()

# Schedule the job to start at 12:01 PM
schedule.every().day.at("12:01:00").do(job)

# Schedule the stop_recording function to run at 18:59:59
schedule.every().day.at("18:59:59").do(stop_recording)

schedule.every().day.at("23:30:00").do(job)
schedule.every().day.at("23:59:59").do(stop_recording)

while True:
    schedule.run_pending()
    time.sleep(1)
