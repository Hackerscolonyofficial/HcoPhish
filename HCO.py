#!/usr/bin/env python3
# HCO Phishing by Azhar — Awareness Lab (single file, SAFE)
# Usage:
#   python HCO.py
#   python HCO.py --tunnel
#
# Notes:
# - This is an educational simulator. It NEVER stores or transmits passwords.
# - Inputs are printed to your terminal for teaching, with password masked.
# - Use only in a controlled lab with informed consent.

import argparse
import os
import re
import signal
import subprocess
import sys
import threading
import time
from textwrap import dedent

# -------- Colors (no external deps) --------
RED   = "\033[1;31m"
GRN   = "\033[1;32m"
YEL   = "\033[1;33m"
BLU   = "\033[1;34m"
CYN   = "\033[1;36m"
WHT   = "\033[1;37m"
RST   = "\033[0m"

def cprint(color, msg):
    print(color + msg + RST)

# -------- Try Flask (auto-install if missing) --------
try:
    from flask import Flask, render_template_string, request, redirect
except Exception:
    cprint(YEL, "[!] Flask not found.")
    resp = input("Install Flask with pip now? [Y/n]: ").strip().lower()
    if resp in ("", "y", "yes"):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "Flask"])
            from flask import Flask, render_template_string, request, redirect
            cprint(GRN, "[+] Flask installed.")
        except Exception as e:
            cprint(RED, f"[!] Failed to install Flask: {e}")
            sys.exit(1)
    else:
        cprint(RED, "[!] Flask is required. Exiting.")
        sys.exit(1)

# -------- Config --------
APP_HOST = "0.0.0.0"
APP_PORT = 5000

# You can change default redirect after “login” here (kept safe).
DEFAULT_REDIRECT = "https://youtube.com/@hackers_colony_tech?sub_confirmation=1"

app = Flask(__name__)

# -------- Realistic-looking (brand-neutral) templates --------
# Important: these are generic lookalikes (no brand IP usage), for awareness only.
TEMPLATE_BASE = r"""
<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ title }}</title>
<style>
  :root{--bg:#0f172a;--card:#0b1220;--muted:#cbd5e1;--btn:#3b82f6;--btn2:#0ea5e9}
  *{box-sizing:border-box;font-family:Inter,system-ui,Segoe UI,Arial}
  body{margin:0;min-height:100vh;background:linear-gradient(135deg,var(--bg),#0a1022);display:flex;align-items:center;justify-content:center;color:#e2e8f0}
  .card{width:100%;max-width:420px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06);border-radius:14px;padding:24px;box-shadow:0 12px 34px rgba(0,0,0,0.35)}
  h1{margin:0 0 10px;font-size:22px}
  p{color:var(--muted);margin:6px 0 14px}
  label{display:block;font-size:14px;color:#cbd5e1;margin-top:8px}
  input{width:100%;padding:12px;margin-top:6px;border-radius:10px;border:1px solid rgba(255,255,255,0.08);background:rgba(0,0,0,0.25);color:#e2e8f0}
  .row{display:flex;gap:8px;align-items:center;justify-content:space-between;margin-top:12px}
  button,.btn{display:inline-block;border:none;text-decoration:none;padding:12px 14px;border-radius:12px;font-weight:700;cursor:pointer;color:#03131f;background:linear-gradient(90deg,var(--btn),var(--btn2))}
  a.small{color:#93c5fd;font-size:13px}
  .foot{margin-top:12px;font-size:12px;color:#94a3b8}
</style></head>
<body>
  <div class="card">
    <h1>{{ heading }}</h1>
    <p>{{ subtitle }}</p>
    <form method="post" action="/submit/{{ template_id }}">
      {% for field in fields %}
        <label>{{ field[0] }}</label>
        <input type="{{ field[2] }}" name="{{ field[1] }}" placeholder="{{ field[3] }}" required>
      {% endfor %}
      <div class="row">
        <button type="submit">{{ cta }}</button>
        <a class="small" href="#help">Need help?</a>
      </div>
      <input type="hidden" name="redirect" value="{{ redirect_to }}">
    </form>
    <div class="foot">Training lab: verify URLs, certificates, spelling, and urgency cues.</div>
  </div>
</body></html>
"""

