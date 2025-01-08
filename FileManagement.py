import pandas as pd

class FileManagement:
    @staticmethod
    def read_csv(file):
        try:
            df = pd.read_csv(file)
            if df.empty:
                print(f"Warning: File {file} is empty.")
            return df
        except FileNotFoundError:
            print(f"Error: File {file} not found.")
        except PermissionError:
            print(f"Error: Permission denied for reading {file}.")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return None


    @staticmethod
    def write_csv(file, df):
        try:
            df.to_csv(file, index=False)
            print(f"File {file} written successfully.")
        except PermissionError:
            print(f"Error: Permission denied for writing to {file}.")
        except Exception as e:
            print(f"Unexpected error: {e}")


    @staticmethod
    def append_file(file, row):
        try:
            df = pd.read_csv(file)
            new_row = pd.DataFrame([row])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(file, index=False)
            print("Row appended successfully.")
        except FileNotFoundError:
            print(f"Error: File {file} not found.")
        except PermissionError:
            print(f"Error: Permission denied for accessing {file}.")
        except Exception as e:
            print(f"Unexpected error: {e}")

    @staticmethod
    def update_csv(file, search_column, search_value, update_column, new_value):
        try:
            df = pd.read_csv(file)
            if search_column in df.columns and update_column in df.columns:
                row_index = df[df[search_column] == search_value].index
                if not row_index.empty:
                    df.loc[row_index, update_column] = new_value
                    df.to_csv(file, index=False)
                    print("Update successful.")
                else:
                    print("Value not found in the specified column.")
            else:
                print("Error: One or more columns not found in the CSV.")
        except FileNotFoundError:
            print(f"Error: File {file} not found.")
        except PermissionError:
            print(f"Error: Permission denied for accessing {file}.")
        except Exception as e:
            print(f"Unexpected error: {e}")

    @staticmethod
    def delete_row(file, search_column, search_value):
        try:
            df = pd.read_csv(file)
            original_length = len(df)
            df = df[df[search_column] != search_value]
            if len(df) < original_length:
                df.to_csv(file, index=False)
                print("Row deleted successfully.")
            else:
                print("Value not found, no rows deleted.")
        except FileNotFoundError:
            print(f"Error: File {file} not found.")
        except PermissionError:
            print(f"Error: Permission denied for accessing {file}.")
        except Exception as e:
            print(f"Unexpected error: {e}")


