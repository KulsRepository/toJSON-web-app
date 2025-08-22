import pandas as pd
import json

def apply_template_to_row(template: dict, row: pd.Series):
    """
    This program recursively applies a JSON template to a single row of a df
    
    args:
        template -> dictionary: this is for the desired JSON structure; 
        it's a dictionary template that explains how it should be formed

        row -> Series from Pandas: this is for a single data row from the df

    returns:
        dictionary!! It returns a new dictionary with the data filled in 
        according to the template 
    """
    trans_dict = {}
    for key, val in template.items():
        if isinstance(val, dict):   # If the value val is another dictionary let's have a recursion
            trans_dict[key] = apply_template_to_row(val, row)
        elif isinstance(val, str):  # If the value is a string then we have a column name
            trans_dict[key] = row.get(val)
        else:   #else, for other datatypes
            trans_dict[key] = val

    return trans_dict

def transform_to_custom_json(df: pd.DataFrame, template: dict) -> list:
    """
    This function takes the dataframe from toJSON.py and turns it into a 
    specific JSON structure

    arguments: df (a dataframe teehee)

    returns: a list of dictionaries in the form of the new JSON structure
    """

    trans_data = []

    for idx, row in df.iterrows():
       
       new_row = apply_template_to_row(template, row)
       trans_data.append(new_row)
    
    return trans_data