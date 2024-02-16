"""
- loops through folder of CSV files
    for each CSV file:
    - Use pandas to read
    - iterate through the urls (in order)
        for each URL:
        - extract story content
        - use GPT-4 to check if it is supportive consumption or control
        - add this result to an array the length of the csv
    - add this array as a column to the end of the csv file
"""

import csv
import pandas as pd
import openai
import requests
import json
from bs4 import BeautifulSoup
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

directory = "C:\\Users\\Shantanu\\Downloads\\Kickstarter_2023-10-12T03_20_02_365Z"

for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path)
        arr = [] * len(filename)
        i = 0
        for item in df['urls']:
            json_data = json.loads(item)
            first_link = json_data['web']['project']
            page = requests.get(first_link)
            soup = BeautifulSoup(page.content, "html.parser")
            feature = soup.find('div', class_='story-content')

            completion = openai.completions.create(
                model="gpt-3.5-turbo",
                prompt=
                "Tell me if this fundraising story is supportive consumption" 
                "or a control (return either the phrase supportive consumption or the "
                "word control. Supportive consumption involves buying a product from a"
                "business to support them. Here is the prompt:" + feature,
                max_tokens=2
            )
            if completion == 'supportive control':
                arr[i] = completion

        df.insert(loc=41, column='category', value=arr)