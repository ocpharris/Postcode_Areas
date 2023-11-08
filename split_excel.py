import argparse
import pandas as pd
import requests
import zipfile
import io
import sys
import os
from datetime import datetime

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
