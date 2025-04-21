from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
import cv2
from ultralytics import YOLO
import time
from sqlalchemy import create_engine, MetaData, Table, func
from sqlalchemy.orm import sessionmaker
import requests  # Untuk mengirim request ke ESP32

app = Flask(__name__)

# Load YOLOv9 model
model = YOLO('best.pt')

camera_active = False
detection_counter = 0
threshold_seconds = 3
last_detection_time = 0
countdown = 0

# Setup database connection
DATABASE_URI = 'mysql+pymysql://root:@localhost:5222/deteksipisang'
engine = create_engine(DATABASE_URI)
metadata = MetaData()
metadata.reflect(bind=engine)

pisang_segar = Table('pisang_segar', metadata, autoload_with=engine)
pisang_busuk = Table('pisang_busuk', metadata, autoload_with=engine)

Session = sessionmaker(bind=engine)
session = Session()

# ESP32 IP Address (Ganti dengan IP ESP32 yang kamu catat)
ESP32_IP = 'http://192.168.90.77'

def generate_frames():
    global camera_active, last_detection_time, countdown, detection_counter

    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    while camera_active:
        success, frame = cap.read()
        if not success:
            break
        else:
            results = model.predict(source=frame, conf=0.50, show=False, imgsz=416)
            detected_objects = results[0].boxes

            if detected_objects:
                if time.time() - last_detection_time > threshold_seconds:
                    last_detection_time = time.time()
                    countdown = threshold_seconds
                    detection_counter += 1
                    for box in detected_objects:
                        class_id = box.cls
                        if class_id == 0:  # Pisang busuk
                            insert_query = pisang_busuk.insert().values(jumlah=1)
                            session.execute(insert_query)
                            session.commit()
                            try:
                                requests.post(f'{ESP32_IP}/control_servo', json={'servo': 'on'})
                            except Exception as e:
                                print(f"Error sending servo request to ESP32: {e}")
                        elif class_id == 1:  # Pisang segar
                            insert_query = pisang_segar.insert().values(jumlah=1)
                            session.execute(insert_query)
                            session.commit()
                            try:
                                requests.post(f'{ESP32_IP}/control_buzzer', json={'buzzer': 'on'})
                            except Exception as e:
                                print(f"Error sending buzzer request to ESP32: {e}")
            else:
                countdown = max(0, countdown - (time.time() - last_detection_time))

            annotated_frame = results[0].plot()
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/video_feed')
def video_feed():
    if camera_active:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Camera is off"

@app.route('/camera_control', methods=['POST'])
def camera_control():
    global camera_active
    if 'start' in request.form:
        camera_active = True
    elif 'stop' in request.form:
        camera_active = False
    return redirect(url_for('indexrev'))

@app.route('/get_counts')
def get_counts():
    total_segar = session.query(func.sum(pisang_segar.c.jumlah)).scalar() or 0
    total_busuk = session.query(func.sum(pisang_busuk.c.jumlah)).scalar() or 0
    return jsonify({'total_segar': total_segar, 'total_busuk': total_busuk})

@app.route('/')
def indexrev():
    return render_template('indexrev.html')

@app.route('/carakerjasistem')
def carakerja():
    return render_template('carakerja.html')

if __name__ == "__main__":
    app.run(debug=True)