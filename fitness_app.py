import time
import pywinctl
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from plyer import notification
from threading import Thread

class FitnessTracker(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Define valid exercises and difficulty levels
        self.EXERCISE_OPTIONS = {
            "push ups": {"beginner": 10, "intermediate": 20, "advanced": 30},
            "sit ups": {"beginner": 15, "intermediate": 30, "advanced": 45},
            "squats": {"beginner": 20, "intermediate": 40, "advanced": 60},
            "plank": {"beginner": 30, "intermediate": 60, "advanced": 90}
        }

        # UI Elements
        self.add_widget(Label(text="Enter the app you want to track:"))
        self.app_input = TextInput(multiline=False)
        self.add_widget(self.app_input)

        self.add_widget(Label(text="Enter time limit (seconds):"))
        self.time_input = TextInput(multiline=False, input_filter='int')
        self.add_widget(self.time_input)

        self.add_widget(Label(text="Choose an exercise: push ups, squats, sit ups, plank"))
        self.exercise_input = TextInput(multiline=False)
        self.add_widget(self.exercise_input)

        self.add_widget(Label(text="Choose difficulty: beginner, intermediate, advanced"))
        self.level_input = TextInput(multiline=False)
        self.add_widget(self.level_input)

        # Status Label (Shows validation messages)
        self.status_label = Label(text="", color=(1, 0, 0, 1))  # Red color for errors
        self.add_widget(self.status_label)

        # Start Button (Initially Disabled)
        self.start_button = Button(text="Start Tracking", on_press=self.start_tracking)
        self.start_button.disabled = True
        self.add_widget(self.start_button)

        # Bind input fields to validation function
        self.app_input.bind(text=self.validate_inputs)
        self.time_input.bind(text=self.validate_inputs)
        self.exercise_input.bind(text=self.validate_inputs)
        self.level_input.bind(text=self.validate_inputs)

    def validate_inputs(self, instance, value):
        """Checks if all inputs are valid and enables Start button"""
        self.status_label.text = ""  # Reset status message

        if not self.app_input.text.strip():
            self.status_label.text = "❌ Please enter an app name!"
            self.start_button.disabled = True
            return

        if not self.time_input.text.strip().isdigit():
            self.status_label.text = "❌ Time limit must be a number!"
            self.start_button.disabled = True
            return

        # Validate Exercise Input (Must exactly match a valid option)
        exercise = self.exercise_input.text.strip().lower()
        if exercise not in self.EXERCISE_OPTIONS:
            self.status_label.text = "❌ Invalid exercise! Choose from push ups, squats, sit ups, plank."
            self.start_button.disabled = True
            return

        # Validate Difficulty Level (Must exactly match beginner, intermediate, advanced)
        level = self.level_input.text.strip().lower()
        if level not in ["beginner", "intermediate", "advanced"]:
            self.status_label.text = "❌ Invalid level! Choose beginner, intermediate, or advanced."
            self.start_button.disabled = True
            return

        self.status_label.text = "✅ All inputs are valid! Ready to start!"
        self.start_button.disabled = False  # Enable button when all inputs are valid

    def start_tracking(self, instance):
        """Starts the tracking process in a separate thread"""
        self.TARGET_APP = self.app_input.text.strip()
        self.TIME_LIMIT = int(self.time_input.text.strip())
        self.EXERCISE = self.exercise_input.text.strip().lower()
        self.LEVEL = self.level_input.text.strip().lower()

        self.EXERCISE_TARGET = self.EXERCISE_OPTIONS[self.EXERCISE][self.LEVEL]

        # Start tracking in a separate thread
        self.status_label.text = f"Tracking {self.TARGET_APP} for {self.TIME_LIMIT} seconds..."
        thread = Thread(target=self.track_usage)
        thread.start()

    def track_usage(self):
        """Tracks app usage and sends a notification when time limit is reached"""
        usage_time = 0
        start_time = None

        while usage_time < self.TIME_LIMIT:
            active_window = pywinctl.getActiveWindow()
            active_app = active_window.title if active_window else "Unknown"

            if self.TARGET_APP.lower() in active_app.lower():
                if start_time is None:
                    start_time = time.time()
                usage_time += time.time() - start_time
                start_time = time.time()
            else:
                start_time = None  # Reset timer when switching away

            self.status_label.text = f"Active: {self.TARGET_APP} - Time: {int(usage_time)}s"
            time.sleep(5)

        notification.notify(
            title="Time's Up!",
            message=f"You've spent {self.TIME_LIMIT} seconds on {self.TARGET_APP}. Time for {self.EXERCISE_TARGET} {self.EXERCISE}!",
            timeout=10
        )
        self.status_label.text = "✅ Time's Up! Do your exercise!"

class MyApp(App):
    def build(self):
        return FitnessTracker()

if __name__ == "__main__":
    MyApp().run()
