import subprocess
import os
import psutil
import HashingValidator
import FragChecker
import PerformanceTracker
import Reporter


def main():
    tracker = PerformanceTracker.PerformanceTracker()
    reporter = Reporter.Reporter()
    folder_hasher = HashingValidator.FolderHasher()
    # Generate original test set hashes
    folder_hasher.hash_folder('Test set/jpeg set progressive (SOF2) (100)')

    tool_name = input("What is the name of the tool/carver being tested?")
    # Start the tracking process
    tracker.track_performance()

    performance_data = {"Tool": [tool_name], "Time": [tracker.elapsed_time]}
    # Compare original hashes to recovered hashes
    folder_hasher.compare_to_recovered('Test set/output')
    reporter.create_comparison_table(folder_hasher)

    reporter.create_table("Tool Performance", performance_data)

    # Export tables to Excel
    reporter.export_to_excel(tool_name + "_report.xlsx")


if __name__ == "__main__":
    main()
