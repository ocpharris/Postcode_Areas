import argparse
import pandas as pd
import requests
import zipfile
import io
import sys
import os
from datetime import datetime

class get_areas:

    # Function to split the CSV file into five alphabetically equal-sized groups
    def split_csv_by_postcode(self):
        # URL of the zip file to load
        zip_file_url = 'https://www.arcgis.com/sharing/rest/content/items/e7824b1475604212a2325cd373946235/data'

        try:
            # Send a GET request to the URL and download the zip file
            response = requests.get(zip_file_url)
            response.raise_for_status()  # Check for any errors in the response

            # Create a ZipFile object from the downloaded content
            with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zip_ref:
                # List the files within the zip file
                file_list = zip_ref.namelist()

                # Choose the spreadsheet you want to extract
                target_spreadsheet = 'PCD_OA_LSOA_MSOA_LAD_MAY22_UK_LU.csv'

                if target_spreadsheet in file_list:
                    # Extract the target spreadsheet
                    with zip_ref.open(target_spreadsheet) as spreadsheet_file:
                        # Read the CSV content and convert it to a DataFrame
                        df = pd.read_csv(spreadsheet_file, encoding='latin1')

                        # Define postcode groups as specified
                        postcode_groups = [
                            ('A-E', ['A', 'B', 'C', 'D', 'E']),
                            ('F-J', ['F', 'G', 'H', 'I', 'J']),
                            ('K-O', ['K', 'L', 'M', 'N', 'O']),
                            ('P-T', ['P', 'Q', 'R', 'S', 'T']),
                            ('U-Z', ['U', 'V', 'W', 'X', 'Y', 'Z'])
                        ]

                        # Create separate DataFrames for each group
                        for group_name, letters in postcode_groups:
                            filtered_df = df[df['pcd7'].str[0].str.upper().isin(letters)]

                            # Save the filtered DataFrame as a CSV file
                            output_file = f'{group_name}.csv'
                            filtered_df.to_csv(output_file, index=False)
                            print(f'Saved {group_name} data to {output_file}')

        except requests.exceptions.RequestException as e:
            print(f"Error downloading the zip file: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    # # Call the function to split the CSV file into postcode groups
    # split_csv_by_postcode()


    def select_postcode_csv(self,postcode):


            # Define the mapping of postcode ranges to CSV file names
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
    def postcode_to_OAs(self,df, postcode):
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





    # # Main script
    # if __name__ == "__main__":
    #     parser = argparse.ArgumentParser(description="Process postcode data.")
    #     parser.add_argument("--postcode", type=str, help="Postcode to process")
    #     args = parser.parse_args()


    #     if args.postcode:
    #         split_csv_by_postcode()
    #         df = select_postcode_csv(args.postcode)
    #         if df is not None:
    #             postcode_to_OAs(df, args.postcode)  # Pass the DataFrame and the postcode

    def main(self,postcode):
        self.split_csv_by_postcode()
        self.select_postcode_csv(postcode=postcode)
        df = self.select_postcode_csv(postcode=postcode)  # Get the DataFrame
        if df is not None:
            self.postcode_to_OAs(df, postcode=postcode)

        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process postcode data.")
    parser.add_argument("--postcode", type=str, help="Postcode to process")
    args = parser.parse_args()

    if args.postcode:
        postcode_area = get_areas()  # Create an instance of the class
        postcode_area.split_csv_by_postcode()
        df = postcode_area.select_postcode_csv(args.postcode)
        if df is not None:
            postcode_area.postcode_to_OAs(df, args.postcode)
