#!/usr/bin/env python3
"""
Enhanced HCO Phishing Awareness Demo with Cloudflare Integration
Beautiful UI with countdown unlock message and color effects
For educational purposes only
"""

import os
import sys
import time
import threading
from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime, timedelta

# Initialize Flask app
app = Flask(__name__)

# Cloudflare simulation
class CloudflareSimulator:
    def __init__(self):
        self.enabled = True
        self.protection_level = "High"
        self.under_attack_mode = False
    
    def verify_request(self, request):
        # Simulate Cloudflare security check
        return True
    
    def challenge_page(self):
        # Generate a Cloudflare challenge page
        current_time = datetime.now().strftime("%Y-%b-%d %H:%M:%S UTC")
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Checking your browser before accessing the site</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; padding-top: 50px; background: #f6f6f6; }}
                .container {{ width: 650px; margin: 0 auto; background: white; padding: 30px; border-radius: 4px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .logo {{ font-weight: bold; font-size: 24px; color: #ff8800; margin-bottom: 20px; }}
                .message {{ font-size: 18px; margin: 20px 0; }}
                .progress {{ height: 20px; background: #e0e0e0; border-radius: 10px; overflow: hidden; margin: 30px 0; }}
                .progress-bar {{ height: 100%; background: #ff8800; width: 0%; transition: width 5s ease-in-out; }}
                .cf-footer {{ margin-top: 30px; font-size: 14px; color: #777; }}
            </style>
            <script>
                window.onload = function() {{
                    var bar = document.getElementById('progress-bar');
                    bar.style.width = '100%';
                    setTimeout(function() {{ window.location.href = '/'; }}, 5000);
                }};
            </script>
        </head>
        <body>
            <div class="container">
                <div class="logo">CLOUDFLARE</div>
                <div class="message">Checking your browser before accessing {request.host}</div>
                <div class="progress">
                    <div id="progress-bar" class="progress-bar"></div>
                </div>
                <div class="message">Verifying your browser connection...</div>
                <div class="cf-footer">
                    {current_time} | <strong>Performance &amp; Security by Cloudflare</strong>
                </div>
            </div>
        </body>
        </html>
        """

# Global variables
cloudflare = CloudflareSimulator()
countdown_time = 60  # seconds
start_time = datetime.now()
unlock_time = start_time + timedelta(seconds=countdown_time)

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
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            width: 100%;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            margin-top: 20px;
        }
        
        header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #ff8a00, #e52e71);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }
        
        h2 {
            font-size: 1.8rem;
            margin: 20px 0;
            color: #ff8a00;
        }
        
        .subtitle {
            font-size: 1.2rem;
            color: #aaa;
            margin-bottom: 20px;
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
            font-size: 2.5rem;
            font-weight: bold;
            color: #ff8a00;
            text-shadow: 0 0 10px rgba(255, 138, 0, 0.5);
        }
        
        .unlock-message {
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background: rgba(46, 204, 113, 0.1);
            border-radius: 15px;
            border: 1px solid rgba(46, 204, 113, 0.3);
            display: none;
        }
        
        .unlock-text {
            font-size: 1.5rem;
            color: #2ecc71;
            text-shadow: 0 0 10px rgba(46, 204, 113, 0.5);
        }
        
        .info-box {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .feature {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .feature:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.1);
        }
        
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 15px;
        }
        
        .warning {
            color: #e74c3c;
            font-weight: bold;
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            background: rgba(231, 76, 60, 0.1);
            border-radius: 10px;
            border: 1px solid rgba(231, 76, 60, 0.3);
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            color: #777;
            font-size: 0.9rem;
        }
        
        .button {
            background: linear-gradient(90deg, #ff8a00, #e52e71);
            border: none;
            color: white;
            padding: 15px 30px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 5px;
            cursor: pointer;
            border-radius: 50px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        .button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        }
        
        .cloudflare-badge {
            display: inline-block;
            background: #ff8800;
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            margin-left: 10px;
        }
        
        .logo {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #ff8a00, #e52e71);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .glow {
            text-shadow: 0 0 10px rgba(255, 138, 0, 0.7);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">HCO</div>
            <h1>Phishing Awareness Demo</h1>
            <p class="subtitle">Educational purpose only - Created by Azhar (Hackers Colony)</p>
        </header>
        
        <div class="countdown">
            <p class="countdown-text">System unlocking in:</p>
            <div class="timer" id="timer">01:00</div>
        </div>
        
        <div class="unlock-message" id="unlockMessage">
            <p class="unlock-text">🔓 System Unlocked! Access granted.</p>
        </div>
        
        <div class="warning">
            ⚠️ WARNING: This is a simulated environment for educational purposes only.
        </div>
        
        <div class="info-box">
            <h2>About This Demonstration</h2>
            <p>This tool is designed to demonstrate how phishing attacks work and how to recognize them. It includes simulated Cloudflare protection to show how security services can help protect against malicious sites.</p>
        </div>
        
        <h2>Features <span class="cloudflare-badge">Cloudflare Protected</span></h2>
        
        <div class="features">
            <div class="feature">
                <div class="feature-icon">🔒</div>
                <h3>Secure Connection</h3>
                <p>Simulated HTTPS encryption and secure data transmission</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🛡️</div>
                <h3>DDoS Protection</h3>
                <p>Cloudflare-integrated distributed denial-of-service protection</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🌐</div>
                <h3>Global CDN</h3>
                <p>Content delivery network for optimized performance</p>
            </div>
        </div>
        
        <div style="text-align: center;">
            <a href="/simulate" class="button">Simulate Phishing Attempt</a>
            <a href="/learn" class="button">Learn About Phishing</a>
        </div>
        
        <div class="footer">
            <p>This is a security awareness demonstration tool only.</p>
            <p>For educational use with proper authorization.</p>
        </div>
    </div>

    <script>
        // Countdown timer
        let timeLeft = {{ countdown_time }};
        const timerElement = document.getElementById('timer');
        const unlockMessage = document.getElementById('unlockMessage');
        
        function updateTimer() {
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            
            if (timeLeft > 0) {
                timeLeft--;
                setTimeout(updateTimer, 1000);
            } else {
                // Countdown complete
                timerElement.textContent = "00:00";
                unlockMessage.style.display = 'block';
                document.querySelector('.countdown').style.backgroundColor = 'rgba(46, 204, 113, 0.1)';
                document.querySelector('.countdown').style.borderColor = 'rgba(46, 204, 113, 0.3)';
                timerElement.style.color = '#2ecc71';
            }
        }
        
        // Start the countdown
        updateTimer();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    if cloudflare.enabled and cloudflare.under_attack_mode:
        return cloudflare.challenge_page()
    return render_template_string(HTML_TEMPLATE, countdown_time=countdown_time)

@app.route('/simulate')
def simulate():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simulated Login</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f0f0f0; padding: 50px; text-align: center; }
            .login-box { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); max-width: 400px; margin: 0 auto; }
            input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
            button { background: #ff8800; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
            .warning { color: #e74c3c; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h2>Login to your account</h2>
            <p style="color:#777;">This is a simulated phishing page for educational purposes</p>
            <input type="text" placeholder="Email or Username">
            <input type="password" placeholder="Password">
            <button>Sign In</button>
            <p class="warning">⚠️ This is a demonstration. Do not enter real credentials.</p>
        </div>
    </body>
    </html>
    """

@app.route('/learn')
def learn():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Learn About Phishing</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f0f0f0; padding: 50px; }
            .content { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); max-width: 800px; margin: 0 auto; }
            h2 { color: #ff8800; }
            .tip { background: #f9f9f9; padding: 15px; border-left: 4px solid #ff8800; margin: 15px 0; }
        </style>
    </head>
    <body>
        <div class="content">
            <h1>Phishing Awareness Tips</h1>
            
            <div class="tip">
                <h2>1. Check the URL</h2>
                <p>Always verify the website address before entering any credentials. Look for slight misspellings or different domains.</p>
            </div>
            
            <div class="tip">
                <h2>2. Look for HTTPS</h2>
                <p>Legitimate websites use HTTPS (look for the padlock icon in the address bar).</p>
            </div>
            
            <div class="tip">
                <h2>3. Don't Trust Urgent Messages</h2>
                <p>Phishing often uses urgency or threats to prompt quick action. Be skeptical of urgent requests for personal information.</p>
            </div>
            
            <div class="tip">
                <h2>4. Verify Unexpected Requests</h2>
                <p>If you receive an unexpected request for information, contact the company directly through official channels.</p>
            </div>
            
            <div class="tip">
                <h2>5. Use Multi-Factor Authentication</h2>
                <p>Even if your credentials are compromised, MFA can prevent unauthorized access.</p>
            </div>
            
            <p style="margin-top: 30px; text-align: center;">
                <a href="/">Return to Demo</a>
            </p>
        </div>
    </body>
    </html>
    """

def start_countdown():
    """Background thread to update the unlock time"""
    global unlock_time
    while True:
        time.sleep(1)
        # Update unlock time every second
        unlock_time = datetime.now() + timedelta(seconds=countdown_time)

if __name__ == '__main__':
    # Start countdown thread
    countdown_thread = threading.Thread(target=start_countdown, daemon=True)
    countdown_thread.start()
    
    # Print colorful startup message
    print("\033[1;35m")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                 HCO Phishing Awareness Demo                  ║")
    print("║                  with Cloudflare Integration                 ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print("\033[1;36m")
    print("[+] Enhanced HCO Awareness Demo starting...")
    print("[+] Educational purpose only")
    print("[+] Created by Azhar (Hackers Colony)")
    print("[+] Cloudflare simulation: \033[1;32mACTIVE\033[1;36m")
    print("[+] Countdown unlock: \033[1;32mENABLED\033[1;36m")
    print("\033[1;33m")
    print(f"[+] Server will be available at: http://127.0.0.1:5000")
    print(f"[+] Cloudflare challenge at: http://127.0.0.1:5000/cf-challenge")
    print("\033[0m")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
