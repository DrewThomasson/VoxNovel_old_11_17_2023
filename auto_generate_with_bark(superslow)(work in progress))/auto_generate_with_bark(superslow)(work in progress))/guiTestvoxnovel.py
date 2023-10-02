import pandas as pd
import tkinter as tk
from tkinter import scrolledtext
import pygame

colors = ['#FFB6C1', '#ADD8E6', '#FFDAB9', '#98FB98', '#D8BFD8']
speaker_colors = {}
currently_playing = None

# Initialize pygame mixer for audio playback
pygame.mixer.init()

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

        # Bind the hover events and click event
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
    print(f"audio_{index}.wav")

    # If an audio is playing, stop it
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        currently_playing = None
        return

    # If the clicked audio is different from the last played one or no audio was played before, play it
    if currently_playing != audio_file:
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        currently_playing = audio_file

root = tk.Tk()
root.title("Book Display")
root.geometry("800x600")

text_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, cursor="arrow")
text_display.pack(expand=True, fill='both', padx=10, pady=10)

speaker_canvas = tk.Canvas(root, height=20, bg="white", bd=1, relief="solid")
speaker_text = speaker_canvas.create_text(5, 10, anchor="w")

load_button = tk.Button(root, text="Load and Display Book", command=display_content)
load_button.pack(pady=10)

root.mainloop()
