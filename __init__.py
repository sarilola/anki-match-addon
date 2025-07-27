# C:\Users\saril\AppData\Roaming\Anki2\addons21\match_addon\__init__.py

from aqt import mw
from aqt.qt import *
from aqt.editor import Editor
from aqt.webview import WebContent
from aqt.gui_hooks import editor_did_init_buttons, webview_will_set_content, card_will_show, profile_did_open
import json
import os

def create_note_type():
    try:
        mm = mw.col.models
        model_name = "Matching Exercise"

        if mm.by_name(model_name):
            print(f"Note type '{model_name}' already exists. Skipping creation.")
            return True

        print(f"Creating note type: {model_name}")
        model = mm.new(model_name)

        mm.add_field(model, mm.new_field("Question or Instructions"))
        mm.add_field(model, mm.new_field("Concept 1"))
        mm.add_field(model, mm.new_field("Answer 1"))
        mm.add_field(model, mm.new_field("Concept 2"))
        mm.add_field(model, mm.new_field("Answer 2"))
        mm.add_field(model, mm.new_field("Concept 3"))
        mm.add_field(model, mm.new_field("Answer 3"))
        mm.add_field(model, mm.new_field("Concept 4"))
        mm.add_field(model, mm.new_field("Answer 4"))

        template = mm.new_template("Match Card")
        template['qfmt'] = load_template_html("match.html")
        template['afmt'] = load_template_html("match.html")

        mm.add_template(model, template)
        mm.add(model)
        mw.col.models.save(model)
        mw.col.save()
        print(f"Note type '{model_name}' created successfully.")
        return True

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error creating note type: {e}")
        return False

def load_template_html(filename):
    addon_package = mw.addonManager.addonFromModule(__name__)
    file_path = os.path.join(mw.addonManager.addonsFolder(), addon_package, "web", filename)
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def inject_web_resources(web_content: WebContent, context):
    if isinstance(context, Editor):
        model = mw.col.models.by_name("Matching Exercise")
        if model and context.note and context.note.mid == model["id"]:
            addon_package = mw.addonManager.addonFromModule(__name__)
            web_content.js.append(f"/_addons/{addon_package}/web/match.js")
    elif hasattr(context, 'note') and context.note is not None:
        if "Question or Instructions" in context.note:
            addon_package = mw.addonManager.addonFromModule(__name__)
            web_content.js.append(f"/_addons/{addon_package}/web/match.js")

def setup_card_html(text: str, card, context):
    note = card.note()
    try:
        if "Question or Instructions" in note:
            # Load the template HTML
            addon_package = mw.addonManager.addonFromModule(__name__)
            file_path = os.path.join(mw.addonManager.addonsFolder(), addon_package, "web", "match.html")
            with open(file_path, encoding="utf-8") as f:
                html = f.read()
            
            # Replace placeholders
            html = html.replace("{{Question or Instructions}}", note["Question or Instructions"])
            html = html.replace("{{Concept 1}}", note["Concept 1"])
            html = html.replace("{{Answer 1}}", note["Answer 1"])
            html = html.replace("{{Concept 2}}", note["Concept 2"])
            html = html.replace("{{Answer 2}}", note["Answer 2"])
            html = html.replace("{{Concept 3}}", note["Concept 3"])
            html = html.replace("{{Answer 3}}", note["Answer 3"])
            html = html.replace("{{Concept 4}}", note["Concept 4"])
            html = html.replace("{{Answer 4}}", note["Answer 4"])
            
            return html
    except Exception as e:
        return text + f"<div style='color:red'>Error procesando tarjeta: {str(e)}</div>"
    return text

def initialize_addon():
    try:
        mw.addonManager.setWebExports(__name__, r"web/.*")
        webview_will_set_content.append(inject_web_resources)
        card_will_show.append(setup_card_html)
    except Exception as e:
        print(f"Error inicializando add-on: {str(e)}")

if mw:
    profile_did_open.append(lambda: (
        create_note_type(),
        initialize_addon()
    ))
else:
    print("Error: mw no está disponible")