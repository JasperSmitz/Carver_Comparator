import HashingValidator
import PerformanceTracker
import Reporter
import TestPrep


def get_test_set_path():
    while True:
        test_type = input("Do you want to test baseline or progressive JPEGs?\n0. Baseline\n1. Progressive\n").lower()
        if test_type == "0":
            return "Test set/Baseline set"
        elif test_type == "1":
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
    fragment_hasher = HashingValidator.FolderHasher()

    fragments = int(input("In how many fragments would you like each file to be split?\n"))
    in_order = bool(int(input("In-order or out-of-order?\n0. Out-of-order\n1. In-order\n")))
    print("Please make sure the test volume is formatted.")

    destination_path = get_destination_path()
    testprep = TestPrep.TestPrep(test_set_path, destination_path, fragments, in_order)
    testprep.prepare_data()
    fragment_hasher.hash_fragments_folder(destination_path)
    input("Please delete the files in the selected drive.\nPress Enter to continue...")

    tracker = PerformanceTracker.PerformanceTracker()
    print("Please prepare the carver or data recovery tool so that starting it is one click away.")

    # Scan Phase
    input("Press Enter to start the scan phase...")
    tracker.track_performance()
    elapsed_time_scan = tracker.elapsed_time_scan
    elapsed_time_carving = tracker.elapsed_time_carving

    performance_data = {
        "Tool": [tool_name],
        "Scan Time": [round(elapsed_time_scan, 2)],
        "Carving Time": [round(elapsed_time_carving, 2)],
    }

    if fragments == 0 or fragments == 1:
        tool_name += "_unfragmented"
    elif in_order:
        tool_name += "_in_order_" + str(fragments) + "_frags"
    elif not in_order:
        tool_name += "_out_of_order_" + str(fragments) + "_frags"

    input("In case the carver/tool did not let you choose an output folder,"
          "\nplease copy the output into the output folder now."
          "\nPress Enter to generate the report.")

    reporter = Reporter.Reporter()
    folder_hasher.compare_to_recovered('Test set/output')
    fragment_hasher.compare_to_recovered('Test set/output')  # Compare fragment hashes
    reporter.create_comparison_table(folder_hasher, fragment_hasher)
    reporter.create_table("Tool Performance", performance_data)
    reporter.export_to_excel(tool_name + "_report.xlsx")


if __name__ == "__main__":
    main()
