
import subprocess
import tkinter as tk
import tkinter.scrolledtext as tksc
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
import threading
import platform
import socket


def dns_query(domain):
    output_box.insert(tk.END, f"Performing DNS lookup for {domain}...\n\n")
    try:
        ip = socket.gethostbyname(domain)
        output_box.insert(tk.END, f"IP Address: {ip}\n")
    except socket.gaierror:
        output_box.insert(tk.END, f"Failed to resolve domain: {domain}\n")
        return
    if domain.count('.') == 3 and all(part.isdigit() for part in domain.split('.')):
        try:
            hostname, _, ip_addrs = socket.gethostbyaddr(domain)
            output_box.insert(tk.END, f"Hostname: {hostname}\n")
            output_box.insert(tk.END, f"Aliases: {', '.join(ip_addrs)}\n")
        except socket.herror:
            output_box.insert(tk.END, "No hostname found for this IP.\n")
    output_box.insert(tk.END, "\n")


def execute_shell_command(cmd, domain_or_ip):
    try:
        if cmd == "ping":
            ping_command(domain_or_ip)
        elif cmd == "traceroute":
            trace_route(domain_or_ip)
        elif cmd == "nslookup":
            dns_query(domain_or_ip)
        elif cmd == "netstat":
            show_netstat()
    except Exception as e:
        output_box.insert(tk.END, f"Error: {str(e)}\n")
    output_box.insert(tk.END, "Command executed.\n")
    output_box.see(tk.END)
    run_btn.config(state=tk.NORMAL)
    save_btn.config(state=tk.NORMAL)
    clear_btn.config(state=tk.NORMAL)


def ping_command(target):
    if platform.system() == "Windows":
        process = subprocess.Popen(["ping", "-n", "4", target], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    else:
        process = subprocess.Popen(["ping", "-c", "4", target], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, errors = process.communicate()
    output_box.insert(tk.END, output)
    if errors:
        output_box.insert(tk.END, f"Errors:\n{errors}")


def trace_route(target):
    traceroute_cmd = "tracert" if platform.system() == "Windows" else "traceroute"
    process = subprocess.Popen([traceroute_cmd, target], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, errors = process.communicate()
    output_box.insert(tk.END, output)
    if errors:
        output_box.insert(tk.END, f"Errors:\n{errors}")


def show_netstat():
    netstat_command = ["netstat", "-an"]
    process = subprocess.Popen(netstat_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, errors = process.communicate()
    output_box.insert(tk.END, output)
    if errors:
        output_box.insert(tk.END, f"Errors:\n{errors}")


def execute_command():
    command = command_selector.get()
    domain_or_ip = input_field.get().strip()
    if not domain_or_ip:
        if command in ["ping", "traceroute", "nslookup"]:
            domain_or_ip = "localhost"
        else:
            domain_or_ip = ""
    if command in ["ping", "traceroute", "nslookup"] and not validate_domain(domain_or_ip):
        output_box.insert(tk.END, f"Could not resolve domain: {domain_or_ip}\n")
    else:
        output_box.delete(1.0, tk.END)
        run_btn.config(state=tk.DISABLED)
        save_btn.config(state=tk.DISABLED)
        clear_btn.config(state=tk.DISABLED)
        threading.Thread(target=execute_shell_command, args=(command, domain_or_ip), daemon=True).start()
        output_frame.pack(fill=tk.BOTH, expand=True)


def validate_domain(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False


def save_output():
    file_name = asksaveasfilename(defaultextension='.txt', filetypes=[('Text files', '*.txt')])
    if file_name:
        try:
            with open(file_name, 'w') as file:
                file.write(output_box.get(1.0, tk.END))
            messagebox.showinfo("Success", f"File saved as {file_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")


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
    messagebox.showinfo("Help", help_message)


window = tk.Tk()
window.title("Network Diagnostics Tool")
window.geometry("900x600")
window.configure(bg="#E9ECEF")

input_frame = tk.Frame(window, pady=20, bg="#E9ECEF")
input_frame.pack(fill=tk.X, padx=30)

input_label = tk.Label(input_frame, text="Enter Hostname/IP:", font=("Arial", 12), bg="#E9ECEF")
input_label.pack(side=tk.LEFT, padx=10)

input_field = tk.Entry(input_frame, font=("Arial", 12), width=40)
input_field.pack(side=tk.LEFT, fill=tk.X)
input_field.insert(0, "localhost")

command_frame = tk.Frame(window, pady=20, bg="#E9ECEF")
command_frame.pack(fill=tk.X, padx=30)

command_label = tk.Label(command_frame, text="Select Command:", font=("Arial", 12), bg="#E9ECEF")
command_label.pack(side=tk.LEFT, padx=10)

command_selector = tk.StringVar(value="ping")
commands = ["ping", "traceroute", "nslookup", "netstat"]

for cmd in commands:
    checkbutton = tk.Checkbutton(command_frame, text=cmd, variable=command_selector, onvalue=cmd, offvalue="", font=("Arial", 11), bg="#E9ECEF")
    checkbutton.pack(side=tk.LEFT, padx=10)

button_frame = tk.Frame(window, pady=20, bg="#E9ECEF")
button_frame.pack(fill=tk.X, padx=30)

run_btn = tk.Button(button_frame, text="Run", command=execute_command, font=("Arial", 12, "bold"), bg="#28A745", fg="white", padx=15, pady=10)
run_btn.pack(side=tk.LEFT, padx=12)

save_btn = tk.Button(button_frame, text="Save", command=save_output, font=("Arial", 12), bg="#007BFF", fg="white", padx=15, pady=10)
save_btn.pack(side=tk.LEFT, padx=12)

clear_btn = tk.Button(button_frame, text="Clear", command=clear_output, font=("Arial", 12), bg="#DC3545", fg="white", padx=15, pady=10)
clear_btn.pack(side=tk.LEFT, padx=12)

help_btn = tk.Button(button_frame, text="Help", command=show_help, font=("Arial", 12), bg="#6C757D", fg="white", padx=15, pady=10)
help_btn.pack(side=tk.LEFT, padx=12)

output_frame = tk.Frame(window, bg="#E9ECEF", padx=30, pady=20)
output_box = tksc.ScrolledText(output_frame, font=("Courier", 10), wrap=tk.WORD, height=15, bg="#343A40", fg="white")
output_box.pack(fill=tk.BOTH, expand=True)

status_bar = tk.Label(window, text="Ready", bg="#6C757D", fg="white", font=("Arial", 10), relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

window.mainloop()



