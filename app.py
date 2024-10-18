from flask import Flask, app, render_template, request, redirect, url_for
import sqlite3

def init_db():
    # Connect to database
    conn = sqlite3.connect('tasks.db')  
    # Create a cursor to SQL queries
    cursor = conn.cursor()  
    # Create the tasks table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT NOT NULL,
                        completed BOOLEAN NOT NULL)''')
    # Save the changes
    conn.commit()
    # Close the connection to the database
    conn.close()  
    
def get_tasks():
    conn = sqlite3.connect('tasks.db')  
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')  
    tasks = cursor.fetchall()  # Fetch all rows from the tasks table
    conn.close()  
    return tasks  # Return the list of tasks

@app.route('/')
def index():
    tasks = get_tasks()  # Get all tasks from the database
    return render_template('index.html', tasks=tasks)  # Render index.html with tasks

@app.route('/add', methods=['POST'])
def add_task():
    task_description = request.form['description']  # Get task description from form
    if task_description:
        conn = sqlite3.connect('tasks.db')  
        cursor = conn.cursor()  
        cursor.execute('INSERT INTO tasks (description, completed) VALUES (?, ?)', (task_description, False))
        conn.commit()  
        conn.close()  
    return redirect(url_for('index'))  # Redirect back to the home page

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    conn = sqlite3.connect('tasks.db')  
    cursor = conn.cursor()  
    cursor.execute('UPDATE tasks SET completed = ? WHERE id = ?', (True, task_id))
    conn.commit()  
    conn.close()  
    return redirect(url_for('index')) 

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')  
    cursor = conn.cursor()  
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()  
    conn.close()  
    return redirect(url_for('index'))  

if __name__ == '__main__':
    init_db()  # Initialize the database when app starts
    app.run(debug=True)  # Run the Flask app in debug mode

