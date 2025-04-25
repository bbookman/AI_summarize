#!/usr/bin/env python3
import schedule
import time
import os
import sys
import datetime
import subprocess
import pytz
from pathlib import Path

# Add parent directory to sys.path to allow importing from src
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

def run_summarizer():
    """Run the main.py script for AI summarizer."""
    print(f"\n=== Scheduled Run at {datetime.datetime.now()} ===")
    
    # Get the path to main.py - try different possible locations
    possible_paths = [
        os.path.join(current_dir, "src", "main.py"),                        # /python-directory-reader/src/main.py
        os.path.join(parent_dir, "src", "main.py"),                         # /AI_summarize/src/main.py
        os.path.join(current_dir.parent.parent, "src", "main.py")           # /code/AI_summarize/src/main.py
    ]
    
    # Try each path until we find one that exists
    main_script = None
    for path in possible_paths:
        if os.path.exists(path):
            main_script = path
            print(f"✓ Found main script at: {main_script}")
            break
    
    # If no valid path was found, exit with error
    if not main_script:
        print(f"❌ FATAL ERROR: Cannot find main script. Tried the following paths:")
        for path in possible_paths:
            print(f"  - {path}")
        print("The application will now exit. Please check your directory structure.")
        sys.exit(1)
    
    # Run the script as a subprocess
    try:
        subprocess.run([sys.executable, main_script], check=True)
        print(f"✓ Summarizer completed successfully at {datetime.datetime.now()}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Summarizer failed with error code {e.returncode}")
        print("The application will exit due to this error.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running summarizer: {e}")
        print("The application will exit due to this error.")
        sys.exit(1)

def get_time_until_next_run():
    """Calculate and display time until next scheduled run."""
    est_tz = pytz.timezone('US/Eastern')
    now = datetime.datetime.now(est_tz)
    
    # Calculate next run time (1 AM EST)
    next_run = now.replace(hour=1, minute=0, second=0, microsecond=0)
    if now.hour >= 1:  # If it's already past 1 AM, schedule for tomorrow
        next_run += datetime.timedelta(days=1)
    
    # Calculate time difference
    time_diff = next_run - now
    hours, remainder = divmod(time_diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return f"{time_diff.days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

def main():
    print("\n=== AI Summarizer Scheduler ===")
    print("Setting up scheduled job to run daily at 1:00 AM EST")
    
    # Schedule the job to run at 1 AM EST
    schedule.every().day.at("01:00").do(run_summarizer)
    
    # Check if we need to run immediately
    if len(sys.argv) > 1 and sys.argv[1] == "--run-now":
        print("Running summarizer immediately...")
        run_summarizer()

    # Display time until next run
    print(f"Next scheduled run in {get_time_until_next_run()}")
    
    # Keep the script running and check the schedule
    while True:
        schedule.run_pending()
        
        # Sleep for 30 seconds before checking again
        for _ in range(10):  # Update countdown every 3 seconds
            sys.stdout.write(f"\rNext run in {get_time_until_next_run()}. Press Ctrl+C to exit.")
            sys.stdout.flush()
            time.sleep(3)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScheduler stopped by user. Exiting...")
        sys.exit(0)