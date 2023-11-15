import time
import keyboard
import mouse


class PerformanceTracker:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.elapsed_time = None

    def start_timer(self):
        print("Waiting for the next click to start the timer...")
        mouse.wait(button="left")  # Wait for the next mouse click
        self.start_time = time.time()
        print("Timer started. Press any key to stop.")

    def stop_timer(self):
        if self.start_time is not None:
            self.end_time = time.time()
            self.elapsed_time = self.end_time - self.start_time
            print(f"Timer stopped. Elapsed time: {self.elapsed_time:.2f} seconds")
            self.start_time = None
        else:
            print("Timer is not started.")

    def track_performance(self):
        self.start_timer()

        print("Performance tracking in progress...")
        # Check for key press in a loop
        while True:
            if keyboard.read_hotkey():
                break

        self.stop_timer()
