import pandas as pd

# Load the files
df_quotes = pd.read_csv("158_emma.quotes", delimiter="\t")
df_tokens = pd.read_csv("158_emma.tokens", delimiter="\t", error_bad_lines=False, quoting=3)

last_end_id = 0  # Initialize the last_end_id to 0
nonquotes_data = []  # List to hold data for nonquotes.csv

# Iterate through the quotes dataframe
for index, row in df_quotes.iterrows():
    start_id = row['quote_start']
    end_id = row['quote_end']
    
    # Get tokens between the end of the last quote and the start of the current quote
    filtered_tokens = df_tokens[(df_tokens['token_ID_within_document'] > last_end_id) & 
                                (df_tokens['token_ID_within_document'] < start_id)]
    
    # Build the word chunk
    words_chunk = ' '.join([token_row['word'] for index, token_row in filtered_tokens.iterrows()])
    
    # Append data to nonquotes_data if words_chunk is not empty
    if words_chunk:
        nonquotes_data.append([words_chunk, last_end_id, start_id, "False", "Narrator"])
    
    last_end_id = end_id  # Update the last_end_id to the end_id of the current quote

# Create a DataFrame for non-quote data
nonquotes_df = pd.DataFrame(nonquotes_data, columns=["Text", "Start Location", "End Location", "Is Quote", "Speaker"])

# Write to nonquotes.csv
nonquotes_df.to_csv("non_quotes.csv", index=False)

