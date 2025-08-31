import os
import sqlite3
import difflib
from flask import Flask, request, render_template, Response, g
from model import GeminiCorrectionModule
from fpdf import FPDF

app = Flask(__name__)
DATABASE = 'database.db'

# --- Database Setup ---
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# --- Initialize Database Table ---
def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY,
                original_text TEXT NOT NULL,
                corrected_text TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()

# Initialize the database table
init_db()

# --- Helper Function for Diff Generation ---
def generate_diff_html(original, corrected):
    """Generates an HTML diff of two strings, highlighting word changes."""
    original_words = original.split()
    corrected_words = corrected.split()
    matcher = difflib.SequenceMatcher(None, original_words, corrected_words)
    
    diff_html = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            diff_html.append('<del>' + ' '.join(original_words[i1:i2]) + '</del>')
            diff_html.append('<ins>' + ' '.join(corrected_words[j1:j2]) + '</ins>')
        elif tag == 'delete':
            diff_html.append('<del>' + ' '.join(original_words[i1:i2]) + '</del>')
        elif tag == 'insert':
            diff_html.append('<ins>' + ' '.join(corrected_words[j1:j2]) + '</ins>')
        elif tag == 'equal':
            diff_html.append(' '.join(original_words[i1:i2]))
    
    # Join with spaces and handle potential HTML issues
    return ' '.join(diff_html).replace(' <', '&nbsp;<').replace('> ', '>&nbsp;')

# Initialize the Gemini module
correction_module = GeminiCorrectionModule()

# --- Main Application Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    if request.method == 'POST':
        original_text = ""
        if 'text' in request.form and request.form['text']:
            original_text = request.form['text']
        
        if original_text and original_text.strip():
            corrected_text = correction_module.correct_text(original_text)
            db.execute('INSERT INTO history (original_text, corrected_text) VALUES (?, ?)',
                       (original_text, corrected_text))
            db.commit()

    history_cursor = db.execute('SELECT * FROM history ORDER BY timestamp DESC')
    history = history_cursor.fetchall()
    
    return render_template('index.html', history=history)

@app.route('/diff/<int:history_id>')
def get_diff(history_id):
    """Endpoint to get the HTML diff for a specific history item."""
    db = get_db()
    item = db.execute('SELECT original_text, corrected_text FROM history WHERE id = ?', (history_id,)).fetchone()
    if not item:
        return "History item not found.", 404
    
    diff_html = generate_diff_html(item['original_text'], item['corrected_text'])
    return diff_html

@app.route('/download/<int:history_id>/<file_format>')
def download(history_id, file_format):
    db = get_db()
    history_item = db.execute('SELECT corrected_text FROM history WHERE id = ?', (history_id,)).fetchone()
    if not history_item:
        return "History not found", 404

    corrected_text = history_item['corrected_text']

    if file_format == 'txt':
        return Response(
            corrected_text,
            mimetype="text/plain",
            headers={"Content-disposition": "attachment; filename=corrected_text.txt"}
        )
    elif file_format == 'pdf':
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=corrected_text.encode('latin-1', 'replace').decode('latin-1'))
        pdf_output = pdf.output(dest='S').encode('latin-1')
        return Response(
            pdf_output,
            mimetype="application/pdf",
            headers={"Content-disposition": "attachment; filename=corrected_text.pdf"}
        )
    
    return "Invalid format", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
