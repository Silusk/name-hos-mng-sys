from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

DB_PATH = "hospital.db"
print("database file path:",os.path.abspath(DB_PATH))

# -----------------------------
# Initialize the SQLite database
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -----------------------------
# Home page + message form
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name").strip()
        email = request.form.get("email").strip()
        subject = request.form.get("subject").strip()
        message = request.form.get("message").strip()
        print("received:",name,email,subject,message)
        if name and email and message:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO messages (name, email, subject, message)
                VALUES (?, ?, ?, ?)
            """, (name, email, subject, message))
            conn.commit()
            conn.close()
            flash("✅ Thank you! Your message has been sent.", "success")
        else:
            flash("⚠️ Please fill all required fields.", "error")

        return redirect(url_for("home"))

    return render_template("index.html")

# -----------------------------
# Admin page to view all messages
# -----------------------------
@app.route("/admin/messages")
def view_messages():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, subject, message, date FROM messages ORDER BY date DESC")
    messages = cursor.fetchall()
    conn.close()
    return render_template("messages.html", messages=messages)

# -----------------------------
# Run app
# -----------------------------
if __name__ == "__main__":
    # Delete DB if file path incorrect (optional safety)
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(debug=True)
