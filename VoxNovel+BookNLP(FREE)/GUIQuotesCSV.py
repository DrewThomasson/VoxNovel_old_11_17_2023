import pandas as pd
import nltk
from collections import Counter
import re
import tkinter as tk
from tkinter import filedialog

# Ensure the necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('averaged_perceptron_tagger')

# Create the main window for GUI
root = tk.Tk()
root.withdraw()  # Hide the main window

# Ask the user to select files using file dialogs
quotes_file_path = filedialog.askopenfilename(title="Select the quotes file")
tokens_file_path = filedialog.askopenfilename(title="Select the tokens file")
entities_file_path = filedialog.askopenfilename(title="Select the entities file")

# Check if the user selected the files or pressed cancel
if not quotes_file_path or not tokens_file_path or not entities_file_path:
    print("File selection canceled. Exiting.")
    exit()

# Load the files
df_quotes = pd.read_csv(quotes_file_path, delimiter="\t")
df_tokens = pd.read_csv(tokens_file_path, delimiter="\t", on_bad_lines='skip', quoting=3)
df_entities = pd.read_csv(entities_file_path, delimiter="\t")

# Build a dictionary to hold character names by char_id
char_names_dict = {}
for index, row in df_entities.iterrows():
    char_id = row['COREF']
    name = row['text']
    if char_id not in char_names_dict:
        char_names_dict[char_id] = []
    char_names_dict[char_id].append(name)

# Function to identify names using NLTK's named entity recognition
def identify_names(text_list):
    text = ' '.join(text_list)
    tokenized = nltk.word_tokenize(text)
    named_entities = nltk.ne_chunk(nltk.pos_tag(tokenized))
    names = []
    for chunk in named_entities:
        if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
            name_tokens = [leaf[0] for leaf in chunk.leaves()]
            if name_tokens[0] in ["Mr.", "Mrs.", "Dr.", "Ms."]:
                prev_index = named_entities.index(chunk) - 1
                if prev_index >= 0 and isinstance(named_entities[prev_index], tuple):
                    name_tokens.insert(0, named_entities[prev_index][0])
            name = ' '.join(name_tokens)
            name_parts = name.split()
            if len(name_parts) > 1 and name_parts[0] == name_parts[1]:
                name = name_parts[0]
            names.append(name)
    return names

# Now, select the most common name for each char_id
for char_id, names in char_names_dict.items():
    names_identified = identify_names(names)
    if names_identified:
        char_names_dict[char_id] = Counter(names_identified).most_common(1)[0][0]
    else:
        char_names_dict[char_id] = Counter(names).most_common(1)[0][0]

quotes_data = []

# Iterate through the quotes dataframe
for index, row in df_quotes.iterrows():
    start_id = row['quote_start']
    end_id = row['quote_end']
    char_id = row['char_id']
    
    # Filter the tokens
    filtered_tokens = df_tokens[(df_tokens['token_ID_within_document'] >= start_id) & 
                                (df_tokens['token_ID_within_document'] <= end_id)]
    
    # Build the words chunk
    words_chunk = ' '.join([token_row['word'] for index, token_row in filtered_tokens.iterrows()])
    words_chunk = words_chunk.replace(" n't", "n't").replace(" n’", "n’")
    words_chunk = re.sub(r' (?=[^a-zA-Z0-9\s])', '', words_chunk)
    
    # Get character name from char_names_dict
    char_name = char_names_dict.get(char_id, "")
    speaker_info = f"{char_id}:{char_name}"
    
    # Append data to quotes_data
    quotes_data.append([words_chunk, start_id, end_id, "True", speaker_info])

# Create a DataFrame for quote data
quotes_df = pd.DataFrame(quotes_data, columns=["Text", "Start Location", "End Location", "Is Quote", "Speaker"])

# Write to quotes.csv
quotes_df.to_csv("quotes.csv", index=False)

