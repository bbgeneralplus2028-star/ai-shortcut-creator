import json

def generate_shortcut_structure(name, description, icon_color, icon_glyph):

    # Simple AI-like rule engine (you can upgrade to OpenAI later)
    actions = []

    desc = description.lower()

    if "weather" in desc:
        actions.append({"identifier": "get_weather", "label": "Get Weather"})
        actions.append({"identifier": "show_notification", "label": "Show Notification"})

    if "call" in desc or "phone" in desc:
        actions.append({"identifier": "ask_input", "label": "Ask for Phone Number"})
        actions.append({"identifier": "call_phone", "label": "Call Phone Number"})

    if "open" in desc or "url" in desc:
        actions.append({"identifier": "open_url", "label": "Open URL"})

    if not actions:
        actions.append({"identifier": "show_notification", "label": "Show Notification"})

    # Fake Apple-style binary (important note below)
    payload = {
        "WFWorkflowName": name,
        "WFWorkflowActions": actions,
        "WFWorkflowIcon": {
            "color": icon_color,
            "glyph": icon_glyph
        }
    }

    binary = json.dumps(payload).encode("utf-8")

    return {
        "actions": actions,
        "binary": binary
    }
