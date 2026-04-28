from flask import Flask, render_template, request, jsonify, send_file
import base64
import json
import os
from shortcuts_engine import generate_shortcut_structure

app = Flask(__name__)

# -------------------------
# STATIC DATA (Templates)
# -------------------------
TEMPLATES = [
    {
        "id": "weather_alert",
        "name": "Weather Alert",
        "description": "Get weather + notification",
        "prompt": "Get weather and show notification",
        "icon_color": "blue",
        "icon_glyph": "cloud"
    },
    {
        "id": "call_contact",
        "name": "Call Someone",
        "description": "Ask for number then call",
        "prompt": "Ask for phone number then call it",
        "icon_color": "green",
        "icon_glyph": "phone"
    }
]

ACTIONS = {
    "get_weather": {"label": "Get Weather", "category": "weather"},
    "show_notification": {"label": "Show Notification", "category": "notification"},
    "ask_input": {"label": "Ask for Input", "category": "input"},
    "call_phone": {"label": "Call Phone Number", "category": "phone"},
    "open_url": {"label": "Open URL", "category": "web"}
}

# -------------------------
# ROUTES
# -------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/templates")
def templates():
    return jsonify({"templates": TEMPLATES})

@app.route("/api/actions")
def actions():
    return jsonify({"actions": ACTIONS})

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json

    name = data.get("name", "My Shortcut")
    description = data.get("description", "")
    icon_color = data.get("icon_color", "blue")
    icon_glyph = data.get("icon_glyph", "star")

    shortcut = generate_shortcut_structure(
        name=name,
        description=description,
        icon_color=icon_color,
        icon_glyph=icon_glyph
    )

    os.makedirs("output", exist_ok=True)

    file_path = f"output/{name.replace(' ', '_')}.shortcut"

    with open(file_path, "wb") as f:
        f.write(shortcut["binary"])

    return jsonify({
        "name": name,
        "actions": shortcut["actions"],
        "file_size": len(shortcut["binary"]),
        "shortcut_base64": base64.b64encode(shortcut["binary"]).decode()
    })

@app.route("/api/download", methods=["POST"])
def download():
    data = request.json
    name = data.get("name", "shortcut")
    file_data = base64.b64decode(data["shortcut_base64"])

    file_path = f"output/{name}.shortcut"

    with open(file_path, "wb") as f:
        f.write(file_data)

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
