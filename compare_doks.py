import pandas as pd
import numpy as np

def compare_tables(table1, table2, output_file):
    # Read the tables from Excel files
    df1 = pd.read_excel(table1)
    df2 = pd.read_excel(table2)

    # Merge the tables based on the 'id' column
    merged_df = pd.merge(df1, df2, on='id', how='outer', suffixes=('_1', '_2'))

    # Filter out rows where the 'id' is not present in both files
    merged_df = merged_df.dropna(subset=['id'])

    # Create a new DataFrame to store the differences
    diff_df = pd.DataFrame()

    # Include 'name', 'keyforgeId', and 'id' columns from the first table
    diff_df['name'] = df1['name']
    diff_df['keyforgeId'] = df1['keyforgeId']
    diff_df['id'] = df1['id']

    # Iterate over each row
    for index, row in merged_df.iterrows():
        # Compare the values in each column except for 'id', 'name', and 'keyforgeId'
        for column in df1.columns:
            if column not in ['id', 'name', 'keyforgeId']:
                value1 = row[column + '_1']
                value2 = row[column + '_2']

                # Check if both values are not NaN and are numerical
                if pd.notnull(value1) and pd.notnull(value2) and np.issubdtype(type(value1), np.number) and np.issubdtype(type(value2), np.number):
                    # Check if the values are not equal
                    if value1 != value2:
                        # Calculate the numerical difference and add it to the new DataFrame
                        diff_df.at[index, column] = value2

    # Write the differences to an Excel file
    diff_df.to_excel(output_file, index=False)

# Specify the file names and the output file name
file1 = 'MyDecks_2023-07-17.xlsx'
file2 = 'MyDecks_2023-07-29.xlsx'
output_file = 'differences.xlsx'

# Call the function to compare the tables and generate the output
compare_tables(file1, file2, output_file)


