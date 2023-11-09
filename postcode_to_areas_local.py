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
        # uncomment when running script locally 
        postcode_mapping = {
            'A': 'A-E.csv',
            'B': 'A-E.csv',
            'C': 'A-E.csv',
            'D': 'A-E.csv',
            'E': 'A-E.csv',
            'F': 'F-J.csv',
            'G': 'F-J.csv',
            'H': 'F-J.csv',
            'I': 'F-J.csv',
            'J': 'F-J.csv',
            'K': 'K-O.csv',
            'L': 'K-O.csv',
            'M': 'K-O.csv',
            'N': 'K-O.csv',
            'O': 'K-O.csv',
            'P': 'P-T.csv',
            'Q': 'P-T.csv',
            'R': 'P-T.csv',
            'S': 'P-T.csv',
            'T': 'P-T.csv',
            'U': 'U-Z.csv',
            'V': 'U-Z.csv',
            'W': 'U-Z.csv',
            'X': 'U-Z.csv',
            'Y': 'U-Z.csv',
            'Z': 'U-Z.csv',
        }



        # Check if the input postcode is valid
        if len(postcode) < 1 or not postcode[0].isalpha():
            return None  # Invalid postcode

        # Get the relevant CSV file based on the first letter of the postcode
        csv_file = postcode_mapping.get(postcode[0].upper())
        # path = os.path.abspath(fr"C:\Users\oharris\Repos\Postcode_Areas\postcode_data")
        # # path = os.path.abspath(os.path.join(os.path.dirname("__file__"), '..', 'postcode_data'))
        # path = os.path.abspath(fr"C:\Users\oharris\Repos\Postcode_Areas\postcode_data")
        # print(path)
        # sys.path.append(path)
        
        if csv_file:
            # Read the CSV file into a DataFrame
            try:
                csv_path = fr"C:\Users\oharris\Repos\Postcode_Areas\postcode_data\{csv_file}"
                df = pd.read_csv(csv_path)
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
