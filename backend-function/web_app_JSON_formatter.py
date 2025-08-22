import json

"""
This code turns the JSON format from the wanted format to the needed format;
most JSON formats will be written like;

"first one": "peepee",

"second one": "googoo",

"third one": {

    "first of the third": "hththt",

    "uwu": "htgngjrt

},

"fourth one": "googoo"

but that needs to be inputted like:

{"first one": "peepee", "second one": "googoo", "third one": {"first of the third": "hththt", "uwu": "htgngjrt"}, "fourth one": "googoo"}

in the input
"""

def format_json(raw_input_str: str) -> str | None:
    """
    This generally works as a callable function but you can execute it as main.
    """

    print("""
        ----------------------------------------------------
                JSON formatter: multi-line to string        
        ----------------------------------------------------
    Paste your multi-line python dictionary representing the JSON
    data structure below; make sure the keys and string values are
                    enclosed in double quotes.

        IGNORE THIS IF NOT CALLED FROM web_app_JSON_formatter.py
    """)
    try:
        dict_ = json.loads(raw_input_str)

        single_line_JSON = json.dumps(dict_, separators=(',', ':'))

        print(f"""
        \n--------------------------------------------------
             Formatted JSON (this is what is being used):
                        {single_line_JSON}
          --------------------------------------------------
        """)
        return single_line_JSON
    
    except json.JSONDecodeError as e:
        print(f"\nError: Invalid JSON format. Please ensure all keys and strings are in double quotes. Details: {e}")
        return None
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        return None

def main():
    """
    Example usage of the format_template_string function.
    """
    # This is an example of a multi-line, readable JSON string
    multiline_template = """
{
    "user_info": {
        "first_name": "peepee",
        "last_name": "googoo"
    },
    "favorite_word": "hththt",
    "random_data": {
        "data_1": "htgngjrt",
        "data_2": "ghghghjg"
    }
}
"""
    # Call the new function to format the string
    formatted_template = format_json(multiline_template)
    
    if formatted_template:
        print("\n--- Formatted Template ---")
        print("This is the single-line string that would be passed to `toJSON.py`")
        print("Template:", formatted_template)
        print("---")
    else:
        print("\nCould not format the template. Please check the JSON syntax.")

if __name__ == "__main__":
    main()