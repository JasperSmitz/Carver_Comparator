import time
import keyboard
import mouse


class PerformanceTracker:
    def __init__(self):
        self.start_time_scan = None
        self.end_time_scan = None
        self.elapsed_time_scan = None

        self.start_time_carving = None
        self.end_time_carving = None
        self.elapsed_time_carving = None

    def start_timer(self):
        """
        Start the timer on the next mouse click.

        Args:

        """
        print("Waiting for the next click to start the timer...")
        mouse.wait(button="left")  # Wait for the next mouse click
        self.start_time_scan = time.time()
        print("Scan timer started...\n Press any key to stop.")

    def stop_timer_scan(self):
        """
        Stop the scan timer (if the timer has started).

        Args:

        """
        if self.start_time_scan is not None:
            self.end_time_scan = time.time()
            self.elapsed_time_scan = self.end_time_scan - self.start_time_scan
            print(f"Scan timer stopped. Elapsed time: {self.elapsed_time_scan:.2f} seconds")
            self.start_time_scan = None
        else:
            print("Scan timer is not started.")

    def start_timer_carving(self):
        """
        Start the carving timer on the next mouse click.

        Args:

        """
        input("Press Enter to move on to the carving phase.\n(Only necessary if the tool splits the process up)")
        print("Waiting for the next click to start the carving timer...")
        mouse.wait(button="left")  # Wait for the next mouse click
        self.start_time_carving = time.time()
        print("Carving timer started...\n Press any key to stop.")

    def stop_timer_carving(self):
        """
        Stop the carving timer (if the timer has started).

        Args:

        """
        if self.start_time_carving is not None:
            self.end_time_carving = time.time()
            self.elapsed_time_carving = self.end_time_carving - self.start_time_carving
            print(f"Carving timer stopped. Elapsed time: {self.elapsed_time_carving:.2f} seconds")
            self.start_time_carving = None
        else:
            print("Carving timer is not started.")

    def track_performance(self):
        """
        Track the time until a key is pressed.

        Args:

        """
        self.start_timer()

        # Check for key press in a loop
        while True:
            if keyboard.read_hotkey():
                break

        self.stop_timer_scan()

        self.start_timer_carving()

        # Check for key press in a loop
        while True:
            if keyboard.read_hotkey():
                break

        self.stop_timer_carving()
