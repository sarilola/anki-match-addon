#--------------------------------#
#     made by sara chiriboga     #
#       discord: sarilolaaa      #
#--------------------------------#

from aqt import mw  # Main Anki window object
from aqt.qt import *
from aqt.editor import Editor
from aqt.webview import WebContent
from aqt.gui_hooks import editor_did_init_buttons, webview_will_set_content, card_will_show, profile_did_open
import json
import os


def create_note_type():
    """
    Creates a custom note type called 'Matching Exercise' with fields for matching concepts and answers.
    Loads custom HTML templates for the card front and back.
    Skips creation if the note type already exists.
    """
    try:
        mm = mw.col.models  # Access the model manager
        model_name = "Matching Exercise"

        # Check if the note type already exists
        if mm.by_name(model_name):
            print(f"Note type '{model_name}' already exists. Skipping creation.")
            return True

        print(f"Creating note type: {model_name}")
        model = mm.new(model_name)

        # Add fields for instructions, concepts, and answers
        mm.add_field(model, mm.new_field("Question or Instructions"))
        mm.add_field(model, mm.new_field("Concept 1"))
        mm.add_field(model, mm.new_field("Answer 1"))
        mm.add_field(model, mm.new_field("Concept 2"))
        mm.add_field(model, mm.new_field("Answer 2"))
        mm.add_field(model, mm.new_field("Concept 3"))
        mm.add_field(model, mm.new_field("Answer 3"))
        mm.add_field(model, mm.new_field("Concept 4"))
        mm.add_field(model, mm.new_field("Answer 4"))

        # Set up card template with custom HTML
        template = mm.new_template("Match Card")
        template['qfmt'] = load_template_html("match_front.html")
        template['afmt'] = load_template_html("match_back.html")

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
    """
    Loads the HTML content for a given template file from the add-on's web directory.
    """
    addon_package = mw.addonManager.addonFromModule(__name__)
    file_path = os.path.join(mw.addonManager.addonsFolder(), addon_package, "web", filename)
    with open(file_path, encoding="utf-8") as f:
        return f.read()


# Optionally inject extra JS resources for the editor or preview (not required for main matching logic)
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
    """
    Hook function to set up the card's HTML before display.
    Loads the appropriate template (front or back) and replaces placeholders with note field values.
    """
    note = card.note()
    try:
        if "Question or Instructions" in note:
            # Choose template based on review context
            template_file = "match_back.html" if context == "reviewAnswer" else "match_front.html"
            # Load template HTML
            addon_package = mw.addonManager.addonFromModule(__name__)
            file_path = os.path.join(mw.addonManager.addonsFolder(), addon_package, "web", template_file)
            with open(file_path, encoding="utf-8") as f:
                html = f.read()
            # Replace placeholders with note field values
            replacements = {
                "{{Question or Instructions}}": note["Question or Instructions"],
                "{{Concept 1}}": note["Concept 1"],
                "{{Answer 1}}": note["Answer 1"],
                "{{Concept 2}}": note["Concept 2"],
                "{{Answer 2}}": note["Answer 2"],
                "{{Concept 3}}": note["Concept 3"],
                "{{Answer 3}}": note["Answer 3"],
                "{{Concept 4}}": note["Concept 4"],
                "{{Answer 4}}": note["Answer 4"]
            }
            for placeholder, value in replacements.items():
                html = html.replace(placeholder, value)
            return html
    except Exception as e:
        # Show error in card if processing fails
        return text + f"<div style='color:red'>Error processing card: {str(e)}</div>"
    return text


def initialize_addon():
    """
    Initializes the add-on: exports web files, injects web resources, and attaches the card HTML setup hook.
    """
    try:
        mw.addonManager.setWebExports(__name__, r"web/.*")
        webview_will_set_content.append(inject_web_resources)
        card_will_show.append(setup_card_html)
    except Exception as e:
        print(f"Error inicializando add-on: {str(e)}")


# On Anki startup, create the note type and initialize the add-on if mw is available
if mw:
    profile_did_open.append(lambda: (
        create_note_type(),
        initialize_addon()
    ))
else:
    print("Error: mw no está disponible")