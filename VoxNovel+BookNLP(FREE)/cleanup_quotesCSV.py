import pandas as pd
import nltk
import re

# Ensure the necessary NLTK data is downloaded
nltk.download('averaged_perceptron_tagger')

def is_pronoun(word):
    """Checks if the given word is a pronoun using NLTK's POS tagging."""
    tag = nltk.pos_tag([word])[0][1]
    return tag in ["PRP", "PRP$", "WP", "WP$"]

def has_alphanumeric(text):
    """Checks if the given text contains any alphanumeric characters."""
    return bool(re.search(r'\w', text))

# Load the quotes.csv file into a DataFrame
df = pd.read_csv("quotes.csv")

# Remove rows where the "Text" column doesn't contain any alphanumeric characters
df = df[df["Text"].apply(has_alphanumeric)]

# Replace speaker names that match the format "{CharID}:{char_name}.{gender_suffix}" where char_name is a pronoun, with "Narrator"
for index, row in df.iterrows():
    speaker = row['Speaker']
    if speaker and ":" in speaker:
        parts = speaker.split(":")
        char_id = parts[0]
        char_name_gender = parts[1]
        
        # Extract char_name from "char_name.gender_suffix" format
        char_name = char_name_gender.split(".")[0]
        
        if is_pronoun(char_name):
            df.at[index, 'Speaker'] = "Narrator"

# Save the updated DataFrame back to quotes.csv
df.to_csv("quotes.csv", index=False)
