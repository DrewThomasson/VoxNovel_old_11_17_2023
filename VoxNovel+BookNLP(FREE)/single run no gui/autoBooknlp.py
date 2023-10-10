import os
import tkinter as tk
from tkinter import filedialog, messagebox
from epub2txt import epub2txt
from booknlp.booknlp import BookNLP

def convert_epub_to_txt(file_path):
    """Convert EPUB to TXT."""
    content = epub2txt(file_path)
    cleaned_content = '\n'.join(line for line in content.splitlines() if not line.startswith('@page'))
    return cleaned_content

def process_file():
    file_path = filedialog.askopenfilename(title='Select File', filetypes=[('Text and EPUB Files', ('*.txt', '*.epub'))])
    if not file_path:
        return

    if file_path.endswith('.epub'):
        # Convert EPUB to TXT first
        content = convert_epub_to_txt(file_path)
        # Save converted content to Working_files directory
        if not os.path.exists('Working_files'):
            os.makedirs('Working_files')
        file_path = os.path.join('Working_files', 'Book.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    elif not file_path.endswith('.txt'):
        messagebox.showerror("Error", "Selected file is not a TXT or EPUB file.")
        return

    # Now process the TXT file with BookNLP
    book_id = "Book"
    output_directory = os.path.join('Working_files', book_id)

    model_params = {
        "pipeline": "entity,quote,supersense,event,coref",
        "model": "big"
    }

    booknlp = BookNLP("en", model_params)
    booknlp.process(file_path, output_directory, book_id)

    messagebox.showinfo("Success", "File processed successfully!")
    
    # Close the GUI
    root.destroy()

root = tk.Tk()
root.title("BookNLP Processor")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

process_button = tk.Button(frame, text="Process File", command=process_file)
process_button.pack()

root.mainloop()

