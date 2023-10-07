import csv
import wave
import random
import os
import subprocess
import pandas as pds
import pygame
import tkinter as tk
from tkinter import scrolledtext, ttk, filedialog
import threading
from balacoon_tts import TTS
from huggingface_hub import hf_hub_download

# Constants & Initializations
colors = ['#FFB6C1', '#ADD8E6', '#FFDAB9', '#98FB98', '#D8BFD8']
speaker_colors = {}
currently_playing = None
MODEL_NAMES = {
    "CMU Artic": "en_us_cmuartic_jets_cpu.addon",
    "Hi-Fi": "en_us_hifi_jets_cpu.addon"
}

pygame.mixer.init()

# Functions from book_display_gui.py
def display_content():
    df = pds.read_csv('book.csv')
    text_display.delete('1.0', tk.END)
    start_idx = '1.0'

    for idx, row in df.iterrows():
        speaker = row['Speaker']
        text = f"{row['Text']}\n\n"
        text_display.insert(tk.END, text)

        if speaker not in speaker_colors:
            speaker_colors[speaker] = colors[len(speaker_colors) % len(colors)]

        end_idx = text_display.index(f"{start_idx} + {len(text)} chars")
        text_display.tag_add(str(idx), start_idx, end_idx)
        text_display.tag_configure(str(idx), background=speaker_colors[speaker])
        text_display.tag_bind(str(idx), "<Enter>", lambda e, s=speaker: show_speaker(e, s))
        text_display.tag_bind(str(idx), "<Leave>", hide_speaker)
        text_display.tag_bind(str(idx), "<Button-1>", lambda e, i=idx: play_audio(i))

        start_idx = end_idx

def show_speaker(event, speaker):
    width = len(speaker) * 7 + 10
    speaker_canvas.configure(width=width)
    speaker_canvas.itemconfig(speaker_text, text=speaker, fill="black")
    x, y, _, _ = text_display.bbox(tk.CURRENT)
    speaker_canvas.place(x=event.x_root - text_display.winfo_rootx(), y=y + 20)

def hide_speaker(event):
    speaker_canvas.place_forget()

def play_audio(index):
    global currently_playing
    folder_path = 'generated_audio_clips'
    audio_file = os.path.join(folder_path, f"audio_{index}.wav")
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        currently_playing = None
        return

    if currently_playing != audio_file:
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        currently_playing = audio_file

# Functions from gui_generate_with_preview.py
def download_model(model_name):
    model_path = MODEL_NAMES[model_name]
    if not os.path.exists(model_path):
        url_map = {
            "en_us_cmuartic_jets_cpu.addon": "https://huggingface.co/balacoon/tts/resolve/main/en_us_cmuartic_jets_cpu.addon",
            "en_us_hifi_jets_cpu.addon": "https://huggingface.co/balacoon/tts/resolve/main/en_us_hifi_jets_cpu.addon"
        }
        subprocess.run(['wget', url_map[model_path]])
    return model_path

def update_voices():
    global tts, supported_speakers

    model_name = model_combobox.get()
    model_path = download_model(model_name)
    tts = TTS(model_path)
    supported_speakers = tts.get_speakers()
    for character_combobox in speaker_dropdown_mapping.values():
        character_combobox["values"] = supported_speakers
        character_combobox.set(random.choice(supported_speakers))

def preview_voice(character):
    speaker = speaker_dropdown_mapping[character].get()
    preview_text = preview_entry.get()
    samples = tts.synthesize(preview_text, speaker)

    with wave.open("temp_preview.wav", "w") as fp:
        fp.setparams((1, 2, tts.get_sampling_rate(), len(samples), "NONE", "NONE"))
        fp.writeframes(samples)
    subprocess.run(['xdg-open', 'temp_preview.wav'])

