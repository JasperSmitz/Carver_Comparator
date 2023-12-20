import unittest
import os
import shutil
from TestPrep import TestPrep


class UnitTestTestPrep(unittest.TestCase):

    def setUp(self):
        # Sets up the base folders needed for the tests
        self.test_source_folder = 'test_source'
        self.test_destination_folder = 'test_destination'
        os.makedirs(self.test_source_folder, exist_ok=True)
        os.makedirs(self.test_destination_folder, exist_ok=True)
        self.create_test_files()

    def create_test_files(self):
        # Creates dummy files to test the fragmentation function with
        for i in range(3):
            with open(os.path.join(self.test_source_folder, f'test_file_{i}.txt'), 'w') as f:
                f.write('Test data')

    def test_prepare_data_in_order(self):
        # Tests the prepare_data method with in_order=True
        test_prep = TestPrep(self.test_source_folder, self.test_destination_folder, 2, True)
        test_prep.prepare_data()

        # Checks if the files were fragmented in_order as expected
        expected_files = ['fragment_0_0', 'fragment_0_1', 'fragment_1_0', 'fragment_1_1', 'fragment_2_0', 'fragment_2_1']
        destination_files = os.listdir(self.test_destination_folder)
        self.assertEqual(sorted(expected_files), sorted(destination_files))

    def test_prepare_data_out_of_order(self):
        # Tests the prepare_data method with in_order=False
        test_prep = TestPrep(self.test_source_folder, self.test_destination_folder, 2, False)
        test_prep.prepare_data()

        # Checks if the files were moved out_of_order correctly
        expected_files = ['fragment_2_1', 'fragment_2_0', 'fragment_1_1', 'fragment_1_0', 'fragment_0_1', 'fragment_0_0']
        destination_files = os.listdir(self.test_destination_folder)
        self.assertEqual(sorted(expected_files), sorted(destination_files))

    def tearDown(self):
        # Remove temp folders
        shutil.rmtree(self.test_source_folder)
        shutil.rmtree(self.test_destination_folder)


if __name__ == '__main__':
    unittest.main()
