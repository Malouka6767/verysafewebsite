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
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    address1 = request.form.get("address1")
    address2 = request.form.get("address2")
    city = request.form.get("city")
    state = request.form.get("state")
    postal = request.form.get("postal")
    country = request.form.get("country")

    data = {
        "First Name": firstName,
        "Last Name": lastName,
        "Address 1": address1,
        "Address 2": address2 or "(none)",
        "City": city,
        "State": state,
        "Postal Code": postal,
        "Country": country,
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
