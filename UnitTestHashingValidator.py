import unittest
import os
from HashingValidator import FolderHasher

class TestFolderHasher(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up a temporary test folder and files
        cls.test_folder = 'test_folder'
        cls.recovered_folder = 'recovered_folder'
        os.makedirs(cls.test_folder, exist_ok=True)
        os.makedirs(cls.recovered_folder, exist_ok=True)
        cls.create_test_files()

    @classmethod
    def create_test_files(cls):
        # Create test files in the test folder
        file_content = b'Test data'
        for i in range(3):
            with open(os.path.join(cls.test_folder, f'test_file_{i}.txt'), 'wb') as f:
                f.write(file_content)

    def test_hash_folder(self):
        # Test hash_folder method
        hasher = FolderHasher()
        hasher.hash_folder(self.test_folder)

        # Add assertions to check if original_hashes are populated correctly
        expected_hashes = {
            os.path.join(self.test_folder, 'test_file_0.txt'): 'hash_value_0',
            os.path.join(self.test_folder, 'test_file_1.txt'): 'hash_value_1',
            os.path.join(self.test_folder, 'test_file_2.txt'): 'hash_value_2',
        }
        self.assertEqual(hasher.original_hashes, expected_hashes)

    def test_compare_to_recovered(self):
        # Test compare_to_recovered method
        hasher = FolderHasher()
        hasher.original_hashes = {
            os.path.join(self.test_folder, 'test_file_0.txt'): 'hash_value_0',
            os.path.join(self.test_folder, 'test_file_1.txt'): 'hash_value_1',
            os.path.join(self.test_folder, 'test_file_2.txt'): 'hash_value_2',
        }

        # Create some recovered hashes
        hasher.recovered_hashes = {
            os.path.join(self.recovered_folder, 'test_file_0_recovered.txt'): 'hash_value_0',
            os.path.join(self.recovered_folder, 'test_file_1_recovered.txt'): 'hash_value_1_wrong',
            os.path.join(self.recovered_folder, 'test_file_2_recovered.txt'): 'hash_value_2',
        }

        # Test the comparison and number of correctly recovered files
        result = hasher.compare_to_recovered(self.recovered_folder)
        self.assertEqual(result, 2)  # Two files should be correctly recovered

    @classmethod
    def tearDownClass(cls):
        # Clean up after the tests by removing test folders
        os.rmdir(cls.test_folder)
        os.rmdir(cls.recovered_folder)

if __name__ == '__main__':
    unittest.main()
