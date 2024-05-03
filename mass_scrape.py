from generic_scraper_single_file import call_llm
import streamlit as st
import json 
import pandas as pd 
import os 
import csv
import time,random
import argparse
progress_text = "Operation in progress. Please wait."
my_bar = st.progress(0, text=progress_text)

def scrape(listings_file, directory,ApiKey):
    with open(listings_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        urls_and_branches = [(row[0], row[1]) for row in reader]  # Extract URL and branchId
    # urls_and_branches = [('www.google.com/mkanjwnjnhsanjws', 1,"Lease")]  # Extract URL and branchId
    if not os.path.exists(directory):
        os.makedirs(directory)
    print(len(urls_and_branches))
    for index, (url,type) in enumerate(urls_and_branches, start=1):
        print(index , "remaininig" , len(urls_and_branches) - index)
        my_bar.progress(index + 1, text=progress_text)
        scraped_data = call_llm(url.strip(),ApiKey)  # Assuming call_llm is defined elsewhere
        if scraped_data:
            # scraped_data["branchId"] = branchId
            scraped_data["recordType"] = type
        
        with open(os.path.join(directory, f"{index}.json"), "w") as json_file:
            json.dump(scraped_data, json_file)
        
        print(f"Scraped {url} and saved as {index}.json")

def json_to_csv(input_folder, output_file):
    json_files = [f for f in os.listdir(input_folder) if f.endswith('.json')]
    if not json_files:
        return

    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        header_written = False  # Flag to track if header is written

        for json_file in json_files:
            with open(os.path.join(input_folder, json_file), 'r') as f:
                data = json.load(f)

            if isinstance(data, list):
                if data:  # Check if the list is not empty
                    if not header_written:
                        header = list(data[0].keys())
                        writer.writerow(header)
                        header_written = True

                    for row in data:
                        writer.writerow(row.values())
            elif isinstance(data, dict):
                if not header_written:
                    header = list(data.keys())
                    writer.writerow(header)
                    header_written = True

                writer.writerow(data.values())
    print("converted JSONS to CSV")



listings_file = "Enter listings file in the format abc.csv"
directory = "Enter directory to store json files same name as csv" 
csv_file = "Enter csv file"

#eg
# listings_file = "/home/balaji/Desktop/QLD/Domain_specific/www.firstnationalcoastal.com.au.csv"
# directory = "QLD/JSONS/www.firstnationalcoastal.com.au.csv" 
# csv_file = "QLD_www.firstnationalcoastal.com.au.csv"
parser = argparse.ArgumentParser()
parser.add_argument('input_file_path', help='Input File Path')
parser.add_argument('output_file_name', help="Output File Path")
parser.add_argument('ApiKey', help="Output File Path")
args = parser.parse_args()
input_file = args.input_file_path
output_file = args.output_file_name
ApiKey = args.ApiKey
input_directory, input_filename = os.path.split(input_file)
output_directory = os.path.join(input_directory, f'output/{input_filename}')
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
output_file = os.path.join(output_directory, output_file)
input_file = input_file
scrape(input_file, output_directory,ApiKey)
json_to_csv(output_directory, output_file)