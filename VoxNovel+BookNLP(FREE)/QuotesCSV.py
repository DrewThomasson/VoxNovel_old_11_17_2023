import pandas as pd
import nltk
from collections import Counter

# Ensure the necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('averaged_perceptron_tagger')

# Load the files
df_quotes = pd.read_csv("158_emma.quotes", delimiter="\t")
df_tokens = pd.read_csv("158_emma.tokens", delimiter="\t", on_bad_lines='skip', quoting=3)
df_entities = pd.read_csv("158_emma.entities", delimiter="\t")

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
            if name_tokens[0] in ["Mr.", "Mrs.", "Dr.", "Ms."]:  # Adjust this list as necessary
                prev_index = named_entities.index(chunk) - 1
                if prev_index >= 0 and isinstance(named_entities[prev_index], tuple):
                    name_tokens.insert(0, named_entities[prev_index][0])
            name = ' '.join(name_tokens)
            # Avoid repeated names like "Emma Emma"
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

quotes_data = []  # List to hold data for quotes.csv

# Iterate through the quotes dataframe
for index, row in df_quotes.iterrows():
    start_id = row['quote_start']
    end_id = row['quote_end']
    char_id = row['char_id']  # Get char_id from df_quotes
    
    # Filter the tokens
    filtered_tokens = df_tokens[(df_tokens['token_ID_within_document'] > start_id) & 
                                (df_tokens['token_ID_within_document'] < end_id)]
    
    # Build the words chunk
    words_chunk = ' '.join([token_row['word'] for index, token_row in filtered_tokens.iterrows()])
    
    # Get character name from char_names_dict
    char_name = char_names_dict.get(char_id, "")
    speaker_info = f"{char_id}:{char_name}"
    
    # Append data to quotes_data
    quotes_data.append([words_chunk, start_id, end_id, "True", speaker_info])

# Create a DataFrame for quote data
quotes_df = pd.DataFrame(quotes_data, columns=["Text", "Start Location", "End Location", "Is Quote", "Speaker"])

# Write to quotes.csv
quotes_df.to_csv("quotes.csv", index=False)

