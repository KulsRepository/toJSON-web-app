import pandas as pd
import os
import openpyxl
def read_file(filepath):
    """
    This function identifies as spreadsheet's filetype and writes it onto a pandas df

    we will keep updating this to support more and more common spreadsheet formats

    returns a tuple; tuple[pd.DataFrame | None, str]: which is a tuple containing the df and a 
    message string, the df is None if there is an error :p :3
    """
    # this gets the extension
    file_ext = os.path.splitext(filepath)[1].lower()
    df = None
    message = ""

    # We will use a dictionary to map extensions to their corresponding pandas reader functions teehee :3
    readers = {
        '.csv': pd.read_csv,
        '.xls': pd.read_excel,
        '.xlsx': pd.read_excel,
        '.ods': pd.read_excel, # pandas can read ODS with openpyxl or odfpy; that'll have to be imported in toJSON.py
        '.html': pd.read_html,
        '.json': pd.read_json,
        '.pickle': pd.read_pickle,
    }

    if file_ext in readers:
        try:
            rf = readers[file_ext]
            print(f"Detected {file_ext.upper()} file: {filepath}")

            # read_html needs special attention :5
            # that's because it returns a list of dfs :2
            if file_ext == '.html':
                df_list = rf(filepath)
                if df_list:
                    df = df_list[0]
                    message = f'YIPPIE, succesfully read the first tale from {filepath}'
                else:
                    message = f'Error: no tables at {filepath}'
                    df = None
            elif file_ext in ['.csv', '.json']:
                df = rf(filepath, encoding="utf-8")
                message = f"succesfully read {filepath}"
            elif file_ext == '.ods':
                df = rf(filepath, engine='odf')
                message = f"succesfully read {filepath}"
            else:
                df = rf(filepath)
                message = f"succesfully read {filepath}"
        except ImportError:
            # This handles cases where a user doesn't have a required library installed
            # e.g., openpyxl for Excel files or odfpy for ODS files
            if file_ext in ['.xls', '.xlsx']:
                message = f"Error: A required library for '{file_ext}' is not installed. Please try 'pip install openpyxl xlrd'."
            elif file_ext == '.ods':
                message = f"Error: A required library for '.ods' is not installed. Please try 'pip install odfpy'."
            else:
                message = f"Error: A required library for '{file_ext}' is not installed."
            df = None
        except Exception as e:
            message = f"An error occurred while reading '{filepath}': {e}"
            df = None
    else:
        message = f"Unsupported file type: {file_ext}. Only CSV, Excel, ODS, HTML, JSON, and Pickle files are supported."

    return df, message
