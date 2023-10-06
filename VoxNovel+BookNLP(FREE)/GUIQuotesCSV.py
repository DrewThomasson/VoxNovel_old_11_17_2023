import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Listbox
import pandas as pd

def generate_csv():
    # Load the files
    df_quotes = pd.read_csv("158_emma.quotes", delimiter="\t")
    df_tokens = pd.read_csv("158_emma.tokens", delimiter="\t", error_bad_lines=False, quoting=3)
    df_entities = pd.read_csv("158_emma.entities", delimiter="\t")

    # Build a dictionary to hold character names by char_id
    char_names_dict = {}
    for index, row in df_entities.iterrows():
        char_id = row['COREF']
        name = row['text']
        if char_id not in char_names_dict:
            char_names_dict[char_id] = set()
        char_names_dict[char_id].add(name)

    quotes_data = []  # List to hold data for quotes.csv

    # Iterate through the quotes dataframe
    for index, row in df_quotes.iterrows():
        start_id = row['quote_start']
        end_id = row['quote_end']
        char_id = row['char_id']  # Get char_id from df_quotes
        
        # Filter the tokens
        filtered_tokens = df_tokens[(df_tokens['token_ID_within_document'] > start_id) & 
                                    (df_tokens['token_ID_within_document'] < end_id)]
        
        # Build the words chunk
        words_chunk = ' '.join([token_row['word'] for index, token_row in filtered_tokens.iterrows()])
        
        # Get character names from char_names_dict
        char_names = ", ".join(char_names_dict.get(char_id, []))
        speaker_info = f"{char_id}:{char_names}"
        
        # Append data to quotes_data
        quotes_data.append([words_chunk, start_id, end_id, "True", speaker_info])

    # Create a DataFrame for quote data
    global quotes_df
    quotes_df = pd.DataFrame(quotes_data, columns=["Text", "Start Location", "End Location", "Is Quote", "Speaker"])

    # Write to quotes.csv
    quotes_df.to_csv("quotes.csv", index=False)

def update_name():
    selected_name = name_listbox.get(name_listbox.curselection())
    char_id = name_selection_window.title().split()[-1]  # get char_id from window title
    quotes_df.loc[quotes_df['Speaker'].str.startswith(f"{char_id}:"), 'Speaker'] = f"{char_id}:{selected_name}"
    quotes_df.to_csv("quotes.csv", index=False)
    name_selection_window.destroy()

def edit_names(char_id):
    global name_selection_window, name_listbox
    names = char_id_name_dict[char_id]
    name_selection_window = Toplevel(window)
    name_selection_window.title(f"Select Name for Character ID {char_id}")
    name_listbox = Listbox(name_selection_window, selectmode=tk.SINGLE)
    for name in names:
        name_listbox.insert(tk.END, name)
    name_listbox.pack()
    confirm_button = tk.Button(name_selection_window, text="Confirm", command=update_name)
    confirm_button.pack()

def launch_gui():
    global window, char_id_name_dict

    window = tk.Tk()
    window.title("Edit Names GUI")

    frame = ttk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(frame)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.update_idletasks()

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.configure(yscrollcommand=scrollbar.set)

    # Load the CSV
    global quotes_df
    quotes_df = pd.read_csv("quotes.csv")

    # Get unique character IDs and names
    char_id_name_dict = {}
    for speaker_info in quotes_df['Speaker'].unique():
        char_id, names = speaker_info.split(':', 1)  # Updated line
        char_id_name_dict[char_id] = names.split(', ')

    for char_id, names in char_id_name_dict.items():
        char_button = ttk.Button(scrollable_frame, text=f"Edit Names for Character ID {char_id}", command=lambda char_id=char_id: edit_names(char_id))
        char_button.pack(fill=tk.X)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    window.mainloop()

# Generate CSV and launch GUI
generate_csv()
launch_gui()

