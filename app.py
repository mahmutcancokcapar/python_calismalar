from flask import Flask, render_template, jsonify
from random import randint
import threading
import time

app = Flask(__name__)

x, y, z, m = 0, 0, 0, 0
lock = threading.Lock()

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

# Ana sayfay burada render ediliyor
@app.route('/')
def index():
    return render_template('index.html')

# AJAX isteği için JSON veri döndüren route
@app.route('/update_data')
def update_data():
    global x, y, z, m
    data = {'x': x, 'y': y, 'z': z, 'm': m}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
