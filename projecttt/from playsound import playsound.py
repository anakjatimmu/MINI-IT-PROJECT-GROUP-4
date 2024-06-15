from playsound import playsound

def play_alarm_sound():
    alarm_file_path = "c:\Users\JAY\Downloads\Telegram Desktop\Timer Sound Effect.mp3"
    playsound(alarm_file_path)

import os
from datetime import datetime

def track_session(session_duration):
    sessions_file = "sessions.txt"
    if not os.path.exists(sessions_file):
        with open(sessions_file, "w") as f:
            f.write("Date,Duration\n")
    
    with open(sessions_file, "a") as f:
        now = datetime.now()
        
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{date_time},{session_duration}\n")

def calculate_session_stats():
    sessions_file = "sessions.txt"
    total_sessions = 0
    total_duration = 0
    
    if os.path.exists(sessions_file):
        with open(sessions_file, "r") as f:
            next(f)  
            for line in f:
                data = line.strip().split(",")
                total_sessions += 1
                total_duration += int(data[1])
    
    return total_sessions, total_duration


