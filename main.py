from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)
DB_PATH = '/nfs/demo.db'

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.execute('''
            CREATE TABLE contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    conn = sqlite3.connect(DB_PATH)
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        if name and phone:
            conn.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
            conn.commit()
    rows = conn.execute("SELECT name, phone FROM contacts").fetchall()
    conn.close()
    return render_template_string("""
        <h2>Add Contact</h2>
        <form method="post">
            <input name="name" placeholder="Name" required>
            <input name="phone" placeholder="Phone" required>
            <button type="submit">Add</button>
        </form>
        <h2>Contacts</h2>
        <ul>
        {% for name, phone in rows %}
            <li>{{ name }} - {{ phone }}</li>
        {% endfor %}
        </ul>
    """, rows=rows)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
