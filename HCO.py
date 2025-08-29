#!/usr/bin/env python3
"""
HCO Awareness Demo Tool
By Azhar (Hackers Colony)
Educational Purpose Only
"""

import os
import time
import threading
import webbrowser
from flask import Flask, render_template_string, redirect, request

app = Flask(__name__)

# ---------------- HTML Template -----------------
html_template = """
<!DOCTYPE html>
<html>
<head>
  <title>HCO Awareness Demo - Advanced</title>
  <style>
    :root {
      --primary: #0f0;
      --secondary: #00f;
      --accent: #ff0;
      --dark: #111;
      --light: #eee;
    }
    
    body { 
      font-family: 'Arial', sans-serif; 
      text-align: center; 
      background: var(--dark); 
      color: var(--light);
      margin: 0;
      padding: 20px;
    }
    
    .container {
      max-width: 900px;
      margin: 0 auto;
      padding: 20px;
    }
    
    .header {
      margin-bottom: 30px;
    }
    
    h1 {
      color: var(--primary);
      font-size: 2.5em;
      margin-bottom: 10px;
      text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
    }
    
    .blue-box {
      background-color: var(--secondary);
      padding: 20px;
      border-radius: 10px;
      margin: 20px 0;
      box-shadow: 0 0 15px rgba(0, 0, 255, 0.5);
    }
    
    .blue-box h2 {
      color: white;
      margin-top: 0;
    }
    
    .button-group {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 15px;
      margin: 25px 0;
    }
    
    button {
      background: var(--primary);
      color: var(--dark);
      padding: 15px 30px;
      font-size: 18px;
      border: none;
      border-radius: 10px;
      cursor: pointer;
      transition: all 0.3s ease;
      font-weight: bold;
      min-width: 200px;
    }
    
    button:hover {
      background: var(--accent);
      transform: translateY(-3px);
      box-shadow: 0 5px 15px rgba(255, 255, 0, 0.4);
    }
    
    .feature-section {
      background: rgba(0, 0, 0, 0.3);
      padding: 20px;
      border-radius: 10px;
      margin: 20px 0;
      text-align: left;
    }
    
    .feature-section h3 {
      color: var(--primary);
      border-bottom: 1px solid var(--primary);
      padding-bottom: 10px;
    }
    
    .footer {
      margin-top: 40px;
      color: #888;
      font-size: 0.9em;
    }
    
    .countdown {
      font-size: 1.5em;
      color: var(--accent);
      margin: 20px 0;
    }
    
    .hidden-content {
      display: none;
      background: rgba(0, 255, 0, 0.1);
      padding: 20px;
      border-radius: 10px;
      margin: 20px 0;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>HCO Awareness Demo</h1>
      <p>Advanced cybersecurity awareness tool for educational purposes only</p>
    </div>
    
    <div class="blue-box">
      <h2>HCO Phish by Azhar</h2>
    </div>
    
    <div class="button-group">
      <button onclick="downloadFile()">Download APK</button>
      <button onclick="showHiddenContent()">Show Hidden Content</button>
      <button onclick="startCountdown()">Unlock Tool</button>
      <button onclick="simulateAttack()">Simulate Attack</button>
      <button onclick="showInfo()">Information</button>
    </div>
    
    <div id="countdown" class="countdown"></div>
    
    <div id="hiddenContent" class="hidden-content">
      <h3>Hidden Content Unlocked!</h3>
      <p>This demonstrates how seemingly hidden content can be revealed with simple interactions.</p>
      <p>In real phishing attempts, this technique might be used to create a false sense of security.</p>
    </div>
    
    <div class="feature-section">
      <h3>About This Demo</h3>
      <p>This tool demonstrates various techniques used in phishing awareness campaigns:</p>
      <ul>
        <li>Social engineering tactics</li>
        <li>Fake download buttons</li>
        <li>Countdown timers creating false urgency</li>
        <li>Hidden content revelation</li>
        <li>Simulated attack scenarios</li>
      </ul>
    </div>
    
    <div class="feature-section">
      <h3>Cybersecurity Best Practices</h3>
      <p>Always verify the source of any application before downloading:</p>
      <ul>
        <li>Check digital signatures when available</li>
        <li>Download only from official app stores or trusted sources</li>
        <li>Keep your security software updated</li>
        <li>Be wary of urgent requests for action</li>
        <li>Educate yourself on common phishing techniques</li>
      </ul>
    </div>
    
    <div class="footer">
      <p>For educational purposes only | Created by Azhar (Hackers Colony) | 2023</p>
    </div>
  </div>

  <script>
    function downloadFile() {
      alert("Awareness Alert: In a real scenario, this would download a potentially harmful file. Always verify sources before downloading!");
    }
    
    function showHiddenContent() {
      const content = document.getElementById('hiddenContent');
      content.style.display = content.style.display === 'none' ? 'block' : 'none';
    }
    
    function startCountdown() {
      // Redirect to YouTube first
      window.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ', '_blank');
      
      // Start countdown
      let timeLeft = 10;
      const countdownElement = document.getElementById('countdown');
      countdownElement.style.display = 'block';
      
      const countdownInterval = setInterval(() => {
        countdownElement.innerHTML = `Tool unlocks in: ${timeLeft} seconds`;
        timeLeft--;
        
        if (timeLeft < 0) {
          clearInterval(countdownInterval);
          countdownElement.innerHTML = "Tool Unlocked!";
          // Here you could enable actual functionality
        }
      }, 1000);
    }
    
    function simulateAttack() {
      alert("Simulation: This demonstrates how a phishing attempt might try to mimic legitimate system warnings to trick users.");
      
      // Create a fake system alert style popup
      const fakeAlert = document.createElement('div');
      fakeAlert.style = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
      `;
      
      fakeAlert.innerHTML = `
        <div style="
          background: linear-gradient(to bottom, #ff3333, #990000);
          padding: 30px;
          border-radius: 10px;
          color: white;
          text-align: center;
          width: 80%;
          max-width: 500px;
          box-shadow: 0 0 20px red;
        ">
          <h2 style="margin-top: 0;">⚠️ SECURITY WARNING ⚠️</h2>
          <p>Your system has been compromised!</p>
          <p>Immediate action required to prevent data loss.</p>
          <button onclick="this.parentElement.parentElement.remove()" style="
            background: white;
            color: red;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            margin-top: 20px;
            font-weight: bold;
            cursor: pointer;
          ">Dismiss</button>
        </div>
      `;
      
      document.body.appendChild(fakeAlert);
    }
    
    function showInfo() {
      alert("This is an educational tool created to demonstrate phishing techniques and raise cybersecurity awareness. No actual malicious code is included in this demonstration.");
    }
  </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html_template)

@app.route("/unlock")
def unlock():
    # Redirect to YouTube first
    time.sleep(2)  # Short delay before redirecting back
    return redirect("/")

# ---------------- Cloudflare Tunnel -----------------
def start_cloudflare():
    print("\n[~] Starting Cloudflare Tunnel...\n")
    os.system("cloudflared tunnel --url http://127.0.0.1:5000 --no-autoupdate")

# ---------------- Main -----------------
if __name__ == "__main__":
    # Start Cloudflare tunnel in a separate thread if needed
    # threading.Thread(target=start_cloudflare, daemon=True).start()
    
    print("[+] Enhanced HCO Awareness Demo starting...")
    print("[+] Educational purpose only")
    print("[+] Created by Azhar (Hackers Colony)\n")
    
    app.run(host="0.0.0.0", port=5000, debug=True)
