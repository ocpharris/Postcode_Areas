import argparse
import pandas as pd
import requests
import zipfile
import io
import sys
import os
from datetime import datetime


def select_postcode_csv(postcode):

        # Define the mapping of postcode ranges to CSV file names
        postcode_mapping = {
            'A': 'A-E',
            'B': 'A-E',
            'C': 'A-E',
            'D': 'A-E',
            'E': 'A-E',
            'F': 'F-J',
            'G': 'F-J',
            'H': 'F-J',
            'I': 'F-J',
            'J': 'F-J',
            'K': 'K-O',
            'L': 'K-O',
            'M': 'K-O',
            'N': 'K-O',
            'O': 'K-O',
            'P': 'P-T',
            'Q': 'P-T',
            'R': 'P-T',
            'S': 'P-T',
            'T': 'P-T',
            'U': 'U-Z',
            'V': 'U-Z',
            'W': 'U-Z',
            'X': 'U-Z',
            'Y': 'U-Z',
            'Z': 'U-Z',
        }


        # Check if the input postcode is valid
        if len(postcode) < 1 or not postcode[0].isalpha():
            return None  # Invalid postcode

        # Get the relevant CSV file based on the first letter of the postcode
        csv_file = postcode_mapping.get(postcode[0].upper())
        path = os.path.abspath(os.path.join(os.path.dirname("__file__"), '..', csv_file))



        sys.path.append(path)

        if csv_file:
            # Read the CSV file into a DataFrame
            try:
                df = pd.read_csv(csv_file)
                return df
            except FileNotFoundError:
                return None  # CSV file not found
        else:
            return None  # No matching CSV file for the input postcode
        
# extracts LSOA and MSOA of inputted postcode 
def postcode_to_OAs(df, postcode):
    df_row = df[df['pcd7'] == postcode]
    lsoa =df_row['lsoa11nm'].iloc[0]
    msoa = df_row['msoa11nm'].iloc[0]
    la = df_row['ladnm'].iloc[0]

    postcode_data = {
    'Postcode': [postcode],
    'LSOA': [lsoa],
    'MSOA': [msoa],
    'Local Authority' : [la]
}

    # Create a DataFrame from the sample data
    df = pd.DataFrame(postcode_data)

        # Get the current date
    current_date = datetime.now()

    # Format the date as "dd_mm_yy"
    formatted_date = current_date.strftime("%d_%m_%y")


    # Define the output file path
    output_csv_file = f"MSOA_LSOA_{postcode}_{formatted_date}.csv"


    # Write the DataFrame to a CSV file
    df.to_csv(output_csv_file, index=False)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process postcode data.")
    parser.add_argument("--postcode", type=str, help="Postcode to process")
    args = parser.parse_args()

    if args.postcode:
        df = select_postcode_csv(args.postcode)  # Get the DataFrame
        if df is not None:
            postcode_to_OAs(df, args.postcode)
