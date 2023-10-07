import tkinter as tk
from tkinter import filedialog
from booknlp.booknlp import BookNLP

def process_file():
    input_file = filedialog.askopenfilename(title='Select Input File', filetypes=[('Text Files', '*.txt')])
    if not input_file:
        return

    book_id = entry.get()
    if not book_id:
        book_id = "default_book_id"

    output_directory = f"output_dir/{book_id}/"

    model_params = {
        "pipeline": "entity,quote,supersense,event,coref",
        "model": "big"
    }

    booknlp = BookNLP("en", model_params)
    booknlp.process(input_file, output_directory, book_id)

root = tk.Tk()
root.title("BookNLP Processor")

entry_label = tk.Label(root, text="Enter Book ID:")
entry_label.pack()

entry = tk.Entry(root)
entry.pack()

process_button = tk.Button(root, text="Process File", command=process_file)
process_button.pack()

root.mainloop()