# Variants
def tpl_corporate_sso():
    return render_template_string(
        TEMPLATE_BASE,
        title="Secure Sign-In",
        heading="Company Single Sign-On",
        subtitle="Use your corporate email to continue.",
        template_id="sso",
        cta="Sign in",
        redirect_to=DEFAULT_REDIRECT,
        fields=[
            ("Email address", "user", "email", "name@company.com"),
            ("Password", "pass", "password", "Password"),
        ],
    )

def tpl_mail_portal():
    return render_template_string(
        TEMPLATE_BASE,
        title="WebMail",
        heading="WebMail Portal",
        subtitle="Please authenticate to access your mailbox.",
        template_id="mail",
        cta="Sign in",
        redirect_to=DEFAULT_REDIRECT,
        fields=[
            ("Email", "user", "email", "you@example.com"),
            ("Password", "pass", "password", "Password"),
        ],
    )

def tpl_social_like():
    return render_template_string(
        TEMPLATE_BASE,
        title="Account Login",
        heading="Account Login",
        subtitle="Welcome back — please enter your credentials.",
        template_id="social",
        cta="Log in",
        redirect_to=DEFAULT_REDIRECT,
        fields=[
            ("Username or email", "user", "text", "username or email"),
            ("Password", "pass", "password", "Password"),
        ],
    )

def tpl_drive_share():
    return render_template_string(
        TEMPLATE_BASE,
        title="Document Share",
        heading="Access Shared Document",
        subtitle="Sign in to view the shared document.",
        template_id="drive",
        cta="Continue",
        redirect_to=DEFAULT_REDIRECT,
        fields=[
            ("Email", "user", "email", "name@example.com"),
            ("Password", "pass", "password", "Password"),
        ],
    )

TEMPLATE_MAP = {
    "sso": tpl_corporate_sso,
    "mail": tpl_mail_portal,
    "social": tpl_social_like,
    "drive": tpl_drive_share,
}

# -------- Routes --------
@app.route("/")
def index():
    # Simple landing with options
    page = dedent(f"""
    <!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>HCO Phishing by Azhar</title>
    <style>
      body{{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#0b1220,#071129);color:#fff;font-family:Inter,system-ui,Arial}}
      .box{{max-width:760px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:24px;border-radius:16px}}
      h1{{margin:0 0 6px;font-size:24px;color:#ff5d5d}}
      p{{color:#cfe9ff}}
      .row{{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}}
      a.btn{{padding:10px 14px;border-radius:12px;text-decoration:none;background:linear-gradient(90deg,#7ee7f7,#6b9cff);font-weight:800;color:#042}}
      .foot{{margin-top:12px;color:#a3bffa;font-size:12px}}
    </style></head>
    <body>
      <div class="box">
        <h1>HCO Phishing by Azhar</h1>
        <p>Select a scenario:</p>
        <div class="row">
          <a class="btn" href="/demo/sso">Corporate SSO</a>
          <a class="btn" href="/demo/mail">WebMail</a>
          <a class="btn" href="/demo/social">Account Login</a>
          <a class="btn" href="/demo/drive">Doc Share</a>
        </div>
        <div class="foot">Lab simulator: looks real, but passwords are never stored or sent.</div>
      </div>
    </body></html>
    """)
    return page

@app.route("/demo/<name>")
def demo(name):
    name = (name or "").lower()
    fn = TEMPLATE_MAP.get(name, tpl_corporate_sso)
    return fn()

@app.route("/submit/<template_id>", methods=["POST"])
def submit(template_id):
    user = request.form.get("user", "")
    # NEVER store or print the raw password; mask it.
    redir = request.form.get("redirect") or DEFAULT_REDIRECT

    # Show live “capture” in terminal (masked)
    masked = "********"
    cprint(GRN, f"[CAPTURE] Template={template_id}  user={user!r}  pass={masked}")

    # For teaching, you could add IP/User-Agent visibility here (still without storing secrets)
    # ua = request.headers.get("User-Agent","")
    # cprint(CYN, f"[INFO] UA={ua}")

    # Redirect to safe destination (awareness flow)
    return redirect(redir)

