from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from config import db_config

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>')
def update(task_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE tasks SET is_complete = NOT is_complete WHERE id = %s", (task_id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
