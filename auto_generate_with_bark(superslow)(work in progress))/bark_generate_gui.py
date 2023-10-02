import csv
import os
import nltk
import numpy as np
import random
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

nltk.download('punkt')

from bark.generation import (
    generate_text_semantic,
    preload_models,
)
from bark.api import semantic_to_waveform
from bark import generate_audio, SAMPLE_RATE
from IPython.display import Audio
from scipy.io.wavfile import write as write_wav

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
preload_models()

# Constants
GEN_TEMP = 0.6
silence = np.zeros(int(0.25 * SAMPLE_RATE))
voice_actors = [
    "v2/en_speaker_0", "v2/en_speaker_2", 
    "v2/en_speaker_3", "v2/en_speaker_4", "v2/en_speaker_5", 
    "v2/en_speaker_6", "v2/en_speaker_7", "v2/en_speaker_8", 
    "v2/en_speaker_9"
]

def generate_long_form_audio(text, speaker):
    sentences = nltk.sent_tokenize(text)
    pieces = []
    if len(text.split()) > 512:
        for sentence in sentences:
            semantic_tokens = generate_text_semantic(
                sentence,
                history_prompt=speaker,
                temp=GEN_TEMP,
                min_eos_p=0.05,
            )
            audio_array = semantic_to_waveform(semantic_tokens, history_prompt=speaker)
            pieces += [audio_array, silence.copy()]
    else:
        for sentence in sentences:
            audio_array = generate_audio(sentence, history_prompt=speaker)
            pieces += [audio_array, silence.copy()]
    return np.concatenate(pieces)

def get_unique_speakers():
    speakers = set()
    with open("book.csv", "r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            speaker_name = row[3]
            speakers.add(speaker_name)
    return list(speakers)

def select_voice_actor_for_speaker():
    speaker_name = speakers_listbox.get(speakers_listbox.curselection())
    voice_actor_window = tk.Toplevel(root)
    voice_actor_label = tk.Label(voice_actor_window, text="Select a voice actor")
    voice_actor_label.pack(pady=10)
    
    voice_actor_combobox = ttk.Combobox(voice_actor_window, values=voice_actors)
    voice_actor_combobox.pack(pady=10)
    
    def assign_voice_actor():
        selected_voice_actor = voice_actor_combobox.get()
        speakers_dict[speaker_name] = selected_voice_actor
        voice_actor_window.destroy()

    assign_button = tk.Button(voice_actor_window, text="Assign", command=assign_voice_actor)
    assign_button.pack(pady=10)

def generate_audio_files():
    with open("book.csv", "r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for idx, row in enumerate(csv_reader):
            text = row[0]
            speaker_name = row[3]
            if speaker_name not in speakers_dict:
                continue
            speaker = speakers_dict[speaker_name]
            print(f"Generating audio for the text: {text}")
            audio_data = generate_long_form_audio(text, speaker)
            
            file_name = f"audio_{idx}"
            write_wav(f"{file_name}.wav", SAMPLE_RATE, audio_data)
    messagebox.showinfo("Info", "Finished generating audio files!")

# GUI Initialization
root = tk.Tk()
root.title("Voice Actor Selector")

speakers_label = tk.Label(root, text="Speakers")
speakers_label.pack(pady=10)

speakers_dict = {}
speakers = get_unique_speakers()
speakers_listbox = tk.Listbox(root)
for speaker in speakers:
    speakers_listbox.insert(tk.END, speaker)
speakers_listbox.pack(pady=10)

select_voice_button = tk.Button(root, text="Select Voice Actor", command=select_voice_actor_for_speaker)
select_voice_button.pack(pady=10)

generate_audio_button = tk.Button(root, text="Generate Audio Files", command=generate_audio_files)
generate_audio_button.pack(pady=20)

root.mainloop()

