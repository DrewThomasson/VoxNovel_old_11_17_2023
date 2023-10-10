import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from epub2txt import epub2txt
from booknlp.booknlp import BookNLP

def calibre_installed():
    """Check if Calibre's ebook-convert tool is available."""
    try:
        subprocess.run(['ebook-convert', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        print("""ERROR NO CALIBRE: running epub2txt convert version...
It appears you dont have the calibre commandline tools installed on your,
This will allow you to convert from any ebook file format:
Calibre supports the following input formats: CBZ, CBR, CBC, CHM, EPUB, FB2, HTML, LIT, LRF, MOBI, ODT, PDF, PRC, PDB, PML, RB, RTF, SNB, TCR, TXT.

If you want this feature please follow online instruction for downloading the calibre commandline tool.

For Linux its: 
sudo apt update && sudo apt upgrade
sudo apt install calibre

""")
        return False

def convert_with_calibre(file_path, output_format="txt"):
    """Convert a file using Calibre's ebook-convert tool."""
    output_path = file_path.rsplit('.', 1)[0] + '.' + output_format
    subprocess.run(['ebook-convert', file_path, output_path])
    return output_path

def process_file():
    file_path = filedialog.askopenfilename(
        title='Select File',
        filetypes=[('Supported Files', 
                    ('*.cbz', '*.cbr', '*.cbc', '*.chm', '*.epub', '*.fb2', '*.html', '*.lit', '*.lrf', 
                     '*.mobi', '*.odt', '*.pdf', '*.prc', '*.pdb', '*.pml', '*.rb', '*.rtf', '*.snb', 
                     '*.tcr', '*.txt'))]
    )
    
    if not file_path:
        return

    if file_path.lower().endswith(('.cbz', '.cbr', '.cbc', '.chm', '.epub', '.fb2', '.html', '.lit', '.lrf', 
                                  '.mobi', '.odt', '.pdf', '.prc', '.pdb', '.pml', '.rb', '.rtf', '.snb', '.tcr')) and calibre_installed():
        file_path = convert_with_calibre(file_path)
    elif file_path.lower().endswith('.epub') and not calibre_installed():
        content = epub2txt(file_path)
        if not os.path.exists('Working_files'):
            os.makedirs('Working_files')
        file_path = os.path.join('Working_files', 'Book.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    elif not file_path.lower().endswith('.txt'):
        messagebox.showerror("Error", "Selected file format is not supported or Calibre is not installed.")
        return

    # Now process the TXT file with BookNLP
    book_id = "Book"
    output_directory = os.path.join('Working_files', book_id)

    model_params = {
        "pipeline": "entity,quote,supersense,event,coref",
        "model": "big"
    }

    booknlp = BookNLP("en", model_params)
    booknlp.process(file_path, output_directory, book_id)

    print("Success, File processed successfully!")
    
    # Close the GUI
    root.destroy()

root = tk.Tk()
root.title("BookNLP Processor")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

process_button = tk.Button(frame, text="Process File", command=process_file)
process_button.pack()

root.mainloop()









import pandas as pd
import re
import glob
import os

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
    output_filename = os.path.join(os.path.dirname(quotes_file), "non_quotes.csv")
    nonquotes_df.to_csv(output_filename, index=False)
    print(f"Saved nonquotes.csv to {output_filename}")

def main():
    # Use glob to get all .quotes and .tokens files within the "Working_files" directory and its subdirectories
    quotes_files = glob.glob('Working_files/**/*.quotes', recursive=True)
    tokens_files = glob.glob('Working_files/**/*.tokens', recursive=True)

    # Pair and process .quotes and .tokens files with matching filenames (excluding the extension)
    for q_file in quotes_files:
        base_name = os.path.splitext(os.path.basename(q_file))[0]
        matching_token_files = [t_file for t_file in tokens_files if os.path.splitext(os.path.basename(t_file))[0] == base_name]

        if matching_token_files:
            process_files(q_file, matching_token_files[0])

    print("All processing complete!")

if __name__ == "__main__":
    main()









import pandas as pd
import nltk
from collections import Counter
import re
import os
import glob

# Ensure the necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('averaged_perceptron_tagger')

# Search for files in the "Working_files" directory and sub-directories
quotes_files = glob.glob("Working_files/**/*quotes", recursive=True)
tokens_files = glob.glob("Working_files/**/*tokens", recursive=True)
entities_files = glob.glob("Working_files/**/*entities", recursive=True)

# Load the files (Assuming only one file each type for simplicity)
df_quotes = pd.read_csv(quotes_files[0], delimiter="\t")
df_tokens = pd.read_csv(tokens_files[0], delimiter="\t", on_bad_lines='skip', quoting=3)
df_entities = pd.read_csv(entities_files[0], delimiter="\t")

# Build a dictionary to hold character names by char_id
char_names_dict = {}
for index, row in df_entities.iterrows():
    char_id = row['COREF']
    name = row['text']
    if char_id not in char_names_dict:
        char_names_dict[char_id] = []
    char_names_dict[char_id].append(name)

def identify_gender(names_list):
    male_pronouns = ['he', 'him', 'his', 'himself']
    female_pronouns = ['she', 'her', 'hers', 'herself']
    
    male_count = sum(1 for name in names_list if name.lower() in male_pronouns)
    female_count = sum(1 for name in names_list if name.lower() in female_pronouns)
    
    if male_count > female_count:
        return ".M"
    elif female_count > male_count:
        return ".F"
    else:
        return ".?"

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

gender_dict = {}
for char_id, names in char_names_dict.items():
    names_identified = identify_names(names)
    gender_identified = identify_gender(names)
    if names_identified:
        char_names_dict[char_id] = Counter(names_identified).most_common(1)[0][0]
    else:
        char_names_dict[char_id] = Counter(names).most_common(1)[0][0]
    gender_dict[char_id] = gender_identified

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
    
    # Get character name and gender from char_names_dict and gender_dict
    char_name = char_names_dict.get(char_id, "")
    gender_suffix = gender_dict.get(char_id, ".?")
    speaker_info = f"{char_id}:{char_name}{gender_suffix}"
    
    # Append data to quotes_data
    quotes_data.append([words_chunk, start_id, end_id, "True", speaker_info])

# Create a DataFrame for quote data
quotes_df = pd.DataFrame(quotes_data, columns=["Text", "Start Location", "End Location", "Is Quote", "Speaker"])

# Write to quotes.csv
quotes_df.to_csv("Working_files/Book/quotes.csv", index=False)

# Print a completion message
print("quotes.csv file has been created!")






















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











import csv
import os

def process_csv(quotes_file_path, non_quotes_file_path):
    # Step 1: Read the contents of quotes.csv and non_quotes.csv into two lists.
    quotes = []
    with open(quotes_file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # skip the header
        for row in csvreader:
            text = row[0]
            start_location = int(row[1])
            end_location = int(row[2])
            speaker = row[4]  # Assuming "Speaker" is in the 4th column
            quotes.append((text, start_location, end_location, speaker, 'True'))

    results = []
    with open(non_quotes_file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # skip the header
        for row in csvreader:
            text = row[0]
            start_location = int(row[1])
            end_location = int(row[2])
            speaker = row[4]  # Assuming "Speaker" is in the 4th column
            results.append((text, start_location, end_location, speaker, 'False'))

    # Step 2: Merge and sort the two lists by start location.
    combined = quotes + results
    combined.sort(key=lambda x: x[1])  # sort based on start location

    # Step 3: Write the sorted list to book.csv.
    with open('Working_files/Book/book.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Text', 'Start Location', 'End Location', 'Speaker', 'Is Quote'])
        for row in combined:
            csvwriter.writerow(row)

    print("Processing complete! book.csv has been created.")


def find_files(directory, filename):
    matches = []

    # Walk through directory
    for root, dirnames, filenames in os.walk(directory):
        for fname in filenames:
            if fname == filename:
                matches.append(os.path.join(root, fname))

    return matches


if __name__ == "__main__":
    quotes_file_path = find_files("Working_files", "quotes.csv")
    non_quotes_file_path = find_files("Working_files", "non_quotes.csv")

    if quotes_file_path and non_quotes_file_path:
        process_csv(quotes_file_path[0], non_quotes_file_path[0])
    else:
        print("Error: Required CSV files not found in the specified directory!")







#this will wipe the computer of any current audio clips from a previous session
import os

def wipe_folder(directory_path):
    # Ensure the directory exists
    if not os.path.exists(directory_path):
        print(f"The directory {directory_path} does not exist!")
        return

    # Iterate through files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        # Check if it's a regular file (not a subdirectory)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

print("wiping any fast generated audio clips cache")
folder_path = "Working_files/generated_audio_clips/"
wipe_folder(folder_path)








import os
import pandas as pd
import random
import shutil  # for copying files

import torch
import torchaudio
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio, load_voice, load_voices

import time

import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')

data = pd.read_csv("Working_files/Book/book.csv")
voice_actors = [va for va in os.listdir("tortoise/voices/") if va != "cond_latent_example"]
male_voice_actors = [va for va in voice_actors if va.endswith(".M")]
female_voice_actors = [va for va in voice_actors if va.endswith(".F")]

def get_random_voice_for_speaker(speaker):
    selected_voice_actors = voice_actors  # default to all voice actors

    if speaker.endswith(".M") and male_voice_actors:    
        selected_voice_actors = male_voice_actors
    elif speaker.endswith(".F") and female_voice_actors:
        selected_voice_actors = female_voice_actors

    if not selected_voice_actors:  # If list is empty, default to all voice actors
        selected_voice_actors = voice_actors
        
    return random.choice(selected_voice_actors)

def ensure_output_folder():
    if not os.path.exists("Working_files/generated_audio_clips"):
        os.mkdir("Working_files/generated_audio_clips")

def split_long_string(text, limit=250):
    if len(text) <= limit:
        return [text]
    
    # Split by commas
    parts = text.split(',')
    new_parts = []
    
    for part in parts:
        while len(part) > limit:
            # Split at the last space before the limit
            break_point = part.rfind(' ', 0, limit)
            if break_point == -1:  # If no space found, split at the limit
                break_point = limit
            new_parts.append(part[:break_point].strip())
            part = part[break_point:].strip()
        new_parts.append(part)
    
    return new_parts

def generate_audio():
    random.seed(int(time.time()))
    ensure_output_folder()
    total_rows = len(data)
    tts = TextToSpeech()

    speaker_voice_map = {}
    print(speaker_voice_map)
    for speaker in data['Speaker'].unique():
        random_voice = get_random_voice_for_speaker(speaker)
        speaker_voice_map[speaker] = random_voice

    # Print the selected voices for each speaker
    for speaker, voice in speaker_voice_map.items():
        print(f"Selected voice for {speaker}: {voice}")

    for index, row in data.iterrows():
        speaker = row['Speaker']
        text = row['Text']
        voice_actor = speaker_voice_map[speaker]
        sentences = sent_tokenize(text)
        
        audio_tensors = []
        for sentence in sentences:
            fragments = split_long_string(sentence)
            for fragment in fragments:
                print(fragment)
                voice_samples, conditioning_latents = load_voice(voice_actor)
                gen = tts.tts_with_preset(fragment, voice_samples=voice_samples, conditioning_latents=conditioning_latents, preset="ultra_fast")
                audio_tensors.append(gen.squeeze(0).cpu())
        
        combined_audio = torch.cat(audio_tensors, dim=1)
        torchaudio.save(os.path.join("Working_files/generated_audio_clips", f'audio_{index}.wav'), combined_audio, 24000)

generate_audio()









import os
import pandas as pd
import torch
import torchaudio
import pygame

# Global Variables & Initializations
colors = ['#FFB6C1', '#ADD8E6', '#FFDAB9', '#98FB98', '#D8BFD8']
speaker_colors = {}
currently_playing = None
pygame.mixer.init()
INPUT_FOLDER = "Working_files/generated_audio_clips"
OUTPUT_FOLDER = "Final_combined_output_audio"
SILENCE_DURATION_MS = 780

def combine_audio_files(silence_duration_ms):
    folder_path = os.path.join(os.getcwd(), INPUT_FOLDER)
    files = sorted([f for f in os.listdir(folder_path) if f.startswith("audio_") and f.endswith(".wav")], 
                   key=lambda f: int(f.split('_')[1].split('.')[0]))
    combined_tensor = torch.Tensor()
    for index, file in enumerate(files):
        waveform, sample_rate = torchaudio.load(os.path.join(folder_path, file))
        channels = waveform.shape[0]
        silence_tensor = torch.zeros(channels, int(silence_duration_ms * sample_rate / 1000))
        combined_tensor = torch.cat([combined_tensor, waveform, silence_tensor], dim=1)
        print(f"Processing {index + 1}/{len(files)}: {file}")

    if not os.path.exists(os.path.join(os.getcwd(), OUTPUT_FOLDER)):
        os.makedirs(os.path.join(os.getcwd(), OUTPUT_FOLDER))

    output_path = os.path.join(os.getcwd(), OUTPUT_FOLDER, "combined_audio.wav")
    torchaudio.save(output_path, combined_tensor, sample_rate)

    print("Combining audio files complete!")

if __name__ == "__main__":
    combine_audio_files(SILENCE_DURATION_MS)









from moviepy.editor import *

def convert_wav_to_mp4(wav_filename, mp4_filename):
    audio = AudioFileClip(wav_filename)
    audio.write_audiofile(mp4_filename, codec='aac')

if __name__ == "__main__":
    wav_filename = "Final_combined_output_audio/combined_audio.wav"
    mp4_filename = "Final_combined_output_audio/combined_audio.mp4"

    convert_wav_to_mp4(wav_filename, mp4_filename)
    print(f"{wav_filename} has been converted to {mp4_filename}.")
