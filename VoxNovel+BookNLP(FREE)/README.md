# Local Processing with BookNLP

Efficiently process speaker quotations in books, running entirely on your local machine without any external costs!

## Prerequisites

Before you proceed, make sure to install **BookNLP** on your system. It is an essential component for speaker quotation attribution in books when using this approach.

[BookNLP GitHub Repository](https://github.com/booknlp/booknlp)

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

### GUINonQuotesCSV.py:
**Purpose**: TBD (Specify the purpose of this script.)

**Functionality**:
- TBD (Specify its functionalities.)

**Requirements**:
- TBD (Any dependencies.)

### GUIQuotesCSV.py:
**Purpose**: TBD

**Functionality**:
- TBD

**Requirements**:
- TBD

### create_book_csv.py:
**Purpose**: Converts a book's text into a structured CSV format.

**Functionality**:
- Parses input text and structures it into rows and columns for further processing.
- Outputs a structured CSV file.

**Requirements**:
- `pandas` library for data manipulation.
- Input text in a specified format.

### book_display_and_generate_with_preview.py:
**Purpose**: Allows users to preview the parsed book data before generating the final output.

**Functionality**:
- Displays book data in a GUI.
- Allows for final editing and confirmation.
- Generates the final processed file upon confirmation.

**Requirements**:
- TBD (Any dependencies.)

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
