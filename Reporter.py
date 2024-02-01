import pandas as pd
import xlsxwriter


class Reporter:
    def __init__(self):
        self.tables = {}

    def create_table(self, table_name, data):
        """
        Create a table with the given name and data.

        Args:
            table_name (string): Name of the table.
            data (dictionary): Dictionary containing the data for the table.
                         Keys are column names, and values are lists of data for each column.
        """
        if table_name in self.tables:
            print(f"Table '{table_name}' already exists. Choose a different name.")
            return

        df = pd.DataFrame(data)
        self.tables[table_name] = df
        print(f"Table '{table_name}' created successfully.")

    def export_to_excel(self, file_name):
        """
        Export all tables to an Excel file.

        Args:
            file_name (string): Name of the Excel file including extension (.xlsx).
        """
        if not file_name.endswith('.xlsx'):
            file_name += '.xlsx'

        with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
            for table_name, df in self.tables.items():
                df.to_excel(writer, sheet_name=table_name, index=False)

        print(f"Tables exported to '{file_name}'.")

    def create_comparison_table(self, folder_hasher, fragment_hasher):
        """
        Create a table comparing original hashes with recovered hashes for both files and fragments.

        Args:
            folder_hasher (FolderHasher): Instance of the FolderHasher class for files.
            fragment_hasher (FolderHasher): Instance of the FolderHasher class for fragments.
        """
        # File comparison data
        comparison_data = {
            'File Name': list(folder_hasher.original_hashes.keys()),
            'Original Hash': list(folder_hasher.original_hashes.values()),
            'Fully Recovered': [
                hash_value in folder_hasher.recovered_hashes.values()
                for hash_value in folder_hasher.original_hashes.values()
            ],
            '100% Partially Recovered': [None] * len(folder_hasher.original_hashes),
            'Partially Recovered': [None] * len(folder_hasher.original_hashes)
        }

        # Fragment comparison data
        fragment_comparison_data = {
            'File Name': list(fragment_hasher.original_hashes.keys()),
            'Original Hash': list(fragment_hasher.original_hashes.values()),
            'Fully Recovered': [
                hash_value in fragment_hasher.recovered_hashes.values()
                for hash_value in fragment_hasher.original_hashes.values()
            ]
        }

        df_files = pd.DataFrame(comparison_data)
        df_fragments = pd.DataFrame(fragment_comparison_data)

        self.tables['Comparison_Files'] = df_files
        self.tables['Comparison_Fragments'] = df_fragments
