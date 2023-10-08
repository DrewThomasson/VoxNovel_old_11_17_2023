import pandas as pd
import nltk

# Ensure the necessary NLTK data is downloaded
nltk.download('averaged_perceptron_tagger')

def is_pronoun(word):
    """Checks if the given word is a pronoun using NLTK's POS tagging."""
    tag = nltk.pos_tag([word])[0][1]
    return tag in ["PRP", "PRP$", "WP", "WP$"]

# Load the quotes.csv file into a DataFrame
df = pd.read_csv("quotes.csv")

# Replace speaker names that match the format "{CharID}:{pronoun}" with "Narrator"
for index, row in df.iterrows():
    speaker = row['Speaker']
    if speaker:
        _, name = speaker.split(":")
        if is_pronoun(name):
            df.at[index, 'Speaker'] = "Narrator"

# Save the updated DataFrame back to quotes.csv
df.to_csv("quotes.csv", index=False)
