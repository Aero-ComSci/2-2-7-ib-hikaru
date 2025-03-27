import subprocess  
import tkinter as tk  
import tkinter.scrolledtext as tksc  
from tkinter import messagebox  
from tkinter.filedialog import asksaveasfilename  
import threading  
import socket  

# AI helped with this function to ensure proper DNS resolution.
def dns_query(domain):
    output_box.insert(tk.END, f"Performing DNS lookup for {domain}...\n\n")
    ip = socket.gethostbyname(domain) 
    output_box.insert(tk.END, f"IP Address: {ip}\n")
    if domain.count('.') == 3 and all(part.isdigit() for part in domain.split('.')):
        hostname, _, ip_addrs = socket.gethostbyaddr(domain)
        output_box.insert(tk.END, f"Hostname: {hostname}\n")
        output_box.insert(tk.END, f"Aliases: {', '.join(ip_addrs)}\n")
    output_box.insert(tk.END, "\n")

def execute_shell_command(cmd, domain_or_ip):
    if cmd == "ping":
        ping_command(domain_or_ip)
    elif cmd == "traceroute":
        trace_route(domain_or_ip)
    elif cmd == "nslookup":
        dns_query(domain_or_ip)
    elif cmd == "netstat":
        show_netstat()
    output_box.insert(tk.END, "Command executed.\n")
    output_box.see(tk.END)
    save_btn.config(state=tk.NORMAL)
    clear_btn.config(state=tk.NORMAL)

# AI helped structure this function to handle Windows ping commands properly
def ping_command(target):
    process = subprocess.Popen(["ping", "-n", "4", target], stdout=subprocess.PIPE, text=True)
    output, _ = process.communicate()
    output_box.insert(tk.END, output)

def trace_route(target):
    process = subprocess.Popen(["tracert", target], stdout=subprocess.PIPE, text=True)
    output, _ = process.communicate()
    output_box.insert(tk.END, output)

def show_netstat():
    process = subprocess.Popen(["netstat", "-an"], stdout=subprocess.PIPE, text=True)
    output, _ = process.communicate()
    output_box.insert(tk.END, output)

# AI helped structure this function using threading as Mr. Baez demonstrated in class
def execute_command(event=None):
    command = command_selector.get()
    domain_or_ip = input_field.get().strip()
    if not domain_or_ip:
        if command in ["ping", "traceroute", "nslookup"]:
            domain_or_ip = "localhost"
    output_box.delete(1.0, tk.END)
    save_btn.config(state=tk.DISABLED)
    clear_btn.config(state=tk.DISABLED)
    threading.Thread(target=execute_shell_command, args=(command, domain_or_ip), daemon=True).start()
    output_frame.pack(fill=tk.BOTH, expand=True)

def save_output():
    file_name = asksaveasfilename(defaultextension='.txt', filetypes=[('Text files', '*.txt')])
    if file_name:
        with open(file_name, 'w') as file:
            file.write(output_box.get(1.0, tk.END))
        messagebox.showinfo("Success", f"File saved as {file_name}")

def clear_output():
    output_box.delete(1.0, tk.END)

def show_help():
    help_message = """
    Ping: Tests the connectivity to a target host and measures round trip time.
    Traceroute: Displays the route packets take to a network host.
    Nslookup: Queries DNS records to get IP addresses of a domain.
    Netstat: Shows network connections, routing tables, and interface statistics.
    
    For usage, input a domain name or IP address and select a command to run.
    """
    #Used AI for the wording to make clear instructions
    messagebox.showinfo("Help", help_message)

window = tk.Tk()
window.geometry("900x600")
window.configure(bg="#E9ECEF")

input_frame = tk.Frame(window, pady=20, bg="#E9ECEF")
input_frame.pack(fill=tk.X, padx=30)

input_label = tk.Label(input_frame, text="Enter Hostname/IP:", font=("Arial", 12), bg="#E9ECEF")
input_label.pack(side=tk.LEFT, padx=10)

input_field = tk.Entry(input_frame, font=("Arial", 12), width=40)
input_field.pack(side=tk.LEFT, fill=tk.X)
input_field.insert(0, "localhost")
input_field.bind("<Return>", execute_command)  # Bind Enter key to trigger command execution

command_frame = tk.Frame(window, pady=20, bg="#E9ECEF")
command_frame.pack(fill=tk.X, padx=30)

command_label = tk.Label(command_frame, text="Select Command:", font=("Arial", 12), bg="#E9ECEF")
command_label.pack(side=tk.LEFT, padx=10)

# I used the drop bar to change up GUI to look diff
command_selector = tk.StringVar(value="ping")
commands = ["ping", "traceroute", "nslookup", "netstat"]

command_dropdown = tk.OptionMenu(command_frame, command_selector, *commands)
command_dropdown.pack(side=tk.LEFT, padx=10)
command_selector.trace_add("write", lambda *args: execute_command()) #was running into an error with the selector had to use some outside help to debug it cuz it wouldn't run when the option is chosen on the selectr
button_frame = tk.Frame(window, pady=20, bg="#E9ECEF")
button_frame.pack(fill=tk.X, padx=30)

output_frame = tk.Frame(window, bg="#E9ECEF", padx=30, pady=20)
output_box = tksc.ScrolledText(output_frame, font=("Courier", 10), wrap=tk.WORD, height=15, bg="#343A40", fg="white")
output_box.pack(fill=tk.BOTH, expand=True)

window.mainloop()
