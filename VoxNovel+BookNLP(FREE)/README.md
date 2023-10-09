# Local Processing with BookNLP

Efficiently process speaker quotations in books, running entirely on your local machine without any external costs!

## Prerequisites

Before you proceed, make sure to install **BookNLP** on your system. It is an essential component for speaker quotation attribution in books when using this approach.

[BookNLP GitHub Repository](https://github.com/booknlp/booknlp)

If you are going to be using tortoise then you should install the tortoise github into this folder so the longtortoise genreate can its voice folder

git clone https://github.com/152334H/tortoise-tts-fast.git

## Execution Order in Terminal

1. `python Gui_bookNLP.py`
2. `python run_gui.py`

## File Descriptions:

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/16015a7d-57db-4dc6-ac35-64aeaab56482)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/8a8024e5-fb37-4809-9eb5-3d662be9ef0f)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/c4044b84-bb12-4dd2-a058-f374f7d13ed1)

### Gui_bookNLP.py:
**Purpose**: Provides a Graphical User Interface (GUI) to manage and interact with the BookNLP functionalities.

**Functionality**:
- Provides a user-friendly interface to interact with BookNLP.
- TBD (Specify further functionalities.)

**Requirements**:
- BookNLP installed on the system.
- TBD (Any other dependencies.)

### run_gui.py:
**Purpose**: Acts as the main runner GUI that integrates and provides access to various functionalities in the repository.

**Functionality**:
- Initiates the main interface that links other GUIs and functionalities.
- TBD (Further details.)

**Requirements**:
- TBD (Any dependencies.)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/8fbe46cb-d839-4ae3-a818-483d79f4de73)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/41795c94-faf8-4a56-ad54-0171ce3d4100)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/5ea89662-d779-4712-b8a5-e1f4d71b8138)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/b7a71e76-993d-446d-ab88-90d6d3f60f79)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/3da23be4-196e-4991-98b4-d9966fe0ce37)


### Manual_name_selectGUIQuotesCSV.py:
**Purpose**: Enables manual selection and editing of names associated with character IDs from a GUI, and creates a structured CSV output.

**Functionality**:
- Imports and processes quote, token, and entity data from specified files.
- Allows for manual selection of character names for specific character IDs.
- Outputs a "quotes.csv" file with structured quote data including text, locations, and speakers.

**Requirements**:
- `pandas` library for data manipulation.
- `tkinter` library for GUI functionality.
- Pre-existing input files: quotes, tokens, and entities in .csv format.

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/c6111137-7ee3-4c3d-8aa3-8bd61a4ff9e0)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/cb35d1fc-d0d2-4e7e-b10e-959aa38a5a3c)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/7956bcdb-07b4-4456-aad7-8ed2c2ec23ff)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/d576a649-6200-4257-a469-f8734d217375)

### GUINonQuotesCSV.py:
**Purpose**: This script processes selected files to segment and save non-quote sections from a book into a separate CSV file.

**Functionality**:
- Provides a GUI for users to select two required files: quotes file and tokens file.
- Processes the selected files to iterate through quotes, identify gaps (non-quote sections) between consecutive quotes, and save these sections.
- Uses token data to reconstruct the non-quote sections, adjusting for punctuation and formatting.
- Outputs the processed non-quote data into a "non_quotes.csv" file with columns for Text, Start Location, End Location, Is Quote, and Speaker. The speaker for non-quotes is labeled as "Narrator".

**Requirements**:
- `pandas` library for data manipulation.
- Input files: A quotes file and a tokens file in .csv format.

**GUI Features**:
- A button for selecting and processing the required files.
- A label to display the processing status.


![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/3af79d23-394c-4011-8d33-1a95b2a0660a)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/9e70a443-1201-47ab-a566-f307ba0debef)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/aa66e301-0de3-438a-a156-c510ea0f1296)


### GUIQuotesCSV.py:
**Purpose**: This script processes selected files to recognize and associate character names with their respective quotes, using named entity recognition from the NLTK library.

**Functionality**:
- Downloads the necessary NLTK data for tokenization and named entity recognition.
- Provides a GUI for users to select three required files: quotes file, tokens file, and entities file.
- Processes the selected files to build a character names dictionary based on character IDs.
- Uses NLTK's named entity recognition to refine and determine the most common name for each character ID.
- Iterates through the quotes data to match tokens to their respective quotes, recognize named entities, and append associated character names.
- Outputs the processed data into a "quotes.csv" file with columns for Text, Start Location, End Location, Is Quote, and Speaker.

**Requirements**:
- `pandas` library for data manipulation.
- `nltk` library for named entity recognition and other natural language processing functionalities.
- Input files: A quotes file, a tokens file, and an entities file in .csv format.




![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/efd73504-c220-4427-9df0-0c66555e3f29)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/eacae753-61c7-4810-80a9-a9596a82b33f)


### create_book_csv.py:
**Purpose**: Converts a book's text into a structured CSV format.

**Functionality**:
- Parses input text and structures it into rows and columns for further processing.
- Outputs a structured CSV file.

**Requirements**:
- `pandas` library for data manipulation.
- Input text in a specified format.

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/8d171836-1ff6-4aed-858e-d6c783b10df8)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/6679102d-8591-49e6-a810-f0eb06a839b2)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/8d8ba5b4-3862-49d8-94d5-016c0039f686)

### book_display_and_generate_with_preview.py:
**Purpose**: Allows users to preview the parsed book data before generating the final output.

**Functionality**:
- Displays book data in a GUI.
- Allows for final editing and confirmation.
- Generates the final processed file upon confirmation.

**Requirements**:
- TBD (Any dependencies.)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/0fa4328b-d86f-4175-9cc6-e57a5656b38f)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/3042ef00-620b-40d7-8e00-8f97e1074fbe)

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/8f674e9e-dc88-432b-bc5a-11202a2c7d92)


### book_display_and_combine_gui.py:
**Purpose**: Provides a GUI for combining and displaying multiple book data files.

**Functionality**:
- Imports multiple book data files.
- Allows for combined viewing and editing.
- Exports a single combined file upon confirmation.

**Requirements**:
- `pandas` library for data manipulation.
- Multiple book data files in the required format.

## Getting Started:

1. Make sure all required libraries and dependencies are installed.
2. Run the desired script following the execution order above.
3. Follow the GUI prompts to access and utilize the tools and features.

## Contributing:

Your contributions are always welcome! Please fork this repository and submit pull requests for any enhancements. For significant changes or feature additions, please open an issue first to discuss your proposal.
