import csv
import os
import nltk
import numpy as np
import random

import nltk
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
        # Advanced Long-Form Generation
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
        # Simple Long-Form Generation
        for sentence in sentences:
            audio_array = generate_audio(sentence, history_prompt=speaker)
            pieces += [audio_array, silence.copy()]

    return np.concatenate(pieces)

speakers_dict = {}  # to store unique speakers

with open("book.csv", "r") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # skip header

    for idx, row in enumerate(csv_reader):
        text = row[0]  # "Text" is in column 0
        speaker_name = row[3]  # "Speaker" is in column 3

        # If the speaker name doesn't exist in our dictionary, add it with a random voice actor
        if speaker_name not in speakers_dict:
            speakers_dict[speaker_name] = random.choice(voice_actors)

        speaker = speakers_dict[speaker_name]  # get the assigned speaker to use
        print(f"Generating audio for the text: {text}")
        print(f"speakers dictionary is {speakers_dict}")
        audio_data = generate_long_form_audio(text, speaker)
        
        
        file_name = f"audio_{idx}"  # naming the audio files
        write_wav(f"{file_name}.wav", SAMPLE_RATE, audio_data)

print("Finished generating audio files!")

