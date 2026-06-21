import datetime
import os
import socket

from flask import Flask, jsonify


app = Flask(__name__)


PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Python Service · Hello!</title>
  <style>
    :root { --blue:#306998; --yellow:#ffd43b; }
    * { box-sizing:border-box; margin:0; padding:0; }
    body {
      font-family:'Segoe UI',system-ui,sans-serif; color:#fff; min-height:100vh;
      display:flex; flex-direction:column; align-items:center; justify-content:center;
      text-align:center; padding:2rem; overflow-x:hidden;
      background:linear-gradient(-45deg,#306998,#1e415e,#4b8bbe,#234567);
      background-size:400% 400%; animation:bg 18s ease infinite;
    }
    @keyframes bg { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
    .badge { background:var(--yellow); color:#234567; padding:.5rem 1.4rem; border-radius:999px;
      font-weight:800; letter-spacing:1px; text-transform:uppercase; font-size:.78rem; box-shadow:0 8px 24px rgba(0,0,0,.3); }
    .snake { font-size:5rem; margin:1.2rem 0; animation:float 3s ease-in-out infinite; }
    @keyframes float { 0%,100%{transform:translateY(0) rotate(-4deg)} 50%{transform:translateY(-18px) rotate(4deg)} }
    h1 { font-size:clamp(2rem,7vw,4.2rem); margin-bottom:.4rem; }
    .sub { opacity:.88; font-size:1.05rem; max-width:40ch; margin:0 auto 1.8rem; }
    .card { background:rgba(255,255,255,.1); backdrop-filter:blur(10px); border:1px solid rgba(255,255,255,.2);
      border-radius:18px; padding:1.2rem 1.6rem; font-family:monospace; min-width:300px; }
    .row { display:flex; justify-content:space-between; gap:1.5rem; padding:.4rem 0; }
    .row span:last-child { color:var(--yellow); font-weight:700; }
    .dot { display:inline-block; width:.7rem; height:.7rem; border-radius:50%; background:#3ad06a;
      box-shadow:0 0 10px #3ad06a; animation:pulse 1.6s infinite; }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.35} }
    .btns { display:flex; gap:.8rem; flex-wrap:wrap; justify-content:center; margin-top:1.8rem; }
    .btn { background:var(--yellow); color:#234567; text-decoration:none; padding:.7rem 1.4rem;
      border-radius:999px; font-weight:700; transition:transform .15s; }
    .btn.ghost { background:transparent; color:#fff; border:1.5px solid rgba(255,255,255,.4); }
    .btn:hover { transform:translateY(-3px); }
    footer { margin-top:2rem; opacity:.6; font-size:.8rem; }
  </style>
</head>
<body>
  <div class="badge">🐍 Python Service</div>
  <div class="snake">🐍</div>
  <h1>Hello, human!</h1>
  <p class="sub">You're doing great. This little Flask app is alive and happy on Kubernetes. &lt;3</p>
  <div class="card">
    <div class="row"><span>status</span><span><span class="dot"></span> live</span></div>
    <div class="row"><span>pod</span><span id="host">…</span></div>
    <div class="row"><span>version</span><span id="ver">…</span></div>
    <div class="row"><span>time</span><span id="time">…</span></div>
  </div>
  <div class="btns">
    <a class="btn" href="/api/v1/info">Service info</a>
    <a class="btn ghost" href="/api/v1/healthz">Health check</a>
  </div>
  <footer>served by python-app · kubernetes</footer>
  <script>
    async function load() {
      try {
        const d = await (await fetch('/api/v1/info')).json();
        document.getElementById('host').textContent = d.hostname;
        document.getElementById('ver').textContent = d.version;
        document.getElementById('time').textContent = d.time;
      } catch (e) {}
    }
    load(); setInterval(load, 5000);
  </script>
</body>
</html>"""


@app.route("/")
def home():
    return PAGE


@app.route("/api/v1/info")
def info():
    return jsonify(
        {
            "time": datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y"),
            "hostname": socket.gethostname(),
            "message": "You are doing great, little human! <3",
            "deployed_on": "kubernetes",
            "version": os.getenv("APP_VERSION", "unknown"),
        }
    )


@app.route("/api/v1/healthz")
def health():
    return jsonify({"status": "up"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
