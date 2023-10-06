import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os

from langchain.llms import CTransformers
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

llm = CTransformers(model="TheBloke/Llama-2-13B-Chat-GGML", model_file='llama-2-13b-chat.ggmlv3.q2_K.bin', callbacks=[StreamingStdOutCallbackHandler()])

template = """
[INST] <<SYS>>
You are a helpful, respectful and honest assistant. Your answers are always brief.
<</SYS>>
{text}[/INST]
"""

prompt = PromptTemplate(template=template, input_variables=["text"])
llm_chain = LLMChain(prompt=prompt, llm=llm)


def extract_sentence(start, end, filename):
    with open(filename, 'r') as f:
        content = f.read()
    sentence = content[start:end]
    return sentence


def extract_context(sentence, filename):
    with open(filename, 'r') as f:
        content = f.read()
    start_index = content.find(sentence)
    if start_index == -1:
        return None
    left_index = max(0, start_index - 500)
    right_index = min(len(content), start_index + len(sentence) + 500)
    return content[left_index:right_index]


def ask_llama2(context, sentence, names):
    input_text = f"""you are an ai model that will respond with the name in all caps:: {context} :Who said :{sentence} answer in only the name and nothing else"""
    print(input_text)
    response = llm_chain.run(input_text)
    return response.upper().strip()


def warn_about_costs(txt_file_path):
    file_size = os.path.getsize(txt_file_path)
    if file_size > 0:
        result = messagebox.askyesno(
            "Cost Warning",
            "Processing large files like an entire book can be costly. For example, processing the entirety of 'Alice in Wonderland' might cost around $10-13, "
            "though it depends on how many quotes from characters exist in the book. Do you wish to continue?"
        )
        if not result:
            return False
    return True


def main(txt_file_path, progress_var, status_label, num_of_wanted_requests):
    df = pd.read_csv('quotes.csv')
    responses = []
    names = []
    request_counter = 0

    for index, row in df.head(num_of_wanted_requests).iterrows():
        sentence = extract_sentence(row['Start Location'], row['End Location'], txt_file_path)
        context = extract_context(sentence, txt_file_path)
        response = ask_llama2(context, sentence, names)
        responses.append(response)
        if response not in names:
            names.append(response)
        request_counter += 1
        progress = (request_counter / num_of_wanted_requests) * 100
        progress_var.set(progress)
        status_label['text'] = f"Processing: {request_counter}/{num_of_wanted_requests}"

    df.loc[df.head(num_of_wanted_requests).index, 'Speaker'] = responses
    df.to_csv('quotes.csv', index=False)
    status_label['text'] = "Done"


def on_start(txt_file_entry, progress_var, status_label, manual_var, manual_entry):
    txt_file_path = txt_file_entry.get()

    if not txt_file_path:
        messagebox.showerror("Error", "Please select the text file.")
        return

    if not warn_about_costs(txt_file_path):
        return

    num_of_wanted_requests = len(pd.read_csv('quotes.csv'))
    if manual_var.get():
        try:
            manual_value = int(manual_entry.get())
            if manual_value > num_of_wanted_requests:
                messagebox.showwarning("Warning", f"Number entered ({manual_value}) is greater than rows in CSV ({num_of_wanted_requests}). Using CSV row count.")
            else:
                num_of_wanted_requests = manual_value
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
            return

    status_label['text'] = "Processing..."
    thread = threading.Thread(target=main, args=(txt_file_path, progress_var, status_label, num_of_wanted_requests))
    thread.start()


def create_gui():
    root = tk.Tk()
    root.title("Llama2 Speaker Identifier")

    ttk.Label(root, text="Text File:").pack(pady=10, padx=10)
    txt_file_entry = ttk.Entry(root, width=40)
    txt_file_entry.pack(pady=10, padx=10, side=tk.LEFT)
    txt_file_btn = ttk.Button(root, text="Browse", command=lambda: txt_file_entry.delete(0, tk.END) or txt_file_entry.insert(tk.END, filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])))
    txt_file_btn.pack(pady=10, padx=10, side=tk.RIGHT)

    manual_var = tk.BooleanVar(value=False)
    manual_check = ttk.Checkbutton(root, text="Manually set number of requests", variable=manual_var)
    manual_check.pack(pady=5)
    manual_entry = ttk.Entry(root, width=10)
    manual_entry.pack(pady=5)

    start_btn = ttk.Button(root, text="Start", command=lambda: on_start(txt_file_entry, progress_var, status_label, manual_var, manual_entry))
    start_btn.pack(pady=10)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=300)
    progress_bar.pack(pady=10)

    status_label = ttk.Label(root, text="Ready to Process")
    status_label.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_gui()

