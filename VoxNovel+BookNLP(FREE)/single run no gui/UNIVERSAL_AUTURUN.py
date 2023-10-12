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
        words_chunk = words_chunk.replace(" n't", "n't").replace(" n’", "n’").replace("( ", "(").replace(" ,", ",").replace("gon na", "gonna")
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
import re
import glob
import os
import nltk

def process_files(quotes_file, entities_file):
    # Load the files
    df_quotes = pd.read_csv(quotes_file, delimiter="\t")
    df_entities = pd.read_csv(entities_file, delimiter="\t")

    character_info = {}

    def is_pronoun(word):
        tagged_word = nltk.pos_tag([word])
        return 'PRP' in tagged_word[0][1] or 'PRP$' in tagged_word[0][1]

    def get_gender(pronoun):
        male_pronouns = ['he', 'him', 'his']
        female_pronouns = ['she', 'her', 'hers']

        if pronoun in male_pronouns:
            return 'Male'
        elif pronoun in female_pronouns:
            return 'Female'
        return 'Unknown'

    # Process the quotes dataframe
    for index, row in df_quotes.iterrows():
        char_id = row['char_id']
        mention = row['mention_phrase']

        # Initialize character info if not already present
        if char_id not in character_info:
            character_info[char_id] = {"names": {}, "pronouns": {}, "quote_count": 0}

        # Update names or pronouns based on the mention_phrase
        if is_pronoun(mention):
            character_info[char_id]["pronouns"].setdefault(mention.lower(), 0)
            character_info[char_id]["pronouns"][mention.lower()] += 1
        else:
            character_info[char_id]["names"].setdefault(mention, 0)
            character_info[char_id]["names"][mention] += 1

        character_info[char_id]["quote_count"] += 1

    # Process the entities dataframe
    for index, row in df_entities.iterrows():
        coref = row['COREF']
        name = row['text']

        if coref in character_info:
            if is_pronoun(name):
                character_info[coref]["pronouns"].setdefault(name.lower(), 0)
                character_info[coref]["pronouns"][name.lower()] += 1
            else:
                character_info[coref]["names"].setdefault(name, 0)
                character_info[coref]["names"][name] += 1

    # Extract the most likely name and gender for each character
    for char_id, info in character_info.items():
        most_likely_name = max(info["names"].items(), key=lambda x: x[1])[0] if info["names"] else "Unknown"
        most_common_pronoun = max(info["pronouns"].items(), key=lambda x: x[1])[0] if info["pronouns"] else None

        gender = get_gender(most_common_pronoun) if most_common_pronoun else 'Unknown'
        gender_suffix = ".M" if gender == 'Male' else ".F" if gender == 'Female' else ".?"

        info["formatted_speaker"] = f"{char_id}:{most_likely_name}{gender_suffix}"
        info["most_likely_name"] = most_likely_name
        info["gender"] = gender

    # Write the formatted data to quotes.csv
    output_filename = os.path.join(os.path.dirname(quotes_file), "quotes.csv")
    with open(output_filename, 'w', newline='') as outfile:
        fieldnames = ["Text", "Start Location", "End Location", "Is Quote", "Speaker"]
        writer = pd.DataFrame(columns=fieldnames)

        for index, row in df_quotes.iterrows():
            char_id = row['char_id']

            if not re.search('[a-zA-Z0-9]', row['quote']):
                print(f"Removing row with text: {row['quote']}")
                continue

            if character_info[char_id]["quote_count"] == 1:
                formatted_speaker = "Narrator"
            else:
                formatted_speaker = character_info[char_id]["formatted_speaker"] if char_id in character_info else "Unknown"

            new_row = {"Text": row['quote'], "Start Location": row['quote_start'], "End Location": row['quote_end'], "Is Quote": "True", "Speaker": formatted_speaker}
            writer = writer.append(new_row, ignore_index=True)

        writer.to_csv(output_filename, index=False)
        print(f"Saved quotes.csv to {output_filename}")

def main():
    # Use glob to get all .quotes and .entities files within the "Working_files" directory and its subdirectories
    quotes_files = glob.glob('Working_files/**/*.quotes', recursive=True)
    entities_files = glob.glob('Working_files/**/*.entities', recursive=True)

    # Pair and process .quotes and .entities files with matching filenames (excluding the extension)
    for q_file in quotes_files:
        base_name = os.path.splitext(os.path.basename(q_file))[0]
        matching_entities_files = [e_file for e_file in entities_files if os.path.splitext(os.path.basename(e_file))[0] == base_name]

        if matching_entities_files:
            process_files(q_file, matching_entities_files[0])

    print("All processing complete!")

if __name__ == "__main__":
    main()






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
import numpy as np

# Read the CSV files
quotes_df = pd.read_csv("Working_files/Book/quotes.csv")
non_quotes_df = pd.read_csv("Working_files/Book/non_quotes.csv")

# Concatenate the dataframes
combined_df = pd.concat([quotes_df, non_quotes_df], ignore_index=True)

# Convert 'None' to NaN
combined_df.replace('None', np.nan, inplace=True)

# Drop rows with NaN in 'Start Location'
combined_df.dropna(subset=['Start Location'], inplace=True)

# Convert the 'Start Location' column to integers
combined_df["Start Location"] = combined_df["Start Location"].astype(int)

# Sort by 'Start Location'
sorted_df = combined_df.sort_values(by="Start Location")

# Save to 'book.csv'
sorted_df.to_csv("Working_files/Book/book.csv", index=False)








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
