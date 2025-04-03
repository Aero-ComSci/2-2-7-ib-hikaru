import subprocess
import tkinter as tk
import tkinter.scrolledtext as tksc
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
import threading
import socket

def dns_query(domain):
    output_box.insert(tk.END, f"Performing DNS lookup for {domain}...\n\n")
    ip = socket.gethostbyname(domain)
    output_box.insert(tk.END, f"IP Address: {ip}\n")
    if domain.count('.') == 3 and all(part.isdigit() for part in domain.split('.')):
        hostname, _, ip_addrs = socket.gethostbyaddr(domain)
        output_box.insert(tk.END, f"Hostname: {hostname}\n")
        output_box.insert(tk.END, f"Aliases: {', '.join(ip_addrs)}\n")
    output_box.insert(tk.END, "\n")

def whois_query(domain):
    output_box.insert(tk.END, f"Performing Whois lookup for {domain}...\n\n")
    process = subprocess.Popen(["whois", domain], stdout=subprocess.PIPE, text=True)
    output, _ = process.communicate()
    output_box.insert(tk.END, output)

def show_arp_table():
    output_box.insert(tk.END, "Retrieving ARP Table...\n\n")
    process = subprocess.Popen(["arp", "-a"], stdout=subprocess.PIPE, text=True)
    output, _ = process.communicate()
    output_box.insert(tk.END, output)

def execute_shell_command(cmd, domain_or_ip):
    update_status("Executing command...")
    if cmd == "ping":
        ping_command(domain_or_ip)
    elif cmd == "traceroute":
        trace_route(domain_or_ip)
    elif cmd == "nslookup":
        dns_query(domain_or_ip)
    elif cmd == "netstat":
        show_netstat()
    elif cmd == "whois":
        whois_query(domain_or_ip)
    elif cmd == "arp":
        show_arp_table()
    output_box.insert(tk.END, "Command executed.\n")
    output_box.see(tk.END)
    save_btn.config(state=tk.NORMAL)
    clear_btn.config(state=tk.NORMAL)
    update_status("Command completed.")

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

def execute_command(event=None):
    command = command_selector.get()
    domain_or_ip = input_field.get().strip()
    if not domain_or_ip:
        if command in ["ping", "traceroute", "nslookup", "whois"]:
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
    Whois: Retrieves domain registration and ownership information.
    ARP Table: Displays IP to MAC address mappings in the local network.
    """
    messagebox.showinfo("Help", help_message)

def update_status(status_text):
    status_var.set(status_text)
    status_bar.update()

window = tk.Tk()
window.geometry("900x650")
window.configure(bg="#E9ECEF")

status_var = tk.StringVar(value="Ready")
status_bar = tk.Label(window, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#F8F9FA")
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

input_frame = tk.Frame(window, pady=20, bg="#E9ECEF")
input_frame.pack(fill=tk.X, padx=30)

input_label = tk.Label(input_frame, text="Enter Hostname/IP:", font=("Arial", 12), bg="#E9ECEF")
input_label.pack(side=tk.LEFT, padx=10)

input_field = tk.Entry(input_frame, font=("Arial", 12), width=40)
input_field.pack(side=tk.LEFT, fill=tk.X)
input_field.insert(0, "localhost")
input_field.bind("<Return>", execute_command)

command_frame = tk.Frame(window, pady=20, bg="#E9ECEF")
command_frame.pack(fill=tk.X, padx=30)

command_label = tk.Label(command_frame, text="Select Command:", font=("Arial", 12), bg="#E9ECEF")
command_label.pack(side=tk.LEFT, padx=10)

command_selector = tk.StringVar(value="ping")
commands = ["ping", "traceroute", "nslookup", "netstat", "whois", "arp"]
command_dropdown = tk.OptionMenu(command_frame, command_selector, *commands)
command_dropdown.pack(side=tk.LEFT, padx=10)

button_frame = tk.Frame(window, pady=20, bg="#E9ECEF")
button_frame.pack(fill=tk.X, padx=30)

save_btn = tk.Button(button_frame, text="Save Output", command=save_output)
save_btn.pack(side=tk.LEFT, padx=10)
save_btn.config(state=tk.DISABLED)

clear_btn = tk.Button(button_frame, text="Clear Output", command=clear_output)
clear_btn.pack(side=tk.LEFT, padx=10)
clear_btn.config(state=tk.DISABLED)

help_btn = tk.Button(button_frame, text="Help", command=show_help)
help_btn.pack(side=tk.LEFT, padx=10)

output_frame = tk.Frame(window, bg="#E9ECEF", padx=30, pady=20)
output_box = tksc.ScrolledText(output_frame, font=("Courier", 10), wrap=tk.WORD, height=15, bg="#343A40", fg="white")
output_box.pack(fill=tk.BOTH, expand=True)

window.mainloop()
