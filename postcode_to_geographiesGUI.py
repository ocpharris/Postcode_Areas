import tkinter as tk
from tkinter import ttk

import argparse
import pandas as pd
import requests     
import numpy as np
import zipfile
import io
import sys
import os
from datetime import datetime
from postcode_to_areas_only import select_postcode_csv  
from postcode_to_areas_only import postcode_to_OAs








 


def scrape_data_button():
    postcode  = postcode_entry.get()
    


    try:
          # generate the Excel file
        df = select_postcode_csv(postcode)
        if df is not None:
            postcode_to_OAs(df,postcode)


        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Complete.")

                # Get the current date
        current_date = datetime.now()

        # Format the date as "dd_mm_yy"
        formatted_date = current_date.strftime("%d_%m_%y")

    
        # Define the output file path
        output_csv_file = f"MSOA_LSOA_{postcode}_{formatted_date}.csv"

        # Open the output file using the default program
        os.startfile(output_csv_file)
    except Exception as e:
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Error: {str(e)}")
    result_text.config(state=tk.DISABLED)




def set_navy_blue_and_white_style():
    style.configure("TLabel", background="navy", foreground="white")
    style.configure("TButton", background="navy", foreground="white")
    style.configure("TEntry", background="white", foreground="navy")

app = tk.Tk()
app.title("Get geographies data")

style = ttk.Style()


# Set the initial style to navy blue and white
set_navy_blue_and_white_style()


# Configure the main window background
app.configure(bg="navy")

# Add a field for entering the postcode
postcode_label = ttk.Label(app, text="Enter Postcode:")
postcode_label.pack()
example_label = postcode_label = ttk.Label(app, text="e.g. AB1 0AA (for 6 characters) or SW1P3XA (for 7 characters)")
example_label.pack()
postcode_entry = ttk.Entry(app)
postcode_entry.pack()

# # Create input fields and labels
# url_label = tk.Label(app, text="Enter postcode (no spaces eg sw1v2le):")
# url_label.pack()
# url_entry = tk.Entry(app)
# url_entry.pack()

# Create a button to trigger scraping
scrape_button = ttk.Button(app, text="Go", command=scrape_data_button)
scrape_button.pack()

# Create a text widget to display results
result_text = tk.Text(app, wrap=tk.WORD, height=10, width=40)
result_text.pack()
result_text.config(state=tk.DISABLED)  # Set text widget to read-only

app.mainloop()
