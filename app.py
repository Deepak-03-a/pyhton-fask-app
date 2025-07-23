from flask import Flask, request
import psycopg2
import os

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

@app.route('/')
def hello():
    return "Flask App connected to PostgreSQL!"

@app.route('/save', methods=['POST'])
def save_message():
    msg = request.form.get("msg", "")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS messages (id serial PRIMARY KEY, msg text);")
    cur.execute("INSERT INTO messages (msg) VALUES (%s);", (msg,))
    conn.commit()
    cur.close()
    conn.close()
    return f"Message saved: {msg}"

@app.route('/messages')
def list_messages():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT msg FROM messages;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return "<br>".join([r[0] for r in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
