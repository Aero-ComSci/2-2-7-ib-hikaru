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

def save_output():
    filename = asksaveasfilename(defaultextension='.txt', filetypes=(('Text files', '*.txt'), ('Python files', '*.py *.pyw'), ('All files', '*.*')))
    if filename:
        with open(filename, mode='w') as file:
            text_to_save = output_textbox.get("1.0", tk.END)
            file.write(text_to_save)

app = tk.Tk()
app.title("Ping URL Checker")

urlf = tk.Frame(app, pady=10, bg="black")
urlf.pack()

url = tk.Label(urlf, text="Enter a URL of interest: ", compound="center", font=("Times New Roman", 14), fg="mediumpurple3", bg="black")
url.pack(side=tk.LEFT)
address_entry = tk.Entry(urlf, font=("Times New Roman", 14))
address_entry.pack(side=tk.LEFT)

command_frame = tk.Frame(app, bg="black")
command_frame.pack()

ping_button = tk.Button(command_frame, text="Check to see if a URL is up and active", command=execute_command, compound="center", font=("Times New Roman", 12), bd=0, relief="flat", cursor="heart", bg="black", activebackground="gray")
ping_button.pack()

output_textbox = tksc.ScrolledText(command_frame, height=10, width=100)
output_textbox.pack()

save_button = tk.Button(command_frame, text="Save Output", command=save_output, font=("Times New Roman", 12), bd=0, relief="flat", cursor="heart", bg="black", activebackground="gray")
save_button.pack()

app.mainloop()
