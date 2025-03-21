import subprocess
import tkinter as tk
import tkinter.scrolledtext as tksc
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
import threading
import platform
import socket

#Used PLTW and a lil bit of stack overflow for info about this and how to use it
def execute_command_thread(command, url_val):
    try:
        if command == "ping":
            if platform.system() == "Windows":
                process = subprocess.Popen(
                    ["ping", "-n", "4", url_val],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            else:
                process = subprocess.Popen(
                    ["ping", "-c", "4", url_val],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            cmd_results, cmd_errors = process.communicate()
            command_textbox.insert(tk.END, cmd_results)
            if cmd_errors:
                command_textbox.insert(tk.END, f"\nErrors:\n{cmd_errors}")
                
        elif command == "tracert" or command == "traceroute":
            cmd = "tracert" if platform.system() == "Windows" else "traceroute"
            process = subprocess.Popen(
                [cmd, url_val],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            cmd_results, cmd_errors = process.communicate()
            command_textbox.insert(tk.END, cmd_results)
            if cmd_errors:
                command_textbox.insert(tk.END, f"\nErrors:\n{cmd_errors}")
                
        elif command == "nslookup":
            perform_dns_lookup(url_val)
                
        elif command == "netstat":
            if platform.system() == "Windows":
                process = subprocess.Popen(
                    ["netstat", "-an"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            else:
                process = subprocess.Popen(
                    ["netstat", "-an"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            cmd_results, cmd_errors = process.communicate()
            command_textbox.insert(tk.END, cmd_results)
            if cmd_errors:
                command_textbox.insert(tk.END, f"\nErrors:\n{cmd_errors}")
    except Exception as e:
        command_textbox.insert(tk.END, f"\nError executing {command}: {str(e)}\n")
    command_textbox.insert(tk.END, "\nCommand execution completed.\n")
    command_textbox.see(tk.END)
    run_button.config(state=tk.NORMAL)
    save_button.config(state=tk.NORMAL)
    clear_button.config(state=tk.NORMAL)

def perform_dns_lookup(domain):
    command_textbox.insert(tk.END, f"DNS lookup for: {domain}\n\n")
    
    # AI helped me with this - What I understood:
    # ChatGPT explained how to use socket to perform DNS lookups and handle both IP and hostname resolution.
    # It suggests using socket.gethostbyname and socket.gethostbyaddr for resolving IP addresses and getting host information.
    try:
        ip_address = socket.gethostbyname(domain)
        command_textbox.insert(tk.END, f"IP Address: {ip_address}\n\n")
    except socket.gaierror:
        command_textbox.insert(tk.END, f"Could not resolve hostname: {domain}\n\n")
        return
    
    if all(c.isdigit() or c == '.' for c in domain):
        try:
            hostname, aliaslist, ipaddrlist = socket.gethostbyaddr(domain)
            command_textbox.insert(tk.END, f"Hostname: {hostname}\n")
            if aliaslist:
                command_textbox.insert(tk.END, f"Aliases: {', '.join(aliaslist)}\n")
            if ipaddrlist:
                command_textbox.insert(tk.END, f"IP Addresses: {', '.join(ipaddrlist)}\n")
            command_textbox.insert(tk.END, "\n")
        except socket.herror:
            command_textbox.insert(tk.END, "Could not find hostname for this IP address\n\n")

def do_command():
    global command_textbox, url_entry
    selected_command = command_var.get()
    command_textbox.delete(1.0, tk.END)
    url_val = url_entry.get().strip()
    if len(url_val) == 0:
        if selected_command in ["ping", "tracert", "traceroute", "nslookup"]:
            url_val = "localhost"
        elif selected_command == "netstat":
            url_val = ""
    if selected_command in ["ping", "tracert", "traceroute", "nslookup"] and url_val != "localhost":
        try:
            socket.gethostbyname(url_val)
        except socket.gaierror:
            command_textbox.insert(tk.END, f"Warning: Could not resolve hostname '{url_val}'. Proceeding anyway.\n\n")
    command_textbox.insert(tk.END, f"Executing {selected_command} for {url_val if url_val else 'system'}\n")
    command_textbox.insert(tk.END, "Please wait...\n\n")
    command_textbox.see(tk.END)
    run_button.config(state=tk.DISABLED)
    save_button.config(state=tk.DISABLED)
    clear_button.config(state=tk.DISABLED)
    
    # AI helped me with this - What I understood:
    # ChatGPT suggested using threading to run commands without freezing the UI.
    # It helps run long commands like `ping` in the background while keeping the GUI responsive.
    thread = threading.Thread(target=execute_command_thread, args=(selected_command, url_val))
    thread.daemon = True
    thread.start()

def save_output():
    filename = asksaveasfilename(
        defaultextension='.txt',
        filetypes=(('Text files', '*.txt'), ('All files', '*.*'))
    )
    if filename:
        try:
            with open(filename, 'w') as file:
                text_to_save = command_textbox.get("1.0", tk.END)
                file.write(text_to_save)
            messagebox.showinfo("Save Successful", f"Output saved to {filename}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving file: {str(e)}")

def clear_output():
    command_textbox.delete(1.0, tk.END)

def show_help():
    help_text = """Network Tools Help:
Ping: Checks if a host is reachable and measures round-trip time.
Traceroute: Shows the path packets take to reach a host.
NSLookup: Performs DNS lookups to find IP addresses and domain information.
Netstat: Displays network connections and routing tables.

Enter a hostname or IP address in the input field and click the 'Run Command' button.
For Netstat, no input is required as it shows local connections.
The Save button allows you to save the output to a text file.
The Clear button clears the output display.

Note: For enhanced DNS lookup functionality, install the dnspython package:
pip install dnspython"""
    
    # AI helped me with this - What I understood:
    # ChatGPT generated the help text, providing a user-friendly guide for the application’s commands.
    # It breaks down the purpose of each command in simple terms, making it easier for users to navigate the app.
    messagebox.showinfo("Network Tools Help", help_text)

root = tk.Tk()
root.title("Network Tools GUI")
root.geometry("850x650")
root.configure(bg="#222222")

 # AI helped me with UI inspiration - What I understood:
# ChatGPT helped me design the layout and structure of the GUI using Tkinter.
# It suggested the use of frames, buttons, and scrolled text areas to organize the user interface logically.


frame_URL = tk.Frame(root, pady=10, bg="#333333")
frame_URL.pack(fill=tk.X, padx=20)

url_label = tk.Label(
    frame_URL,
    text="Enter hostname or IP address:",
    font=("Helvetica", 12),
    bg="#333333",
    fg="#FFFFFF"
)
url_label.pack(side=tk.LEFT, padx=(0, 10))

url_entry = tk.Entry(frame_URL, font=("Helvetica", 12), width=40)
url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
url_entry.insert(0, "localhost")

frame_command = tk.Frame(root, pady=10, bg="#333333")
frame_command.pack(fill=tk.X, padx=20)

command_label = tk.Label(
    frame_command,
    text="Select command:",
    font=("Helvetica", 12),
    bg="#333333",
    fg="#FFFFFF"
)
command_label.pack(side=tk.LEFT, padx=(0, 10))

command_var = tk.StringVar(root)
command_var.set("ping")
commands = ["ping", "tracert" if platform.system() == "Windows" else "traceroute", "nslookup", "netstat"]
for command in commands:
    rb = tk.Radiobutton(
        frame_command,
        text=command,
        variable=command_var,
        value=command,
        font=("Helvetica", 10),
        bg="#333333",
        fg="#FFFFFF",
        activebackground="#444444",
        activeforeground="#FFFFFF",
        selectcolor="#666666"
    )
    rb.pack(side=tk.LEFT, padx=10)

button_frame = tk.Frame(root, pady=10, bg="#333333")
button_frame.pack(fill=tk.X, padx=20)

run_button = tk.Button(
    button_frame,
    text="Run Command",
    command=do_command,
    font=("Helvetica", 10, "bold"),
    bg="#4CAF50",
    fg="#FFFFFF",
    padx=12,
    pady=6,
    relief=tk.RAISED,
    bd=2,
    activebackground="#45a049"
)
run_button.pack(side=tk.TOP, padx=10, pady=5)

save_button = tk.Button(
    button_frame,
    text="Save Output",
    command=save_output,
    font=("Helvetica", 10),
    bg="#2196F3",
    fg="#FFFFFF",
    padx=12,
    pady=6,
    relief=tk.RAISED,
    bd=2,
    activebackground="#1976D2"
)
save_button.pack(side=tk.TOP, padx=10, pady=5)

clear_button = tk.Button(
    button_frame,
    text="Clear Output",
    command=clear_output,
    font=("Helvetica", 10),
    bg="#f44336",
    fg="#FFFFFF",
    padx=12,
    pady=6,
    relief=tk.RAISED,
    bd=2,
    activebackground="#D32F2F"
)
clear_button.pack(side=tk.TOP, padx=10, pady=5)

help_button = tk.Button(
    button_frame,
    text="Help",
    command=show_help,
    font=("Helvetica", 10),
    bg="#9E9E9E",
    fg="#000000",
    padx=12,
    pady=6,
    relief=tk.RAISED,
    bd=2,
    activebackground="#757575"
)
help_button.pack(side=tk.TOP, padx=10, pady=5)

output_frame = tk.Frame(root, bg="#222222", padx=20, pady=10)
output_frame.pack(fill=tk.BOTH, expand=True)

command_textbox = tksc.ScrolledText(
    output_frame,
    font=("Consolas", 10),
    bg="#333333",
    fg="white",
    wrap=tk.WORD,
    bd=1,
    relief=tk.GROOVE
)
command_textbox.pack(fill=tk.BOTH, expand=True)

status_bar = tk.Label(
    root,
    text="Ready",
    bd=1,
    relief=tk.SUNKEN,
    anchor=tk.W,
    bg="#333333",
    font=("Helvetica", 9),
    fg="#FFFFFF"
)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

command_textbox.insert(tk.END, "Select a command and click 'Run Command' to begin.\n")

root.mainloop()
