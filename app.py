import sqlite3 
from flask import request, jsonify, Flask , render_template

app = Flask(__name__)

def create_database():
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL
                  )''')
    connect.commit()
    connect.close()

def clear_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users')
    conn.commit()
    conn.close()

@app.route('/adduser', methods=['POST'])
def add_user():
    data = request.json
    if not data:
        return jsonify({'error': 'No user provided'}), 400

    user_name = data.get('name')
    user_id = data.get('id')

    if user_name is None or user_id is None:
        return jsonify({'error': 'Name or ID not provided'}), 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('INSERT INTO users (name, id) VALUES (?, ?)', (user_name, user_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM users WHERE id > 5')
    results = cursor.fetchall()
    conn.close()

    names = [result[0] for result in results]

    return jsonify({'Names with IDs greater than 5': names})



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cleardatabase')  # New route for clearing database
def clear_database_route():
    clear_database()
    return 'Database cleared successfully'


if __name__ == '__main__':
    create_database()  # Call the function to create the database
    app.run(debug=True)
