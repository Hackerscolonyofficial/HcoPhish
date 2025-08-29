#!/usr/bin/env python3
"""
HCO PHISHING TOOL
By Azhar (Hackers Colony)
Educational Purpose Only
"""

import os
import time
import threading
from flask import Flask, render_template_string

app = Flask(__name__)

# ---------------- HTML Demo -----------------
html_template = """
<!DOCTYPE html>
<html>
<head>
  <title>Awareness Demo - HCO</title>
  <style>
    body { font-family: Arial, sans-serif; text-align: center; background: #111; color: #0f0; }
    h1 { color: red; }
    button {
      background: #0f0; color: #111; padding: 15px 30px;
      font-size: 18px; border: none; border-radius: 10px; cursor: pointer;
    }
    button:hover { background: yellow; }
  </style>
</head>
<body>
  <h1>🚨 HCO Awareness Demo 🚨</h1>
  <p>This is only for educational / awareness purpose.</p>
  <button onclick="downloadFile()">Download APK</button>

  <script>
    function downloadFile(){
      alert("Awareness Only! No real file here.");
    }
  </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html_template)

# ---------------- Cloudflare Tunnel -----------------
def start_cloudflare():
    print("\n[~] Starting Cloudflare Tunnel...\n")
    os.system("cloudflared tunnel --url http://127.0.0.1:5000 --no-autoupdate")

# ---------------- Main -----------------
if __name__ == "__main__":
    threading.Thread(target=start_cloudflare, daemon=True).start()
    print("[+] Flask server starting...\n")
    app.run(host="0.0.0.0", port=5000)
