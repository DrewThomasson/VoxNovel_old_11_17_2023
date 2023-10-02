# VoxNovel
![VoxNovelLogo](https://github.com/DrewThomasson/VoxNovel/assets/126999465/34b5b312-aa70-44e4-a35c-f3f5ac1b24de)

**VoxNovel:** GPT-4 powered audiobooks with unique character voices.
**Only compatable with Ubuntu linux at the moment**
    
    -Created Notebook versions of this to be run in google colab for free if you don't have Ubuntu

## Overview

VoxNovel is an innovative program that leverages the capabilities of GPT-4 to analyze literature, attribute quotations to specific characters, and generate a tailored audiobook where each character has a distinct voice. This not only provides an immersive audiobook experience but also brings each character to life with a unique voice, making the listening experience much more engaging.

## How to Run VoxNovel

1. **Setup**:
    - Clone the repository: `git clone https://github.com/DrewThomasson/VoxNovel`.
    - Navigate to the directory: `cd VoxNovel`.
    - Install the balacoon package via pip.
    - `pip install -i https://pypi.fury.io/balacoon/ balacoon-tts`
    - `pip install numpy`
    - `pip install huggingface_hub`
    - `pip install openai`
    - Install the necessary packages: 

2. **Run full VOXNOVEL GUI**:
    - In terminal: `run_gui.py`.
    - Close out of each GUI when it says "Complete", and the next GUI in order will automatically run.

### About Files

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/1d357806-7eff-4855-a8e3-7d147e181e99)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/72e43fa0-ebb3-4074-8ec5-d2cf88d335af)


3. **gui_create_quotes_files.py**:
    - This program accepts a .txt file of your book. Ensure it is consistently formatted regarding how quotes are presented.
    - It will either automatically detect or allow manual input of delimiters used in your book for character quotes.
    - Outputs a `quotes.csv` file containing all character quotes with specified start and end delimiters.
    - Outputs a `nonquotes.csv` file for narration, containing everything that isn't a character quote.
    - Finally, displays a merged view of narration and character quotes as a single CSV file.

    **Requirements**:
    - Your book in `.txt` format.
    - Your OpenAI key.

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/04895691-38f2-4565-85e5-d9cbf3eecb25)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/0c3fb9f5-5a08-4dd9-a919-40aeb37bd2ef)



4. **speaker_find_attribute.py**:
    - Designed to identify the speaker of quotes using OpenAI's GPT-4.

    **Functionality**:
        - Input your OpenAI API key and select the `.txt` file.
        - Specify the number of requests or allow the program to decide based on `quotes.csv` length.
        - Real-time progress updates.
        - Observes a 60-second pause every 20 requests due to API limits.
        - Appends speaker names to the `quotes.csv` file upon completion.

    **Requirements**:
        - Text in `.txt` format.
        - OpenAI API key.
        - `quotes.csv` with columns for each quote's start and end locations.

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/7d8a64db-dfe5-4be2-b510-dae852b4d6d2)


5. **create_book_csv.py**:
    - Merges `quotes.csv` and `non_quotes.csv` to produce a unified `book.csv`, ensuring chronological order.

    **Functionality**:
        - On start, a GUI button initiates processing.
        - Reads `quotes.csv` and `non_quotes.csv`, marking quotes with 'True' and non-quotes with 'False'.
        - Combines data, sorts by start location, and outputs `book.csv`.
        - GUI progress bar fills as processing progresses, signaling completion with a message.

    **Requirements**:
        - `quotes.csv` and `non_quotes.csv` with columns for text content, start/end locations, and speaker (speaker in 4th column).
        - A GUI-compatible system.

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/30c013c3-080b-4ea7-a076-295d4cdfc8a0)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/5bd87dcc-5957-4aaf-a690-65d159d46c40)

6. **book_display_and_generate_with_preview.py**:
    - This program provides a GUI interface to display book content and generate voice-over for it.
    - Books should be in `.csv` format with at least two columns: `Speaker` and `Text`.
    - Allows users to select a TTS model and map unique speakers in the book to different voice-over characters.
    - Supports voice preview for selected characters to help users make an informed choice.
    - Outputs audio files (in `.wav` format) for each row in the book, synthesized using the selected voices.
    - Features a progress bar to show completion status while processing the CSV to generate voiceovers.
    - Displays the book content in a color-coded format, with different colors for different speakers. Hovering over the colored sections will display the name of the speaker.
    - Users can click on any section in the book display to play the corresponding audio.

    **Requirements**:
    - Your book in `.csv` format with columns `Speaker` and `Text`.
    - Internet connection to download the TTS models.
    - Required Python libraries: `csv`, `wave`, `random`, `os`, `subprocess`, `pandas`, `pygame`, `tkinter`, `threading`, `balacoon_tts`, `huggingface_hub`.


![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/8f7ab11a-6650-44cf-9b22-c2b322a7fa1d)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/297a62cb-61a5-4f43-9a14-1182db93e87d)




7. **book_display_and_combine_gui.py.py**:
    - A multifunctional GUI application allowing:
        1. Book display with speaker-based background colors.
        2. Audio previews for book sections.
        3. Combining audio chunks with specified silence durations.

    **Functionality**:
        - **Book Display**: Loads `book.csv`, differentiating speakers by background color. Hover to see speaker names; click to play audio.
        - **Audio Preview**: Links text segments to corresponding `audio_INDEX.wav` files. Click to play/stop audio.
        - **Audio Combination**: Specify silence duration between chunks and combine them into `combined_audio.wav` with a progress bar.

    **Requirements**:
        - `book.csv` with columns for text and speaker.
        - Audio files named `audio_INDEX.wav`.
        - Libraries: `pandas`, `torch`, `torchaudio`, `tkinter`, `pygame`.

8. **Enjoy!**:
    - Relish your auto-generated audiobook, with each character uniquely voiced.
  

   **DEMO**
   

https://github.com/DrewThomasson/VoxNovel/assets/126999465/530e8781-c77c-4424-89cd-a02df363b0bf


https://github.com/DrewThomasson/VoxNovel/assets/126999465/53b694a9-5ddd-4174-82bc-07aff22d2330



## Contributing

We welcome VoxNovel contributions! Open an issue or submit a pull request for suggestions, improvements, or feature additions.


The revised README should now be more organized and easier to understand for users looking to engage with the VoxNovel project.
