import subprocess
import os
import psutil
import HashingValidator
import FragChecker
import PerformanceTracker


def create_volume(drive_letter, new_volume_label):
    diskpart_script = f"""
    select disk {drive_letter}
    clean
    create partition primary
    format fs=ntfs label="{new_volume_label}" quick
    assign
    """

    with open('diskpart_script.txt', 'w') as script_file:
        script_file.write(diskpart_script)

    subprocess.run(['diskpart', '/s', 'diskpart_script.txt'], shell=True)

    subprocess.run(['del', 'diskpart_script.txt'], shell=True)


def list_external_drives():
    drives = psutil.disk_partitions(all=True)
    external_drives = []

    for drive in drives:
        if "removable" in drive.opts or "cdrom" in drive.opts:
            external_drives.append(drive.device)

    return external_drives


new_volume_label = "Test Volume"


def create_fragmented_files(directory, num_files, file_size):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)

        for i in range(num_files):
            file_path = os.path.join(directory, f"fragmented_file_{i}.dat")
            with open(file_path, 'wb') as file:
                # Write data to the file
                file.write(b'0' * file_size)
            # Delete the file to leave empty space

    except Exception as e:
        print(f"Error creating fragmented files: {e}")


def main():
    folder_hasher = HashingValidator.FolderHasher()
    folder_hasher.hash_folder("./Test set/jpeg set progressive (SOF2) (100)")
    print("Test set hashes generated!")
    print("Amount recovered succesfully: " + str(folder_hasher.compare_to_recovered("./Test set/output")))

    drive_to_check = "D:"  # Replace with user input in the final console app
    fragmentation_percent = FragChecker.check_drive_fragmentation(drive_to_check)

    if fragmentation_percent is not None:
        print(f"Fragmentation on {drive_to_check}: {fragmentation_percent}%")
    else:
        print(f"Drive {drive_to_check} was not found or an error occurred..")

    tracker = PerformanceTracker.PerformanceTracker()
    tracker.track_performance()


if __name__ == "__main__":
    main()
