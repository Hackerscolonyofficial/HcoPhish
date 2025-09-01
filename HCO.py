#!/usr/bin/env python3
"""
HCO Phish by Azhar
For educational purposes only
"""

from flask import Flask, render_template_string, request, redirect
import random

app = Flask(__name__)

# HTML Template with multiple service simulations
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Gateway</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: #f5f5f5;
            color: #333;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            max-width: 500px;
            width: 100%;
            background: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        
        .logo {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 20px;
            color: #1a73e8;
        }
        
        h1 {
            font-size: 1.5rem;
            margin-bottom: 20px;
            color: #202124;
        }
        
        .service-icon {
            font-size: 2.5rem;
            margin: 15px 0;
        }
        
        .form-group {
            margin-bottom: 20px;
            text-align: left;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #5f6368;
        }
        
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 12px;
            border: 1px solid #dadce0;
            border-radius: 4px;
            font-size: 16px;
            transition: border 0.2s;
        }
        
        input[type="text"]:focus,
        input[type="password"]:focus {
            border: 1px solid #1a73e8;
            outline: none;
        }
        
        .button {
            background: #1a73e8;
            border: none;
            color: white;
            padding: 12px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 20px 0;
            cursor: pointer;
            border-radius: 4px;
            transition: background 0.2s;
            width: 100%;
            font-weight: 500;
        }
        
        .button:hover {
            background: #1565c0;
        }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #5f6368;
            font-size: 0.8rem;
        }
        
        .service-selector {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
            margin: 20px 0;
        }
        
        .service-btn {
            padding: 10px 15px;
            background: #f1f3f4;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: background 0.2s;
        }
        
        .service-btn:hover {
            background: #e8eaed;
        }
        
        .hidden {
            display: none;
        }
        
        .security-notice {
            background: #fef7e0;
            padding: 15px;
            border-radius: 4px;
            margin: 20px 0;
            text-align: left;
            font-size: 0.9rem;
            border-left: 3px solid #fbbc04;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">Security Gateway</div>
        
        <div id="serviceSelection">
            <h1>Select a service to demonstrate</h1>
            
            <div class="service-selector">
                <button class="service-btn" onclick="selectService('gmail')">Gmail</button>
                <button class="service-btn" onclick="selectService('facebook')">Facebook</button>
                <button class="service-btn" onclick="selectService('instagram')">Instagram</button>
                <button class="service-btn" onclick="selectService('youtube')">YouTube</button>
                <button class="service-btn" onclick="selectService('pubg')">PUBG</button>
                <button class="service-btn" onclick="selectService('bgmi')">BGMI</button>
                <button class="service-btn" onclick="selectService('freefire')">Free Fire</button>
                <button class="service-btn" onclick="selectService('threads')">Threads</button>
                <button class="service-btn" onclick="selectService('yahoo')">Yahoo</button>
                <button class="service-btn" onclick="selectService('snapchat')">Snapchat</button>
            </div>
        </div>
        
        <div id="loginForm" class="hidden">
            <div class="service-icon" id="serviceIcon">📧</div>
            <h1 id="serviceTitle">Service Login</h1>
            
            <form id="demoForm" onsubmit="handleSubmit(event)">
                <div class="form-group">
                    <label for="username">Username or Email</label>
                    <input type="text" id="username" name="username" placeholder="Enter your username">
                </div>
                
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" placeholder="Enter your password">
                </div>
                
                <button type="submit" class="button">Sign in</button>
            </form>
            
            <div class="security-notice">
                <strong>Security Awareness:</strong> This is a demonstration page. In a real phishing attack, criminals create fake login pages to steal credentials. Always check the URL before entering your information.
            </div>
        </div>
        
        <div id="resultMessage" class="hidden">
            <div class="service-icon">✅</div>
            <h1>Security Demonstration Complete</h1>
            <p>This simulation shows how phishing attacks attempt to steal your credentials.</p>
            
            <div class="security-notice">
                <strong>How to protect yourself:</strong><br>
                1. Always check the website URL before logging in<br>
                2. Look for HTTPS and the lock icon in the address bar<br>
                3. Enable two-factor authentication on your accounts<br>
                4. Use unique passwords for different services<br>
                5. Be wary of unsolicited emails asking you to login
            </div>
            
            <button class="button" onclick="resetDemo()">Try Another Service</button>
        </div>
        
        <div class="footer">
            <p>HCO Security Awareness Demo | For educational purposes only</p>
        </div>
    </div>

    <script>
        let currentService = '';
        
        const serviceConfigs = {
            gmail: { icon: '📧', title: 'Gmail' },
            facebook: { icon: '👤', title: 'Facebook' },
            instagram: { icon: '📸', title: 'Instagram' },
            youtube: { icon: '📺', title: 'YouTube' },
            pubg: { icon: '🎮', title: 'PUBG Mobile' },
            bgmi: { icon: '🎯', title: 'Battlegrounds Mobile India' },
            freefire: { icon: '🔥', title: 'Garena Free Fire' },
            threads: { icon: '🧵', title: 'Threads' },
            yahoo: { icon: '📬', title: 'Yahoo Mail' },
            snapchat: { icon: '👻', title: 'Snapchat' }
        };
        
        function selectService(service) {
            currentService = service;
            const config = serviceConfigs[service];
            
            document.getElementById('serviceIcon').textContent = config.icon;
            document.getElementById('serviceTitle').textContent = config.title + ' Login';
            
            document.getElementById('serviceSelection').classList.add('hidden');
            document.getElementById('loginForm').classList.remove('hidden');
        }
        
        function handleSubmit(event) {
            event.preventDefault();
            
            // Simulate "processing" delay
            setTimeout(() => {
                document.getElementById('loginForm').classList.add('hidden');
                document.getElementById('resultMessage').classList.remove('hidden');
            }, 1000);
            
            return false;
        }
        
        function resetDemo() {
            document.getElementById('username').value = '';
            document.getElementById('password').value = '';
            
            document.getElementById('resultMessage').classList.add('hidden');
            document.getElementById('serviceSelection').classList.remove('hidden');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/auth', methods=['POST'])
def auth():
    # This endpoint doesn't actually store anything
    # For educational purposes only
    return redirect('/')

if __name__ == '__main__':
    print("\033[1;35m")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                 HCO Phish by Azhar.                                     ║")
    print("║               SIMULATION FOR EDUCATIONAL USE                            ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print("\033[1;36m")
    print("[+] Security Awareness Demo starting...")
    print("[+] Educational purpose only - No data is being collected")
    print("[+] Created for security awareness training")
    print("\033[1;33m")
    print(f"[+] Local: http://127.0.0.1:5000")
    print("[+] On other devices, use your computer's IP address instead of localhost")
    print("\033[0m")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)
