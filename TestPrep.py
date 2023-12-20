import os
import shutil


class TestPrep:
    def __init__(self, source_folder, destination_folder, fragments, in_order):
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.fragments = fragments
        self.in_order = in_order

    def fragment_files(self):
        """
        Fragments the files in a given folder into a given number of fragments using binary read and write
        functions.

        Args:

        """
        files = [f for f in os.listdir(self.source_folder) if os.path.isfile(os.path.join(self.source_folder, f))]

        # Create fragments outside the destination folder
        for file_index, file_name in enumerate(files):
            file_path = os.path.join(self.source_folder, file_name)
            with open(file_path, 'rb') as f:
                total_size = os.path.getsize(file_path)
                chunk_size = total_size // self.fragments

                for index in range(self.fragments):
                    start_pos = chunk_size * index
                    end_pos = chunk_size * (index + 1) if index < self.fragments - 1 else total_size

                    f.seek(start_pos)
                    with open(f'fragment_{file_index}_{index}', 'wb') as dat_file:
                        dat_file.write(f.read(end_pos - start_pos))

    def prepare_data(self):
        """
        Prepares the data by copying it in-order (eg. fragment_0_0, then fragment_0_1, then fragment_1_0 etc.)
        or out-of-order (by copying it in the reverse order of in-order)

        Args:
        """
        self.fragment_files()

        num_files = len(os.listdir(self.source_folder))
        project_folder = os.getcwd()  # Gets current working directory

        if self.in_order:
            # Copy files in order
            for fragment_index in range(self.fragments):
                for file_index in range(num_files):
                    file_to_copy = f'fragment_{file_index}_{fragment_index}'
                    src = os.path.join(project_folder, file_to_copy)
                    dst = os.path.join(self.destination_folder, file_to_copy)
                    shutil.move(src, dst)
        else:
            # Copy files out of order (reversed in order)
            for fragment_index in reversed(range(self.fragments)):
                for file_index in reversed(range(num_files)):
                    file_to_copy = f'fragment_{file_index}_{fragment_index}'
                    src = os.path.join(project_folder, file_to_copy)
                    dst = os.path.join(self.destination_folder, file_to_copy)
                    shutil.move(src, dst)
