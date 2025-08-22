import os
import sys
from flask import jsonify
import pandas as pd
import json
import openpyxl
import functions_framework

# This next move is gonna make us able to take in the files from the
# rest of the directories :3
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.insert(0, parent_dir)

# I'll make it a try-except for clarity:
try:
    from toJSON import transform_to_custom_json
    from toJSON import format_json
    from extension_uwu import read_file
except ImportError as e:
    print(f"Error importing modules from parent directory: {e}")

# The reason I separated the directories is because then the web-app can be
# seen by itself and the functions can be abstracted. if you want to understand
# the functions by themselves then look at their code in the parent directory :3

@functions_framework.http   # this is for GitHub pages, my other code for this was for a normal web-page
def convert_to_json(request):
    """This is a function that processes http requests with the spreadsheet files
        and the JSON template, and then returns a result :)"""
    if request.method != 'POST':
        return jsonify({"success": False, "message": "Method not allowed: use POST"}), 405  #that's the error code that says that the request's http method isn't supported
    
    file = request.files.get('file')    # this gets the spreadsheet uwu
    template_str = request.form.get('template') # this gets the JSON template input, both of these are named in the index.html document

    if not file:
        return jsonify({"success": False, "message": "no file part in the request."}), 400
    if file.filename == '':
        return jsonify({"success": False, "message": "no selected file"}), 400
    if not template_str:
        return jsonify({"success": False, "message": "no provided JSON template"}), 400
    
    # Now we move onto working with the file directly in the memory
    try:
        # 1: format and parse the user's JSON template :p
        formatted_template_str = format_json(template_str)
        if formatted_template_str is None:
            return jsonify({"success": False, "message": "Invalid JSON format."}), 400
        
        custom_template = json.loads(formatted_template_str)

        # 2: now we read the spreadsheet file with extension_uwu
        df, read_msg = read_file(file)

        if df is None:
            return jsonify({"success": False, "message": read_msg}), 400
        
        # 3: noww we can handle the row or column headers

        transformed_data = transform_to_custom_json(df, custom_template)

        # 4: now we can finally return the converted JSON data and it is done :)
        return jsonify({"success": True, "data": transformed_data}), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"An unexpected error occurred: {str(e)}"}), 500