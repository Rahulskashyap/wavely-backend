import schedule
import time
import subprocess
import sys
import os
from datetime import datetime

print("Python Executable:")
print(sys.executable)

def generate_daily_podcast():
    schedule.every().day.at("05:30").do(generate_daily_podcast)

print("Scheduler Started...")
print("Waiting for 05:30 every day...")

while True:
    print(f"[{datetime.now()}] Waiting...")
    schedule.run_pending()
    time.sleep(30)

    print("\n==============================")
    print("Starting Daily Podcast...")
    print("==============================")

    backend_path = os.path.dirname(os.path.abspath(__file__))

    result = subprocess.run(
        [sys.executable, "generate_daily_podcast.py"],
        cwd=backend_path
    )

    if result.returncode == 0:
        print("✅ Podcast Generated Successfully")
    else:
        print("❌ Podcast Generation Failed")