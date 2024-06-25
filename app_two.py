from flask import Flask, render_template, request
import cv2
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index-two.html')

@app.route('/scan', methods=['POST'])
def scan():
    if request.method == 'POST':
        # Kamerayı aç
        cap = cv2.VideoCapture(0)
        
        # Fotoğraf çek
        ret, frame = cap.read()
        if ret:
            # Fotoğrafı base64'e dönüştür
            _, buffer = cv2.imencode('.jpg', frame)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            img_data = f"data:image/jpeg;base64,{img_base64}"
            
            # Fotoğrafı web arayüzüne gönder
            return render_template('index-two.html', image=img_data)
        else:
            return 'Kamera açılamadı!'
    return 'Geçersiz istek'

if __name__ == '__main__':
    app.run(debug=True)
