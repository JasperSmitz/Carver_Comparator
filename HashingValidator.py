import os
import hashlib


class FolderHasher:
    def __init__(self, hash_algorithm='sha256'):
        self.hash_algorithm = hash_algorithm
        self.original_hashes = {}
        self.recovered_hashes = {}

    def hash_folder(self, folder_path):
        """
        Generate hashes for all files in a folder and save them in the original_hashes dictionary.

        Args:
            folder_path (string): Path to the folder that contains the files that need to be hashed.
        """
        self.original_hashes = {}
        print("Generating hashes for original test set...")
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = self.hash_file(file_path)
                self.original_hashes[file_path] = file_hash

    def hash_fragments_folder(self, folder_path):
        """
        Generate hashes for all fragment files in a folder and save them in the original_hashes dictionary.

        Args:
            folder_path (string): Path to the folder that contains the fragment files that need to be hashed.
        """
        self.original_hashes = {}
        print("Generating hashes for fragment test set...")
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = self.hash_file(file_path)
                self.original_hashes[file_path] = file_hash

    def hash_file(self, file_path):
        """
        Generate a hash for a file

        Args:
            file_path (string): The direct path to the file that needs to be hashed.
        """
        hasher = hashlib.new(self.hash_algorithm)
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(65536)
                if not data:
                    break
                hasher.update(data)
        return hasher.hexdigest()

    def compare_to_recovered(self, recovered_folder_path):
        """
        Compare the original hashes to the hashes of output files.

        Args:
            recovered_folder_path (string): The path to the folder containing the recovered files.
        """
        self.recovered_hashes = {}  # Reset the recovered_hashes attribute
        for root, _, files in os.walk(recovered_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = self.hash_file(file_path)
                self.recovered_hashes[file_path] = file_hash
        correctly_recovered = 0
        for file_path, original_hash in self.original_hashes.items():
            if original_hash in self.recovered_hashes.values():
                correctly_recovered += 1

        return correctly_recovered
