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
  <title>Python App</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Segoe UI', system-ui, sans-serif;
      min-height: 100vh;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      background: linear-gradient(135deg, #306998 0%, #1e415e 100%);
      color: #fff; text-align: center; padding: 2rem;
    }}
    header {{
      background: #ffd43b; color: #234567;
      padding: 1rem 2.5rem; border-radius: 999px;
      font-weight: 800; letter-spacing: 1px; text-transform: uppercase;
      box-shadow: 0 8px 30px rgba(0,0,0,.3); margin-bottom: 2rem;
    }}
    h1 {{ font-size: clamp(2rem, 6vw, 4rem); margin-bottom: .5rem; }}
    .logo {{ font-size: 4rem; margin-bottom: 1rem; }}
    .card {{
      background: rgba(255,255,255,.1); backdrop-filter: blur(8px);
      border: 1px solid rgba(255,255,255,.2); border-radius: 16px;
      padding: 1.5rem 2rem; margin-top: 1.5rem; font-family: monospace;
    }}
    .pill {{ display:inline-block; background:#ffd43b; color:#234567; padding:.2rem .8rem; border-radius:999px; font-weight:700; }}
    a {{ color: #ffd43b; }}
    footer {{ margin-top: 2rem; opacity: .7; font-size: .85rem; }}
  </style>
</head>
<body>
  <header>🐍 Python Service</header>
  <div class="logo">🐍</div>
  <h1>You are doing great, little human! &lt;3</h1>
  <p>A Flask app, served fresh from Kubernetes.</p>
  <div class="card">
    host <span class="pill">{hostname}</span><br><br>
    version <span class="pill">{version}</span><br><br>
    {time}
  </div>
  <footer>API: <a href="/api/v1/info">/api/v1/info</a> &middot; <a href="/api/v1/healthz">/api/v1/healthz</a></footer>
</body>
</html>"""


@app.route("/")
def home():
    return PAGE.format(
        hostname=socket.gethostname(),
        version=os.getenv("APP_VERSION", "unknown"),
        time=datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y"),
    )


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
