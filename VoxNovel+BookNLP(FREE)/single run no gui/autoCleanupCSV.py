import pandas as pd
import nltk
import re
import os
import glob
import csv

# Ensure the necessary NLTK data is downloaded
nltk.download('averaged_perceptron_tagger')

def is_pronoun(word):
    """Checks if the given word is a pronoun using NLTK's POS tagging."""
    tag = nltk.pos_tag([word])[0][1]
    return tag in ["PRP", "PRP$", "WP", "WP$"]

def has_alphanumeric(text):
    """Checks if the given text contains any alphanumeric characters."""
    return bool(re.search(r'\w', text))

def find_file(filename, directory):
    """Searches for the file in the given directory and its subdirectories."""
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

# Search for the file in the "Working_files" directory and its subfolders
filepath = find_file("quotes.csv", "Working_files")

if filepath is None:
    print("Error: 'quotes.csv' not found in 'Working_files' or its subdirectories!")
    exit()

# Load the quotes.csv file into a DataFrame using the found path
df = pd.read_csv(filepath)

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

# Save the updated DataFrame back to the same filepath
df.to_csv(filepath, index=False)

# Step 1: Read the file and load the contents using the found path
with open(filepath, 'r') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)
    
    # Ensure "Speaker" column exists
    if "Speaker" not in headers:
        print("Error: 'Speaker' column not found!")
        exit()

    # Load all rows
    rows = [row for row in reader]

# Step 2: Count occurrences of each name
name_counts = {}
for row in rows:
    speaker_index = headers.index("Speaker")
    name = row[speaker_index]
    name_counts[name] = name_counts.get(name, 0) + 1

# Step 3 and 4: Replace names with "Narrator" if they appear only once and print message
for row in rows:
    speaker_index = headers.index("Speaker")
    name = row[speaker_index]
    if name_counts[name] == 1:
        print(f"{name}: was found with 1 quote: Turning into Narrator line")
        row[speaker_index] = "Narrator"
        name_counts["Narrator"] = name_counts.get("Narrator", 0) + 1
        del name_counts[name]

# Optional: Write changes back to the CSV file using the found path
with open(filepath, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)

# Sort the counts from most to least
sorted_counts = sorted(name_counts.items(), key=lambda x: x[1], reverse=True)

# Print the updated counts
print("\nCharacter Quote Counts after Changes:")
for name, count in sorted_counts:
    print(f"{name}: {count} times")

