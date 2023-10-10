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

