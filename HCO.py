#!/usr/bin/env python3
"""
HCO Phish Tool by Azhar
For educational purposes only
"""

import os
import time
import sys
import subprocess
import threading
from flask import Flask, render_template_string, redirect

# Check if Flask is installed, install if not
try:
    from flask import Flask, render_template_string, redirect
except ImportError:
    print("Installing Flask...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask, render_template_string, redirect

# Color codes for terminal
class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HCO Tool</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Courier New', monospace;
        }
        
        body {
            background: #000;
            color: #0f0;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
            background-image: radial-gradient(#002200, #000);
        }
        
        .container {
            max-width: 600px;
            width: 100%;
            background: rgba(0, 0, 0, 0.8);
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 0 20px #0f0;
            text-align: center;
            border: 1px solid #0f0;
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 20px;
            color: #0f0;
            text-shadow: 0 0 10px #0f0;
        }
        
        .logo {
            font-size: 3.5rem;
            font-weight: bold;
            margin-bottom: 10px;
            color: #f00;
            text-shadow: 0 0 10px #f00;
        }
        
        .countdown {
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background: rgba(0, 255, 0, 0.1);
            border-radius: 15px;
            border: 1px solid #0f0;
        }
        
        .timer {
            font-size: 3rem;
            font-weight: bold;
            color: #f00;
            text-shadow: 0 0 10px #f00;
            margin: 20px 0;
        }
        
        .button {
            background: #00f;
            border: none;
            color: white;
            padding: 15px 30px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 18px;
            margin: 20px 0;
            cursor: pointer;
            border-radius: 5px;
            transition: all 0.3s ease;
            border: 1px solid #00f;
        }
        
        .button:hover {
            background: #007;
            box-shadow: 0 0 15px #00f;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            color: #0f0;
            font-size: 0.9rem;
        }
        
        .hidden {
            display: none;
        }
        
        .options {
            text-align: left;
            margin: 20px 0;
        }
        
        .option-item {
            padding: 10px;
            margin: 5px 0;
            background: rgba(0, 0, 255, 0.1);
            border-radius: 5px;
            border-left: 3px solid #00f;
        }
        
        .author {
            color: #f00;
            font-weight: bold;
            margin: 20px 0;
            text-shadow: 0 0 5px #f00;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">HCO</div>
        <h1>Phish Tool</h1>
        
        <div id="subscribeSection">
            <p>Tool locked 🔐 To unlock subscribe to our YouTube channel</p>
            
            <a href="https://www.youtube.com" target="_blank" class="button">Subscribe on YouTube</a>
            
            <div style="margin-top: 30px;">
                <button class="button" onclick="verifySubscription()">I've Subscribed</button>
            </div>
        </div>
        
        <div id="countdownSection" class="hidden">
            <div class="countdown">
                <p>Redirecting to YouTube in:</p>
                <div class="timer" id="timer">10</div>
            </div>
        </div>
        
        <div id="unlockSection" class="hidden">
            <div class="author">HCO Phish by Azhar</div>
            
            <div class="options">
                <div class="option-item">1. Instagram</div>
                <div class="option-item">2. Facebook</div>
                <div class="option-item">3. Gmail</div>
                <div class="option-item">4. YouTube</div>
                <div class="option-item">5. Free Fire</div>
                <div class="option-item">6. PUBG</div>
                <div class="option-item">7. BGMI</div>
                <div class="option-item">8. Threads</div>
                <div class="option-item">9. Snapchat</div>
                <div class="option-item">10. Yahoo</div>
            </div>
            
            <div class="footer">
                <p>For educational purposes only</p>
            </div>
        </div>
    </div>

    <script>
        function verifySubscription() {
            // Hide subscribe section, show countdown
            document.getElementById('subscribeSection').classList.add('hidden');
            document.getElementById('countdownSection').classList.remove('hidden');
            
            // Start countdown from 10
            let count = 10;
            const timerElement = document.getElementById('timer');
            
            const countdownInterval = setInterval(() => {
                timerElement.textContent = count;
                
                if (count === 0) {
                    clearInterval(countdownInterval);
                    // Redirect to YouTube
                    window.location.href = 'https://www.youtube.com';
                    // After redirect, show unlock section when coming back
                    setTimeout(() => {
                        window.location.href = window.location.origin + '/unlock';
                    }, 5000);
                }
                
                count--;
            }, 1000);
        }
        
        // Check if we're on the unlock page
        if (window.location.pathname === '/unlock') {
            document.getElementById('subscribeSection').classList.add('hidden');
            document.getElementById('countdownSection').classList.add('hidden');
            document.getElementById('unlockSection').classList.remove('hidden');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/unlock')
def unlock():
    return render_template_string(HTML_TEMPLATE)

@app.route('/youtube')
def youtube_redirect():
    return redirect("https://www.youtube.com")

def print_banner():
    os.system('clear')
    print(f"{colors.RED}{colors.BOLD}")
    print("╔══════════════════════════════════════════════════╗")
    print("║                HCO Phish Tool                   ║")
    print("║                 by Azhar                        ║")
    print("╚══════════════════════════════════════════════════╝")
    print(f"{colors.END}")
    print(f"{colors.RED}Tool locked 🔐 To unlock subscribe our YouTube channel{colors.END}")
    print()

def countdown():
    for i in range(9, 0, -1):
        print(f"{colors.RED}Redirecting to YouTube in: {colors.YELLOW}{i}{colors.END}", end='\r')
        time.sleep(1)
    print()
    
    # Open YouTube in browser
    print(f"{colors.GREEN}Redirecting to YouTube...{colors.END}")
    time.sleep(2)
    
    # Simulate coming back
    print(f"{colors.CYAN}Welcome back! Tool unlocked.{colors.END}")
    time.sleep(1)
    
    # Show options
    print(f"\n{colors.RED}HCO Phish by Azhar{colors.END}")
    print(f"{colors.YELLOW}Available options:{colors.END}")
    print(f"{colors.GREEN}1. Instagram{colors.END}")
    print(f"{colors.GREEN}2. Facebook{colors.END}")
    print(f"{colors.GREEN}3. Gmail{colors.END}")
    print(f"{colors.GREEN}4. YouTube{colors.END}")
    print(f"{colors.GREEN}5. Free Fire{colors.END}")
    print(f"{colors.GREEN}6. PUBG{colors.END}")
    print(f"{colors.GREEN}7. BGMI{colors.END}")
    print(f"{colors.GREEN}8. Threads{colors.END}")
    print(f"{colors.GREEN}9. Snapchat{colors.END}")
    print(f"{colors.GREEN}10. Yahoo{colors.END}")
    print(f"\n{colors.CYAN}Select an option (1-10): {colors.END}", end='')

def run_flask():
    print(f"{colors.BLUE}\nWeb server starting on http://127.0.0.1:5000{colors.END}")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def main():
    print_banner()
    
    # Wait for user to press enter
    input(f"{colors.YELLOW}Press Enter after subscribing...{colors.END}")
    
    # Start countdown
    countdown()
    
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{colors.RED}Exiting...{colors.END}")
        sys.exit(0)

if __name__ == '__main__':
    main()
