from aqt import mw
from aqt.qt import *
from aqt.editor import Editor
from aqt.gui_hooks import editor_did_init_buttons
import json

# register a new note type in anki
def add_match_note_type():
    mm = mw.col.models
    match_model = mm.new("Matching Concepts")
    
    # fields inside the model
    mm.add_field(match_model, mm.new_field("Question"))
    mm.add_field(match_model, mm.new_field("Concept"))
    mm.add_field(match_model, mm.new_field("Answer"))
    
    # card's interface
    template = mm.new_template("Match Card")
    template['afmt'] = "{{FrontSide}}<hr id='answer'>"
    
    # adding the template to de card model
    mm.add_template(match_model, template)
    mm.add(match_model)


# button in the editor
def setup_editor_buttons(buttons, editor):
    def create_match_card():
        # create new note with JSON structure
        note = editor.note
        note.fields[0] = "Write the question or instructions"
        note.fields[1] = json.dumps({
            "preguntas": [
                {"texto": "Pregunta 1", "opciones": ["Opción A", "Opción B"]},
                {"texto": "Pregunta 2", "opciones": ["Opción C", "Opción D"]}
            ]
        })
        editor.loadNote()
    
    b = editor.addButton(icon="match.png", cmd="match_card",
                         func=create_match_card, tip="Crear ejercicio Match")
    buttons.append(b)
    return buttons

# initialize
def init():
    add_match_note_type()
    editor_did_init_buttons.append(setup_editor_buttons)

init()

from aqt.webview import WebContent
from aqt.gui_hooks import webview_did_receive_js_message

# 4. Inyectar recursos web
def on_webview_set_content(web_content: WebContent, context):
    if isinstance(context, anki.cards.Card) and context.note().model()['name'] == "Match Exercise":
        web_content.js.append("/_addons/match_addon/web/match.js")
        web_content.css.append("/_addons/match_addon/web/match.css")
        web_content.body += mw.col.media.escape_html(context.note().fields[1])

# 5. Manejar verificación
def handle_js_message(handled, cmd, context):
    if cmd.startswith("verificar:"):
        resultados = json.loads(cmd[10:])
        # Lógica de verificación (aquí usarías las respuestas correctas)
        correctas = all(r != "" for r in resultados)  # Ejemplo simple
        
        # Enviar resultado a JS
        js = f"showResult({json.dumps(correctas)})"
        context.web.eval(js)
        return (True, None)
    return handled

# 6. Mostrar resultado en JS
JS_SHOW_RESULT = """
function showResult(correct) {
    const resultDiv = document.getElementById('resultado');
    resultDiv.textContent = correct ? 
        '✅ Todas correctas!' : '❌ Algunas respuestas faltantes';
    resultDiv.style.color = correct ? 'green' : 'red';
}
"""

# 7. Configurar hooks
def init_web():
    gui_hooks.webview_will_set_content.append(on_webview_set_content)
    gui_hooks.webview_did_receive_js_message.append(handle_js_message)
    mw.addonManager.setWebExports(__name__, r"web/.*")

init_web()