import requests
import json
import pandas as pd
import datetime
import time
import config

# Set up the API endpoints and headers
my_decks_url = "https://decksofkeyforge.com/public-api/v1/my-decks"
deck_info_url = "https://decksofkeyforge.com/public-api/v3/decks/"
stats_url = "https://decksofkeyforge.com/public-api/v1/stats"
api_key = config.API_KEY
headers = {"Api-Key": api_key}

# Define a function to split the 'houseAndCards' column into separate dataframes
def split_house_and_cards(df):
    new_df = pd.DataFrame(columns=['ID', 'House', 'Card', 'Rarity', 'Legacy', 'Maverick', 'Anomaly', 'Enhanced'])
    for index, row in df.iterrows():
        deck_id = row['id']
        house_cards = row['housesAndCards']
        for hc in house_cards:
            house = hc['house']
            cards = hc.get('cards', [])  # Use .get() to handle missing or different key names
            for card in cards:
                card_title = card.get('cardTitle', '')
                rarity = card.get('rarity', '')
                legacy = card.get('legacy', False)
                maverick = card.get('maverick', False)
                anomaly = card.get('anomaly', False)
                enhanced = card.get('enhanced', False) # Use .get() to handle missing or different key names
                new_row = {
                    'ID': deck_id,
                    'House': house,
                    'Card': card_title,
                    'Rarity': rarity,
                    'Legacy': bool(legacy),
                    'Maverick': bool(maverick),
                    'Anomaly': bool(anomaly),
                    'Enhanced': bool(enhanced)
                }

                new_df = pd.concat([new_df, pd.DataFrame(new_row, index=[0])], ignore_index=True)
    return new_df


# Get a list of all decks owned or added to favorites, funny, or notes
try:
    my_decks_response = requests.get(my_decks_url, headers=headers)
    my_decks_response.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(f"Error occurred while fetching my decks: {err}")
    exit()

my_decks_data = json.loads(my_decks_response.content)

# Extract the deck IDs from the response
deck_ids = [deck['deck']['keyforgeId'] for deck in my_decks_data]

# Create a dictionary to store the deck information
deck_dict = {}

# Loop through each deck ID and request the deck information
for deck_id in deck_ids:
    try:
        deck_info_response = requests.get(deck_info_url + str(deck_id), headers=headers)
        deck_info_response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"Error occurred while fetching deck {deck_id}: {err}")
        continue
    
    deck_info_data = json.loads(deck_info_response.content)
    
    # Extract the deck information and add it to the dictionary
    deck_info_dict = deck_info_data.get('deck')
    if not deck_info_dict:
        print(f"Error: no deck information returned for deck {deck_id}")
        continue
        
    deck_dict[deck_id] = deck_info_dict
    
    # Pause for 2.5 seconds before making the next API call
    time.sleep(2.5)

# Convert the dictionary to a pandas DataFrame
deck_df = pd.DataFrame.from_dict(deck_dict, orient='index')

# Split the 'houseAndCards' column into separate dataframes
house_df = split_house_and_cards(deck_df)


# Write the dataframes to Excel files
if deck_df.empty:
    print("No deck information available, exiting...")
    exit()

today = datetime.datetime.today().strftime("%Y-%m-%d")
filename = f"MyDecks_{today}.xlsx"

with pd.ExcelWriter(filename) as writer:
    # Write deck_df to sheet 1
    deck_df.to_excel(writer, sheet_name="Decks", index=False)
    
    # Write house_df to sheet 2
    house_df.to_excel(writer, sheet_name="Houses", index=False)

print(f"Successfully saved deck information to {filename}")
