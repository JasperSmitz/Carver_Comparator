import os
import shutil


class TestPrep:
    def __init__(self, source_folder, destination_folder):
        self.source_folder = source_folder
        self.destination_folder = destination_folder

    # Eventually look into replacing this with images.
    def copy_to_external_drive(self):
        """
        Copies data from the selected test set over to the external hard drive

        """
        if not os.path.exists(self.source_folder):
            print(f"Source folder '{self.source_folder}' does not exist.")
            return

        if not os.path.exists(self.destination_folder):
            print(f"Destination folder '{self.destination_folder}' does not exist.")
            return

        print(f"Copying files from '{self.source_folder}' to '{self.destination_folder}'...")
        for root, dirs, files in os.walk(self.source_folder):
            for file in files:
                source_file = os.path.join(root, file)
                relative_path = os.path.relpath(source_file, self.source_folder)
                destination_file = os.path.join(self.destination_folder, relative_path)

                destination_directory = os.path.dirname(destination_file)
                if not os.path.exists(destination_directory):
                    os.makedirs(destination_directory)

                shutil.copy2(source_file, destination_file)

        print("Files copied successfully.")
