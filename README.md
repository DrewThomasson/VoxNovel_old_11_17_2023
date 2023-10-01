# VoxNovel
VoxNovel: GPT-4 powered audiobooks with unique character voices.
# VoxNovel: Automatic Audiobook Generation with Character Voice Assignment

VoxNovel is an innovative program that leverages the capabilities of GPT-4 to analyze literature, attribute quotations to specific characters, and generate a tailored audiobook where each character has a distinct voice. This not only provides an immersive audiobook experience but also brings each character to life with a unique voice, making the listening experience much more engaging.

## Repository Structure

### Files:

1. **book_to_csv.py**: 
    - Takes a `.txt` file as input and utilizes GPT-4's advanced capabilities to detect and attribute quotations to characters.
    - Outputs the content in a structured `.csv` format with columns 'Speaker' and 'Text'.

2. **book_display_and_combine_with_preview.py**:
    - This script offers a GUI where users can view the book's content with highlighted speakers.
    - Offers Text-to-Speech (TTS) previews and the ability to generate audio segments for each quotation.

3. **book_display_and_combine_gui.py**:
    - A dedicated GUI tool that allows users to:
        - Display the book content color-coded based on the speaker.
        - Combine generated audio files with user-specified silence durations between chunks.

4. **generate_audiobook.py**:
    - Generates an audiobook by stitching together audio chunks corresponding to the content of the book.
    - Differentiates characters using unique voice actors to create an immersive listening experience.

## How to Run VoxNovel:

1. **Setup**:
    - Clone the repository: `git clone <repository_url>`.
    - Navigate to the directory: `cd VoxNovel`.
    - Install the necessary packages: `pip install -r requirements.txt` (Make sure you have `pip` installed).

2. **Convert Book to CSV**:
    - Run `python book_to_csv.py --input_path <path_to_txt_file>`.
    - This will generate a `book.csv` file in the current directory with the book content.

3. **Generate Audio Segments**:
    - Open the GUI to preview content: `python book_display_and_combine_with_preview.py`.
    - Review the content and generate audio segments using the provided controls.

4. **Combine Audio Segments**:
    - To stitch the audio files together with specified silence durations, run the GUI tool: `python book_display_and_combine_gui.py`.
    - Load the book, set desired silence duration, and combine the audio segments.

5. **Generate the Audiobook**:
    - Run `python generate_audiobook.py` to generate the final audiobook.

6. **Enjoy!**
    - Listen to your automatically generated audiobook with each character having a unique voice.

## Contributing:

We welcome contributions to VoxNovel! Please feel free to open an issue or submit a pull request if you have suggestions, improvements, or features to add.

## License:

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

With the provided README, users should have a clear understanding of what each file in the VoxNovel project does and how to execute them to generate their own audiobooks. You can further enhance this README by adding sections on dependencies, troubleshooting, acknowledgments, or any other specific information you'd like to share about VoxNovel.
