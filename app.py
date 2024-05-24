from flask import Flask, render_template, request, jsonify, g
import datetime
import sqlite3
import threading
import time

app = Flask(__name__)

DATABASE = 'check_ins.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

user_dict = {
    "705131444": "Aanish Farrukh"
}

def get_name_by_id(id, user_dict):
    id_first_9 = id[:9]
    if id_first_9 in user_dict:
        return user_dict[id_first_9]
    else:
        return None

def flash_background():
    time.sleep(4)
    app.config['FLASH'] = False

@app.route('/')
def index():
    return render_template('index.html', flash=app.config.get('FLASH', False))

@app.route('/check_ins', methods=['GET'])
def get_check_ins():
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM check_ins")
    check_ins = c.fetchall()
    return jsonify(check_ins)

@app.route('/check_in', methods=['POST'])
def check_in():
    id = request.form.get('id')
    if not id:
        return jsonify({'error': 'ID is required'}), 400

    name = get_name_by_id(id, user_dict)
    if not name:
        return jsonify({'error': 'ID not found'}), 404

    db = get_db()
    c = db.cursor()

    # Get current time
    check_in_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insert data into the database
    try:
        c.execute("INSERT INTO check_ins (id, name, check_in_time) VALUES (?, ?, ?)", (id, name, check_in_time))
        db.commit()
        app.config['FLASH'] = True
        threading.Thread(target=flash_background).start()
        return jsonify({'message': f'Checked in successfully. Welcome, {name}!'}), 200
    except sqlite3.IntegrityError as e:
        print("Error:", e)  # Print the error message
        return jsonify({'error': 'Failed to check in'}), 400

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)