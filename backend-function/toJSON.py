import pandas as pd
import json
import os
from extension_uwu import read_file
from data_structure import transform_to_custom_json
from web_app_JSON_formatter import format_json
import openpyxl


def to_json(input_file_path: str, output_file_path: str, template: dict):
    """
    For now this program identifies a spreadsheet's filetype and converts it to a JSON file.
    
    Returns:
        bool: True if the conversion was successful, False otherwise.
    
    Results in:
        A JSON file at the specified output path.
    """

    if not os.path.exists(input_file_path):
        print(f"Input file {input_file_path} does not exist.")
        return False
    
    try:
        # Now we will get the file extension to determine how to read it, and also initialize the DataFrame
        df, read_msg = read_file(input_file_path)
        print(read_msg)
        
        # Now we can convert the dataframe to JSON teehee :3
        if df is not None:

            header_type = input("Are your headers in columns (c) or rows (r)? ").lower()
            
            # If the user says 'rows', transpose the DataFrame
            if header_type == 'r':
                print("Transposing the data to treat rows as headers.")
                df = df.T
                # The first row of the transposed dataframe is now the column names.
                # We need to set this as the header and clean up the original index.
                df.columns = df.iloc[0]
                df = df[1:].reset_index(drop=True)

            transformed_data = transform_to_custom_json(df, template)   #template will be defined after
            
            # previous function kept just in case -> json_data = df.to_json(orient='records', indent=4)
            with open(output_file_path, 'w', encoding = 'utf-8') as toJSON:
                json.dump(transformed_data, toJSON, indent=4, ensure_ascii= False)

            print(f"Successfully converted {input_file_path} to {output_file_path}")
            return True
        
    # Now to the exceptions!!
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except pd.errors.EmptyDataError as e:
        print(f"Empty data error: {e}")
    except pd.errors.ParserError as e:
        print(f"Parser error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    except ImportError as e:
        print(f"Import error: {e}. Make sure you have the required libraries installed.")

def main():
    input_file_path = r'C:\Users\Kuls\Desktop\code\python\projects\toJSON Github\toJSON\Book2.ods'  # Replace with your input file path
    output_file_path = r'C:\Users\Kuls\Desktop\code\python\projects\toJSON\output_file2.json'  # Replace with your desired output file path

    print("""

    input your data in JSON format line by line and when you are done press control Z, 
    which will show ^Z (or ctrl D -> ^D on Mac/Linux) and hit enter, then answer whether 
    your data is row or column depending and then you'd have your data structure :)

          ^
         /|\
        / | \   Make sure that the first line is just "{" and the last "}" ANDD don't     
        --*--   forget the indents where they are needed :) (like after the curly brackets).
              
    """)
    i = 0
    lines = []
    while True:
        try:
            line = input(f"\n line number {i+1} here: ")
            lines.append(line)
            i += 1
                
        except EOFError:
            break
    template_str = "\n".join(lines)

    try:
        
        formatted_template_str = format_json(template_str)
        if formatted_template_str is None:
            print("Conversion failed due to invalid template.")
            return
        
        custom_template = json.loads(formatted_template_str)
        strawberry_yoghurt = to_json(input_file_path, output_file_path, custom_template)
        if strawberry_yoghurt:
            print("Conversion completed successfully    YIPPIE YIPPIE YIPPE :D :3 :3.")
        else:
            print("Conversion failed.")
    
    except json.JSONDecodeError as e:
        print(f"\nError: Invalid JSON format. Please try again. Details: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()