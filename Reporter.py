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

    def create_comparison_table(self, folder_hasher):
        """
        Create a table comparing original hashes with recovered hashes.

        Args:
            folder_hasher (FolderHasher): Instance of the FolderHasher class.
        """
        comparison_data = {
            'File Name': list(folder_hasher.original_hashes.keys()),
            'Original Hash': list(folder_hasher.original_hashes.values()),
            'Fully Recovered': [
                hash_value in folder_hasher.recovered_hashes.values()
                for hash_value in folder_hasher.original_hashes.values()
            ]
        }
        self.create_table('Comparison', comparison_data)