def get_unique_characters_from_csv(filename):
    with open(filename, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        return set(row['Speaker'] for row in reader)

def synthesize_and_save(text, speaker_name, output_filename):
    speaker = speaker_dropdown_mapping[speaker_name].get()
    samples = tts.synthesize(text, speaker)
    with wave.open(output_filename, "w") as fp:
        fp.setparams((1, 2, tts.get_sampling_rate(), len(samples), "NONE", "NONE"))
        fp.writeframes(samples)

def process_csv():
    folder_path = 'generated_audio_clips'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open('book.csv', mode='r', encoding='utf-8-sig') as csvfile:
        reader = list(csv.DictReader(csvfile))
        total = len(reader)
        for index, row in enumerate(reader):
            text = row['Text']
            speaker = row['Speaker']
            output_filename = os.path.join(folder_path, f"audio_{index}.wav")
            synthesize_and_save(text, speaker, output_filename)
            current_percentage = (index+1)/total * 100
            progress_var.set(current_percentage)
            label.config(text=f"{current_percentage:.2f}% done")
            root.update_idletasks()
        label.config(text="Complete!")

# Main GUI Setup
root = tk.Tk()
root.title("Combined GUI")
root.geometry("1200x800")

# TTS Section
tts_frame = ttk.Frame(root)
tts_frame.pack(pady=10, fill=tk.X)

model_label = ttk.Label(tts_frame, text="Select Model:")
model_label.grid(row=0, column=0, padx=5, pady=5)
model_combobox = ttk.Combobox(tts_frame, values=list(MODEL_NAMES.keys()), state="readonly")
model_combobox.grid(row=0, column=1, padx=5, pady=5)
model_combobox.bind("<<ComboboxSelected>>", lambda event: update_voices())
model_combobox.set(list(MODEL_NAMES.keys())[0])

preview_label = ttk.Label(tts_frame, text="Preview Text:")
preview_label.grid(row=0, column=2, padx=5, pady=5)
preview_entry = ttk.Entry(tts_frame, width=30)
preview_entry.grid(row=0, column=3, padx=5, pady=5)
preview_entry.insert(0, "Hello, this is a voice preview.")

unique_characters = get_unique_characters_from_csv('book.csv')
speaker_dropdown_mapping = {}
scrollable_frame = ttk.Frame(tts_frame)
canvas = tk.Canvas(scrollable_frame)
scrollbar = ttk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
horizontal_scrollbar = ttk.Scrollbar(scrollable_frame, orient="horizontal", command=canvas.xview)  # New horizontal scrollbar
scrollable_window = tk.Frame(canvas)
scrollable_window.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)
canvas.create_window((0, 0), window=scrollable_window, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set, xscrollcommand=horizontal_scrollbar.set)  # Updated to include horizontal scrollbar

for index, character in enumerate(unique_characters, start=1):
    ttk.Label(scrollable_window, text=character).grid(row=index, column=0, padx=5, pady=5)
    combobox = ttk.Combobox(scrollable_window, width=20)  # Updated with width
    combobox.grid(row=index, column=1, padx=5, pady=5)
    speaker_dropdown_mapping[character] = combobox
    preview_button = ttk.Button(scrollable_window, text="Preview", command=lambda char=character: preview_voice(char), width=10)  # Updated with width
    preview_button.grid(row=index, column=2, padx=5, pady=5)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
horizontal_scrollbar.pack(side="bottom", fill="x")  # New horizontal scrollbar pack
scrollable_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

update_voices()
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(tts_frame, variable=progress_var, maximum=100)
progress_bar.grid(row=len(unique_characters)+2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10, padx=5)
label = ttk.Label(tts_frame, text="Select voices for characters and click 'Start'")
label.grid(row=len(unique_characters)+1, column=0, columnspan=4, pady=5)
start_button = ttk.Button(tts_frame, text="Start", command=lambda: threading.Thread(target=process_csv).start())
start_button.grid(row=len(unique_characters)+3, column=0, columnspan=4, pady=20)

# Book Display Section
book_frame = ttk.Frame(root)
book_frame.pack(pady=10, expand=True, fill='both')

text_display = scrolledtext.ScrolledText(book_frame, wrap=tk.WORD, cursor="arrow")
text_display.pack(expand=True, fill='both', padx=10, pady=10)

speaker_canvas = tk.Canvas(book_frame, height=20, bg="white", bd=1, relief="solid")
speaker_text = speaker_canvas.create_text(5, 10, anchor="w")

load_and_display_button = ttk.Button(book_frame, text="Load and Display Book", command=display_content)
load_and_display_button.pack(pady=10)

root.mainloop()

