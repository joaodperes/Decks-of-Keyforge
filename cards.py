import requests
import json
import pandas as pd
import config

# Set your API key
api_key = config.API_KEY

# Set the URL for the API call
url = "https://decksofkeyforge.com/public-api/v1/cards"

# Set the headers for the API call
headers = {
    "Api-Key": api_key,
    "Content-Type": "application/json"
}

# Make the API call and convert the response to JSON
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'
json_data = response.json()

# Convert the JSON data to a Pandas DataFrame
cards_df = pd.json_normalize(json_data)

# Remove non-ASCII characters from all columns
cards_df = cards_df.replace({r'[^\x00-\x7F]+':''}, regex=True)

# Output the DataFrame to a JSON file
cards_df.to_json("cards.json", orient="records", indent=2)