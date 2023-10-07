import tkinter as tk
from tkinter import filedialog, messagebox
from epub2txt import epub2txt

def convert_epub_to_txt(file_path):
    """Convert EPUB to TXT."""
    content = epub2txt(file_path)
    cleaned_content = '\n'.join(line for line in content.splitlines() if not line.startswith('@page'))
    return cleaned_content

def select_file():
    """Open a file dialog and set the selected file path to the entry widget."""
    file_path = filedialog.askopenfilename(filetypes=[('EPUB files', '*.epub')])
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def perform_conversion():
    """Convert the selected EPUB file to TXT and save it."""
    file_path = entry.get()
    if not file_path:
        messagebox.showerror("Error", "Please select an EPUB file first.")
        return

    content = convert_epub_to_txt(file_path)
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[('Text files', '*.txt')])

    if save_path:
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(content)
        messagebox.showinfo("Success", "File converted and saved successfully!")

# Set up the main GUI window
root = tk.Tk()
root.title("EPUB to TXT Converter")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="Select an EPUB file:")
label.pack(anchor="w")

entry = tk.Entry(frame, width=50)
entry.pack(fill="x")

browse_button = tk.Button(frame, text="Browse", command=select_file)
browse_button.pack(anchor="e", pady=(5, 10))

convert_button = tk.Button(frame, text="Convert to TXT", command=perform_conversion)
convert_button.pack()

root.mainloop()

