import os
import pandas as pd
import torch
import torchaudio
import tkinter as tk
from tkinter import ttk, scrolledtext
import pygame

# Global Variables & Initializations
colors = ['#FFB6C1', '#ADD8E6', '#FFDAB9', '#98FB98', '#D8BFD8']
speaker_colors = {}
currently_playing = None
pygame.mixer.init()

# Book Display Functions
def display_content():
    df = pd.read_csv('book.csv')
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
    audio_file = f"audio_{index}.wav"
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        currently_playing = None
        return
    if currently_playing != audio_file:
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        currently_playing = audio_file

# Audio Combine Functions
def combine_audio_files(silence_duration_ms):
    folder_path = os.getcwd()
    files = sorted([f for f in os.listdir(folder_path) if f.startswith("audio_") and f.endswith(".wav")], key=lambda f: int(f.split('_')[1].split('.')[0]))
    combined_tensor = torch.Tensor()
    progress_var.set(0)
    for index, file in enumerate(files):
        waveform, sample_rate = torchaudio.load(os.path.join(folder_path, file))
        channels = waveform.shape[0]
        silence_tensor = torch.zeros(channels, int(silence_duration_ms * sample_rate / 1000))
        combined_tensor = torch.cat([combined_tensor, waveform, silence_tensor], dim=1)
        progress_var.set((index + 1) / len(files) * 100)
        root.update()
    torchaudio.save(os.path.join(folder_path, "combined_audio.wav"), combined_tensor, sample_rate)
    progress_var.set(100)
    progress_label.config(text="Complete!")

def update_duration_label(value):
    duration_label.config(text=f"{int(float(value))} ms")

def start_combining():
    silence_duration = slider.get()
    combine_audio_files(silence_duration)

# Main GUI
root = tk.Tk()
root.title("Book and Audio Manager")
root.geometry("900x800")

text_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, cursor="arrow")
text_display.pack(expand=True, fill='both', padx=10, pady=10)

speaker_canvas = tk.Canvas(root, height=20, bg="white", bd=1, relief="solid")
speaker_text = speaker_canvas.create_text(5, 10, anchor="w")

load_button = tk.Button(root, text="Load and Display Book", command=display_content)
load_button.pack(pady=10)

frame = ttk.Frame(root, padding="10")
frame.pack(pady=20)

ttk.Label(frame, text="Silence Duration (ms) between audio chunks:").grid(row=0, column=0, sticky=tk.W, pady=5)
slider = ttk.Scale(frame, from_=0, to=2000, orient=tk.HORIZONTAL, length=300, command=update_duration_label)
slider.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
duration_label = ttk.Label(frame, text="0 ms")
duration_label.grid(row=1, column=1, pady=5)

btn = ttk.Button(frame, text="Combine Audio Files", command=start_combining)
btn.grid(row=2, column=0, pady=10)
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate", variable=progress_var)
progress_bar.grid(row=3, column=0, pady=5)
progress_label = ttk.Label(frame, text="0%")
progress_label.grid(row=4, column=0, pady=5)

root.mainloop()

