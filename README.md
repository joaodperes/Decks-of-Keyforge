# Decks of Keyforge
 Automate data extraction from DoKs using an API key.

![Decks of Keyforge logo](https://decksofkeyforge.com/static/media/dok.bb36eaf16060b5a5d7846b3af789d6a5.svg)

## config.py

Insert your API Key in the file and store in the same folder as the remaining files.

## doks.py

Gets your (owned on DoKs) deck data into an Excel file (named MyDecks_today's_date).
The file has a "Decks" sheet, with all deck characteristics such as id, name, E, A, C, etc; but also SAS, previous SAS, AERC and Power Level / Chains.
In the second sheet, named "Houses", you'll find individual card data structured as follows:

ID | House | Card | Rarity | Legacy | Maverick | Anomaly | Enhanced
---|---|---|---|---|---|---|---

**Note:** *ID refers to Deck ID, not keyforgeId*

## cards.py

Extracts all card data into an Excel file. Does not need to be run often, just after a new set is added to the MV.
It is also *not* required for doks.py, but can be used to get additional card information and card images, e.g.:

id | cardTitle | house | cardType | frontImage
---|---|---|---|---
0202aefb-83de-4a66-a206-f343cc902ab7 | 1-2 Punch | Brobnar | Action | ![1-2 Punch card art](https://mastervault-storage-prod.s3.amazonaws.com/media/card_front/en/435_001_CCC247PX4H2C_en.png)

## compare_doks.py

Allows you to compare two versions of MyDecks.xlsx and identify the differences between values. Does not require an API call, but the Excel files should be stored in the same folder as this file.
The output will be an Excel file with a similar structure, but the values that did not change will be represented by empty cells.

To specify which files you want to compare just edit the following:

~~~~ python
file1 = 'MyDecks_2023-07-17.xlsx'
file2 = 'MyDecks_2023-07-29.xlsx'
output_file = 'differences.xlsx'
~~~~
You can also change the output_file name if you so desire - perhaps even include today's date as with the other modules.
