import os
import pandas as pd
import random
import shutil  # for copying files

import torch
import torchaudio
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio, load_voice, load_voices

import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')

data = pd.read_csv("book.csv")
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
    ensure_output_folder()
    total_rows = len(data)
    tts = TextToSpeech()

    speaker_voice_map = {}
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

