import os
import hashlib


class FolderHasher:
    def __init__(self, hash_algorithm='sha256'):
        self.hash_algorithm = hash_algorithm
        self.original_hashes = {}

    def hash_folder(self, folder_path):
        """Generate hashes for all files in a folder and save them in the original_hashes dictionary."""
        self.original_hashes = {}
        print("Generating hashes for original test set...")
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = self.hash_file(file_path)
                self.original_hashes[file_path] = file_hash
        print(self.original_hashes)

    def hash_file(self, file_path):
        """Generate a hash for a file"""
        hasher = hashlib.new(self.hash_algorithm)
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(65536)
                if not data:
                    break
                hasher.update(data)
        return hasher.hexdigest()

    def compare_to_recovered(self, recovered_folder_path):
        """Compare the original hashes to the hashes of output files."""
        recovered_hashes = {}
        for root, _, files in os.walk(recovered_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = self.hash_file(file_path)
                recovered_hashes[file_hash] = True
        print(recovered_hashes)
        correctly_recovered = 0
        for file_path, original_hash in self.original_hashes.items():
            if original_hash in recovered_hashes:
                correctly_recovered += 1

        return correctly_recovered