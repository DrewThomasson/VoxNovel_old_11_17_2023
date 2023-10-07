import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog

def process_files(quotes_file, tokens_file):
    # Load the files
    df_quotes = pd.read_csv(quotes_file, delimiter="\t")
    df_tokens = pd.read_csv(tokens_file, delimiter="\t", error_bad_lines=False, quoting=3)

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
        words_chunk = words_chunk.replace(" n't", "n't").replace(" n’", "n’")
        words_chunk = re.sub(r' (?=[^a-zA-Z0-9\s])', '', words_chunk)
        
        # Append data to nonquotes_data if words_chunk is not empty
        if words_chunk:
            nonquotes_data.append([words_chunk, last_end_id, start_id, "False", "Narrator"])
        
        last_end_id = end_id  # Update the last_end_id to the end_id of the current quote

    # Create a DataFrame for non-quote data
    nonquotes_df = pd.DataFrame(nonquotes_data, columns=["Text", "Start Location", "End Location", "Is Quote", "Speaker"])

    # Write to nonquotes.csv
    nonquotes_df.to_csv("non_quotes.csv", index=False)

# GUI setup
root = tk.Tk()
root.title("Harry Potter Book Processor")
root.geometry("400x200")

def open_and_process():
    quotes_file = filedialog.askopenfilename(title="Select the Quotes file")
    tokens_file = filedialog.askopenfilename(title="Select the Tokens file")
    
    if quotes_file and tokens_file:  # check if both files are selected
        process_files(quotes_file, tokens_file)
        label_result.config(text="Processing complete!")

btn_select = tk.Button(root, text="Select Files and Process", command=open_and_process)
btn_select.pack(pady=40)

label_result = tk.Label(root, text="")
label_result.pack()

root.mainloop()