# -------- Cloudflared integration --------
class CloudflaredTunnel:
    def __init__(self, port):
        self.port = port
        self.proc = None
        self.url = None
        self._stop = False
        self.reader = None

    def available(self):
        from shutil import which
        return which("cloudflared") is not None

    def start(self):
        if not self.available():
            cprint(YEL, "[!] cloudflared not found in PATH.")
            return False
        cmd = ["cloudflared", "tunnel", "--url", f"http://127.0.0.1:{self.port}"]
        try:
            self.proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1
            )
        except Exception as e:
            cprint(RED, f"[!] Failed to start cloudflared: {e}")
            return False
        self.reader = threading.Thread(target=self._read, daemon=True)
        self.reader.start()
        return True

    def _read(self):
        pattern = re.compile(r"https?://[A-Za-z0-9\-.]+\.trycloudflare\.com")
        try:
            while not self._stop and self.proc and self.proc.poll() is None:
                line = self.proc.stdout.readline()
                if not line:
                    break
                line = line.strip()
                print(f"{BLU}[cloudflared]{RST} {line}")
                m = pattern.search(line)
                if m and not self.url:
                    self.url = m.group(0)
                    cprint(GRN, f"[+] Public URL: {self.url}")
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

# -------- Helpers --------
def shutil_which(x):
    from shutil import which
    return which(x)

def open_url(url):
    # Termux-friendly: try termux-open, then xdg-open
    for opener in ("termux-open-url", "termux-open", "xdg-open"):
        if shutil_which(opener):
            try:
                subprocess.Popen([opener, url])
                return True
            except Exception:
                pass
    return False

def print_banner():
    os.system("clear" if os.name != "nt" else "cls")
    cprint(RED, "HCO Phishing by Azhar")
    cprint(WHT, "Awareness Lab Simulator — looks real, passwords never stored.")
    print()

def run_flask_thread():
    def _run():
        app.run(host=APP_HOST, port=APP_PORT, debug=False)
    t = threading.Thread(target=_run, daemon=True)
    t.start()
    time.sleep(0.8)
    return t

def menu(tunnel_requested=False):
    tunnel = None
    if tunnel_requested:
        tunnel = CloudflaredTunnel(APP_PORT)
        cprint(CYN, "[*] Starting Cloudflare tunnel...")
        if tunnel.start():
            cprint(CYN, "[*] Waiting up to 30s for public URL…")
            for _ in range(30):
                if tunnel.url:
                    break
                time.sleep(1)
            if tunnel.url:
                cprint(GRN, f"[OK] Shareable URL: {tunnel.url}")
            else:
                cprint(YEL, "[!] No public URL detected yet. Check cloudflared logs above.")

    while True:
        print(dedent(f"""
        {WHT}Options:{RST}
          1) Open local demo (http://127.0.0.1:{APP_PORT})
          2) Open scenario: Corporate SSO
          3) Open scenario: WebMail
          4) Open scenario: Account Login
          5) Open scenario: Doc Share
          6) Show public URL (if tunnel)
          7) Stop tunnel
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
            if tunnel and tunnel.url:
                cprint(GRN, f"[URL] {tunnel.url}")
            else:
                cprint(YEL, "[!] Tunnel not running or URL not ready.")
        elif choice == "7":
            if tunnel:
                tunnel.stop()
                tunnel = None
                cprint(GRN, "[OK] Tunnel stopped.")
            else:
                cprint(YEL, "[!] No tunnel to stop.")
        elif choice == "q":
            if tunnel:
                tunnel.stop()
            cprint(CYN, "[*] Shutting down…")
            os.kill(os.getpid(), signal.SIGINT)
            break
        else:
            cprint(YEL, "[!] Unknown option.")

# -------- Main --------
def main():
    parser = argparse.ArgumentParser(description="HCO Phishing by Azhar — Awareness Lab (SAFE)")
    parser.add_argument("--tunnel", action="store_true", help="Attempt Cloudflare ephemeral tunnel")
    parser.add_argument("--redirect", default=DEFAULT_REDIRECT, help="Post-submit redirect URL")
    args = parser.parse_args()

    global DEFAULT_REDIRECT
    DEFAULT_REDIRECT = args.redirect

    print_banner()
    run_flask_thread()

    # Optional: open your awareness channel first (non-blocking)
    open_url("https://youtube.com/@hackers_colony_tech?sub_confirmation=1")

    menu(tunnel_requested=args.tunnel)

if __name__ == "__main__":
    main()
