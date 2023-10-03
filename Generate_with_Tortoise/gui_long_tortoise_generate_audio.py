import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.simpledialog import askstring
import os
import pandas as pd
import random
import shutil  # for copying files
import subprocess  # to open the audio file with the default video player
import nltk
import torch
import torchaudio
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio, load_voice, load_voices

# Load CSV data
data = pd.read_csv("book.csv")

# Get list of available voice actors
voice_actors = os.listdir("tortoise/voices/")

# Downloading necessary NLTK data
nltk.download('punkt')

# Main app
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Selector")
        self.speaker_voice_map = {}

        # Dropdown for each speaker in CSV
        for idx, speaker in enumerate(data['Speaker'].unique()):
            tk.Label(root, text=speaker).grid(row=idx, column=0)
            combo = ttk.Combobox(root, values=voice_actors)
            
            # Set random voice
            random_voice = random.choice(voice_actors)
            combo.set(random_voice) 
            
            combo.grid(row=idx, column=1)
            self.speaker_voice_map[speaker] = combo

            # Add a preview button for each character
            tk.Button(root, text="Preview", command=lambda speaker=speaker: self.preview_voice(speaker)).grid(row=idx, column=2)

        # Buttons to add new voice and generate audio
        tk.Button(root, text="Add New Voice", command=self.add_new_voice).grid(row=idx+1, column=0)
        tk.Button(root, text="Generate Audio", command=self.generate_audio).grid(row=idx+1, column=1)

        # Progress bar setup
        self.progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
        self.progress.grid(row=idx+2, column=0, columnspan=3)

    def add_new_voice(self):
        folder_name = askstring("New Voice", "Enter name for the new voice:")
        if folder_name:
            new_folder_path = os.path.join("tortoise/voices/", folder_name)
            os.mkdir(new_folder_path)
            file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3"), ("WAV Files", "*.wav")])

            if file_path:
                shutil.copy(file_path, new_folder_path)
                
                # Refresh the voice_actors list
                global voice_actors
                voice_actors = os.listdir("tortoise/voices/")
                
                # Update the dropdowns
                for combo in self.speaker_voice_map.values():
                    combo['values'] = voice_actors

    def split_text(self, text):
        """Split the text into smaller chunks based on sentences."""
        return nltk.sent_tokenize(text)
    
    def generate_audio(self):
        total_rows = len(data)
        tts = TextToSpeech()
        
        for index, row in data.iterrows():
            speaker = row['Speaker']
            text = row['Text']
            voice_actor = self.speaker_voice_map[speaker].get()
            
            voice_samples, conditioning_latents = load_voice(voice_actor)
            
            sentences = self.split_text(text)
            audio_pieces = []
            for sentence in sentences:
                gen = tts.tts_with_preset(sentence, voice_samples=voice_samples, conditioning_latents=conditioning_latents, preset="ultra_fast")
                audio_pieces.append(gen.squeeze(0).cpu())
                
            concatenated_audio = torch.cat(audio_pieces, dim=0)
            torchaudio.save(f'audio_{index}.wav', concatenated_audio, 24000)
            
            progress_percentage = (index + 1) / total_rows * 100
            self.progress['value'] = progress_percentage
            self.root.update_idletasks()

    def preview_voice(self, speaker):
        voice_actor = self.speaker_voice_map[speaker].get()
        voice_folder = os.path.join("tortoise/voices/", voice_actor)
        audio_samples = [f for f in os.listdir(voice_folder) if f.endswith(('.mp3', '.wav'))]
        
        if audio_samples:
            sample_path = os.path.join(voice_folder, audio_samples[0])
            subprocess.Popen(["xdg-open", sample_path])

root = tk.Tk()
app = App(root)
root.mainloop()

