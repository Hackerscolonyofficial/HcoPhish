#!/usr/bin/env python3
"""
HCO Phishing Awareness Demo with YouTube Integration
For educational purposes only
"""

import time
import threading
from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime, timedelta

# Initialize Flask app
app = Flask(__name__)

# Global variables
countdown_time = 8  # seconds
start_time = datetime.now()
unlock_time = start_time + timedelta(seconds=countdown_time)
subscribed = False

# HTML Template with beautiful styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HCO Security Awareness</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: #fff;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            max-width: 600px;
            width: 100%;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            text-align: center;
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 20px;
            background: linear-gradient(90deg, #ff8a00, #e52e71);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }
        
        .logo {
            font-size: 3.5rem;
            font-weight: bold;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #ff8a00, #e52e71);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .subtitle {
            font-size: 1.2rem;
            color: #aaa;
            margin-bottom: 30px;
        }
        
        .countdown {
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background: rgba(255, 138, 0, 0.1);
            border-radius: 15px;
            border: 1px solid rgba(255, 138, 0, 0.3);
        }
        
        .countdown-text {
            font-size: 1.2rem;
            margin-bottom: 10px;
        }
        
        .timer {
            font-size: 3rem;
            font-weight: bold;
            color: #ff8a00;
            text-shadow: 0 0 10px rgba(255, 138, 0, 0.5);
            margin: 20px 0;
        }
        
        .unlock-message {
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background: rgba(46, 204, 113, 0.1);
            border-radius: 15px;
            border: 1px solid rgba(46, 204, 113, 0.3);
        }
        
        .unlock-text {
            font-size: 1.8rem;
            color: #2ecc71;
            text-shadow: 0 0 10px rgba(46, 204, 113, 0.5);
            margin-bottom: 20px;
        }
        
        .author {
            font-size: 1.5rem;
            color: #ff8a00;
            margin: 20px 0;
        }
        
        .cloudflare-link {
            display: block;
            margin: 30px 0;
            padding: 15px;
            background: rgba(255, 138, 0, 0.1);
            border-radius: 10px;
            border: 1px solid rgba(255, 138, 0, 0.3);
            text-decoration: none;
            color: #ff8a00;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .cloudflare-link:hover {
            background: rgba(255, 138, 0, 0.2);
            transform: translateY(-2px);
        }
        
        .button {
            background: linear-gradient(90deg, #ff8a00, #e52e71);
            border: none;
            color: white;
            padding: 15px 30px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 18px;
            margin: 20px 0;
            cursor: pointer;
            border-radius: 50px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        .button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            color: #777;
            font-size: 0.9rem;
        }
        
        .hidden {
            display: none;
        }
        
        .youtube-icon {
            font-size: 4rem;
            color: #ff0000;
            margin: 20px 0;
            animation: pulse 1.5s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        
        .instructions {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            text-align: left;
        }
        
        .instructions ol {
            padding-left: 20px;
            margin: 15px 0;
        }
        
        .instructions li {
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">HCO</div>
        <h1>Phishing Awareness Demo</h1>
        <p class="subtitle">Educational purpose only</p>
        
        <div id="subscribeSection">
            <div class="instructions">
                <h3>To unlock the tool:</h3>
                <ol>
                    <li>Subscribe to our YouTube channel</li>
                    <li>Return to this page</li>
                    <li>Click the verification button</li>
                </ol>
            </div>
            
            <div class="youtube-icon">▶️</div>
            
            <a href="https://www.youtube.com" target="_blank" class="button">Visit YouTube</a>
            
            <div style="margin-top: 30px;">
                <button class="button" onclick="verifySubscription()">I've Subscribed</button>
            </div>
        </div>
        
        <div id="countdownSection" class="hidden">
            <div class="countdown">
                <p class="countdown-text">Unlocking tool in:</p>
                <div class="timer" id="timer">8</div>
            </div>
        </div>
        
        <div id="unlockSection" class="hidden">
            <div class="unlock-message">
                <p class="unlock-text">🔓 Tool Unlocked!</p>
                <p class="author">HCO Phish by Azhar</p>
            </div>
            
            <a href="https://cloudflare.com" target="_blank" class="cloudflare-link">
                🔗 Cloudflare Protected Link
            </a>
            
            <div class="footer">
                <p>This is a security awareness demonstration tool only.</p>
                <p>For educational use with proper authorization.</p>
            </div>
        </div>
    </div>

    <script>
        function verifySubscription() {
            // Hide subscribe section, show countdown
            document.getElementById('subscribeSection').classList.add('hidden');
            document.getElementById('countdownSection').classList.remove('hidden');
            
            // Start countdown from 8
            let count = 8;
            const timerElement = document.getElementById('timer');
            
            const countdownInterval = setInterval(() => {
                timerElement.textContent = count;
                
                if (count === 0) {
                    clearInterval(countdownInterval);
                    // Show unlock section
                    document.getElementById('countdownSection').classList.add('hidden');
                    document.getElementById('unlockSection').classList.remove('hidden');
                }
                
                count--;
            }, 1000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/youtube')
def youtube_redirect():
    # Simulate redirect to YouTube
    return redirect("https://www.youtube.com")

if __name__ == '__main__':
    # Print startup message
    print("\033[1;35m")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                                 HCO Phish                               ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print("\033[1;36m")
    print("[+] Enhanced HCO Awareness starting...")
    print("[+] Educational purpose only")
    print("[+] Created by Azhar (Hackers Colony)")
    print("\033[1;33m")
    print(f"[+] Server available at: http://127.0.0.1:5000")
    print("\033[0m")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)
