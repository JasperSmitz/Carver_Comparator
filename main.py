import HashingValidator
import FragChecker
import PerformanceTracker
import Reporter
import TestPrep


def get_test_set_path():
    while True:
        test_type = input("Do you want to test baseline or progressive JPEGs?\n").lower()
        if test_type == "baseline":
            return "Test set/Baseline set"
        elif test_type == "progressive":
            return "Test set/Progressive set"
        else:
            print("Incorrect test type. Please enter 'baseline' or 'progressive'.")


def get_destination_path():
    while True:
        destination_path = input("What drive do you want to perform the test on?\n")
        if destination_path == "C:/":
            print("Cannot perform action on the C:/ drive")
        else:
            return destination_path


def main():
    tool_name = input("What is the name of the tool/carver being tested?\n")

    test_set_path = get_test_set_path()
    folder_hasher = HashingValidator.FolderHasher()
    folder_hasher.hash_folder(test_set_path)

    print("Please make sure the test set volume is formatted.")

    destination_path = get_destination_path()
    testprep = TestPrep.TestPrep(test_set_path, destination_path)
    testprep.copy_to_external_drive()

    input("Please delete the files in the selected drive.\nPress Enter to continue...")

    tracker = PerformanceTracker.PerformanceTracker()
    print("Please prepare the carver or data recovery tool so that starting it is one click away.")
    input("Press Enter to continue...")
    tracker.track_performance()

    performance_data = {"Tool": [tool_name], "Time": [tracker.elapsed_time]}

    reporter = Reporter.Reporter()
    folder_hasher.compare_to_recovered('Test set/output')
    reporter.create_comparison_table(folder_hasher)
    reporter.create_table("Tool Performance", performance_data)
    reporter.export_to_excel(tool_name + "_report.xlsx")


if __name__ == "__main__":
    main()
