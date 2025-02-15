from flask import Flask, render_template, url_for, redirect, request
import sqlite3

app = Flask(__name__)

# Database setup 
DATABASE = "database.db"

def get_db_connection():
    """
    Establishes a connection to the SQLite database and returns the connection object.
    Sets the row factory to sqlite3.Row to allow dictionary-like access to query results.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return conn

# INITIALIZE DATABASE
with get_db_connection() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    """)  # Creates the tasks table if it doesn't exist
    conn.commit()
    

@app.route("/")
def index():
    """
    Fetches all tasks from the database and renders them in the index.html template.
    """
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=['POST'])
def add_task():
    """
    Adds a new task to the database if a title is provided and redirects to the homepage.
    """
    title = request.form.get("title")  # Retrieves the task title from the form
    if title:
        conn = get_db_connection()
        conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        conn.commit()
        conn.close()
    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    """
    Marks a task as completed by updating its 'completed' status in the database.
    """
    conn = get_db_connection()
    conn.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    """
    Deletes a task from the database based on its ID.
    """
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Runs the Flask app in debug mode on port 2020, accessible from any host
    app.run(debug=True, host="0.0.0.0", port=2020)
