import time
import pywinctl
from plyer import notification
# This script tracks the time spent on a specific app and notifies the user when the time limit is reached


# Get user input for the app and time limit
TARGET_APP = input("Enter the name of the app you want to track: ").strip()
TIME_LIMIT = int(input("Enter the time limit in seconds: "))

# Choose exercise & difficulty level
EXERCISE_OPTIONS = {
    "push ups": {"beginner": 10, "intermediate": 20, "advanced": 30},
    "sit ups": {"beginner": 15, "intermediate": 30, "advanced": 45},
    "squats": {"beginner": 20, "intermediate": 40, "advanced": 60},
    "plank": {"beginner": 30, "intermediate": 60, "advanced": 90}
}

# Choose exercise
print("\nChoose and exercise: pushups, squats, situps, plank")
EXERCISE = input("Enter the exercise you want to do: ").strip().lower()

print("\nChoose difficulty level: beginner, intermediate, advanced")
LEVEL = input("Enter difficulty level: ").strip().lower()

# Validate user input
if EXERCISE not in EXERCISE_OPTIONS or LEVEL not in EXERCISE_OPTIONS[EXERCISE]:
    print("Invalid selection! Using default exercise: pushups, beginner level.")
    EXERCISE = "push ups"
    LEVEL = "beginner"

# Set the required reps/time for the chosen exercise
EXERCISE_TARGER = EXERCISE_OPTIONS[EXERCISE][LEVEL]

# Track the time spent on the target app
usage_time = 0 # time spent on the target app in seconds
start_time = None # Track when the user starts using the app

def get_active_window():
    """Returns the title of the currently active window."""
    try:
        active_window = pywinctl.getActiveWindow()
        return active_window.title if active_window else "Unknwn"
    except Exception as e:
        return f"Error: {e}"
    
print(f"\nTracking {TARGET_APP} for {TIME_LIMIT} seconds. When time is up do {EXERCISE_TARGER} {EXERCISE}!")

while True:
    active_app = get_active_window()

    if TARGET_APP.lower() in active_app.lower():
        if start_time is None:
            start_time = time.time() # Start counting time
        usage_time += time.time() - start_time
        start_time = time.time()
    else:
        start_time = None # Reset timer when user switches to another app

    print(f"Active App: {active_app}: {int(usage_time)} seconds")

    if usage_time >= TIME_LIMIT:
        notification.notify(
            title= "Time's Up Buddy!",
            message= f"You've spent {TIME_LIMIT} seconds on {TARGET_APP}, Time for your Workout!",
            timeout = 10
        )
        break # Exit the loop when time limit is reached

    time.sleep(5) # Check every 5 seconds