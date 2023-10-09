import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.simpledialog import askstring
import os
import pandas as pd
import random
import shutil  # for copying files
import subprocess  # to open the audio file with the default video player

import torch
import torchaudio
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio, load_voice, load_voices

import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.simpledialog import askstring
import os
import pandas as pd
import random
import shutil
import subprocess

# Your other imports remain here

data = pd.read_csv("book.csv")
voice_actors = os.listdir("voices/")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Selector")
        self.speaker_voice_map = {}

        # Outer Frame that holds everything
        outer_frame = ttk.Frame(root)
        outer_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollable Frame for Speakers
        self.canvas = tk.Canvas(outer_frame)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(outer_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        outer_frame.grid_rowconfigure(0, weight=1)
        outer_frame.grid_columnconfigure(0, weight=1)

        self.frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create widgets for speakers in the scrollable frame
        for idx, speaker in enumerate(data['Speaker'].unique()):
            tk.Label(self.frame, text=speaker).grid(row=idx, column=0)
            combo = ttk.Combobox(self.frame, values=voice_actors)
            random_voice = random.choice(voice_actors)
            combo.set(random_voice)
            combo.grid(row=idx, column=1)
            self.speaker_voice_map[speaker] = combo
            tk.Button(self.frame, text="Preview", command=lambda speaker=speaker: self.preview_voice(speaker)).grid(row=idx, column=2)

        # Non-scrollable frame for buttons and progress bar
        button_frame = ttk.Frame(outer_frame)
        button_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        tk.Button(button_frame, text="Add New Voice", command=self.add_new_voice).grid(row=0, column=0)
        tk.Button(button_frame, text="Generate Audio", command=self.generate_audio).grid(row=0, column=1)
        self.progress = ttk.Progressbar(button_frame, orient="horizontal", length=200, mode="determinate")
        self.progress.grid(row=1, column=0, columnspan=2)


    def add_new_voice(self):
        folder_name = askstring("New Voice", "Enter name for the new voice:")
        if folder_name:
            new_folder_path = os.path.join("voices/", folder_name)
            os.mkdir(new_folder_path)
            file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3"), ("WAV Files", "*.wav")])
            if file_path:
                shutil.copy(file_path, new_folder_path)
                global voice_actors
                voice_actors = os.listdir("voices/")
                for combo in self.speaker_voice_map.values():
                    combo['values'] = voice_actors

    def split_long_string(self, text, limit=250):
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

    def generate_audio(self):
        total_rows = len(data)
        tts = TextToSpeech()
        for index, row in data.iterrows():
            speaker = row['Speaker']
            text = row['Text']
            voice_actor = self.speaker_voice_map[speaker].get()
            sentences = sent_tokenize(text)
            
            audio_tensors = []
            for sentence in sentences:
                fragments = self.split_long_string(sentence)
                for fragment in fragments:
                    print(fragment)
                    voice_samples, conditioning_latents = load_voice(voice_actor)
                    gen = tts.tts_with_preset(fragment, voice_samples=voice_samples, conditioning_latents=conditioning_latents, preset="ultra_fast")
                    audio_tensors.append(gen.squeeze(0).cpu())
            
            combined_audio = torch.cat(audio_tensors, dim=1)
            torchaudio.save(f'audio_{index}.wav', combined_audio, 24000)
            progress_percentage = (index + 1) / total_rows * 100
            self.progress['value'] = progress_percentage
            self.root.update_idletasks()


    def preview_voice(self, speaker):
        voice_actor = self.speaker_voice_map[speaker].get()
        voice_folder = os.path.join("voices/", voice_actor)
        audio_samples = [f for f in os.listdir(voice_folder) if f.endswith(('.mp3', '.wav'))]
        if audio_samples:
            sample_path = os.path.join(voice_folder, audio_samples[0])
            subprocess.Popen(["xdg-open", sample_path])

root = tk.Tk()
app = App(root)
root.mainloop()

