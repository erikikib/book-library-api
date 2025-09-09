from flask import Flask, request, jsonify
import sqlite3, os

DB = "books.db"
app = Flask(__name__)

def conn():
    return sqlite3.connect(DB)

def init_db():
    with conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS books(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            read INTEGER DEFAULT 0
        )""")
init_db()

@app.get("/books")
def list_books():
    with conn() as c:
        rows = c.execute("SELECT id,title,author,read FROM books ORDER BY id").fetchall()
    data = [{"id": r[0], "title": r[1], "author": r[2], "read": bool(r[3])} for r in rows]
    return jsonify(data)

@app.post("/books")
def create_book():
    data = request.get_json(force=True)
    with conn() as c:
        cur = c.execute("INSERT INTO books(title,author,read) VALUES(?,?,?)",
                        (data.get("title",""), data.get("author",""), int(bool(data.get("read", False)))))
        bid = cur.lastrowid
    return jsonify({"id": bid}), 201

@app.put("/books/<int:bid>")
def update_book(bid):
    data = request.get_json(force=True)
    with conn() as c:
        c.execute("UPDATE books SET title=?, author=?, read=? WHERE id=?",
                  (data.get("title",""), data.get("author",""), int(bool(data.get("read", False))), bid))
    return jsonify({"updated": bid})

@app.delete("/books/<int:bid>")
def delete_book(bid):
    with conn() as c:
        c.execute("DELETE FROM books WHERE id=?", (bid,))
    return jsonify({"deleted": bid})

if __name__ == "__main__":
    app.run(debug=True)
