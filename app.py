from flask import Flask, render_template, jsonify, request
from random import randint
import threading
import time
import sqlite3
from datetime import datetime

app = Flask(__name__)

x, y, z, m = 0, 0, 0, 0
lock = threading.Lock()

# Veritabanı kurulumu
def init_db():
    conn = sqlite3.connect('coordinates.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS coordinates
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, x INTEGER, y INTEGER, z INTEGER, m INTEGER, timestamp TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Koordinatları veri tabanına kaydetme
def save_coordinates_db(x, y, z, m):
    try:
        conn = sqlite3.connect('coordinates.db')
        c = conn.cursor()
        current_time = datetime.now().strftime("%d-%m-%Y / %H:%M:%S")
        c.execute("INSERT INTO coordinates (x, y, z, m, timestamp) VALUES (?, ?, ?, ?, ?)",
                  (x, y, z, m, current_time))
        conn.commit()
        conn.close()
        print("Coordinates saved successfully.")
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])

# Rastgele koordinatlar burada üretiliyor
def generate_random_coordinates():
    global x, y, z, m
    with lock:
        x = randint(1, 100)
        y = randint(1, 100)
        z = randint(1, 100)
        m = randint(1, 100)

# Koordinatlar burada güncelleniyor
def update_coordinates():
    while True:
        generate_random_coordinates()
        time.sleep(1)

# Thread'i başlatma
update_thread = threading.Thread(target=update_coordinates)
update_thread.daemon = True
update_thread.start()

# Ana sayfa burada render ediliyor
@app.route('/')
def index():
    return render_template('index.html')

# AJAX isteği için JSON veri döndüren route
@app.route('/update_data')
def update_data():
    global x, y, z, m
    data = {'x': x, 'y': y, 'z': z, 'm': m}
    return jsonify(data)

@app.route('/save_coordinates', methods=['POST'])
def save_coordinates():
    global x, y, z, m
    save_coordinates_db(x, y, z, m)
    return jsonify({'status': 'success'})

@app.route('/view_coordinates')
def view_coordinates():
    try:
        conn = sqlite3.connect('coordinates.db')
        c = conn.cursor()
        c.execute("SELECT * FROM coordinates")
        rows = c.fetchall()
        conn.close()
        return render_template('view_coordinates.html', rows=rows)
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
        return render_template('view_coordinates.html', rows=[])

if __name__ == '__main__':
    app.run(debug=True)
