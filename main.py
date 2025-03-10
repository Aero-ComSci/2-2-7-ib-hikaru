import subprocess
import tkinter as tk
import tkinter.scrolledtext as tksc
from tkinter.filedialog import asksaveasfilename

def execute_command():
    global output_textbox, address_entry

    output_textbox.delete(1.0, tk.END)
    address_val = address_entry.get()
    
    if len(address_val) == 0:
        address_val = "::1"

    output_textbox.insert(tk.END, f"Pinging {address_val}...\n")
    output_textbox.update()

    process = subprocess.Popen(f"ping {address_val}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process_results, process_errors = process.communicate()

    output_textbox.insert(tk.END, process_results.decode('utf-8'))
    output_textbox.insert(tk.END, process_errors.decode('utf-8'))
