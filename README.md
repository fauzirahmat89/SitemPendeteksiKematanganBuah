# 🍌 Banana Quality Detection System — YOLO & ESP32

Sistem ini mendeteksi kualitas buah pisang (Segar / Busuk) secara otomatis menggunakan kamera, YOLO, ESP32, dan Python Flask.  
Ketika pisang terdeteksi, sistem akan mencatat data ke MySQL dan mengontrol **servo motor** atau **buzzer** melalui ESP32.

---

## 💡 Fitur Utama

- 📸 Deteksi Otomatis menggunakan YOLO.
- 🗄️ Pencatatan Data ke MySQL (`pisang_segar` & `pisang_busuk`).
- 🤖 Kontrol Hardware:  
   - Servo bergerak saat pisang **busuk** terdeteksi.
   - Buzzer berbunyi saat pisang **segar** terdeteksi.
- 🌐 Web Interface dengan Flask untuk menampilkan kamera dan statistik deteksi.

## ⚙️ Teknologi

- YOLO — Object Detection.
- Python + Flask — Web server & pengolahan data.
- MySQL — Database logging.
- ESP32 — Kontrol servo & buzzer.
- OpenCV — Video streaming & image handling.
- SQLAlchemy — ORM untuk database.

---

## 🚀 Cara Instalasi

### 1️⃣ Persiapan Python (PC / Laptop)

```bash
git clone https://github.com/username/banana-quality-detector.git
cd banana-quality-detector
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> Pastikan file `best.pt` (YOLO model) tersedia di direktori yang sama.

---

### 2️⃣ Konfigurasi Database

Buat database `deteksipisang` dengan tabel:

```sql
CREATE DATABASE deteksipisang;
USE deteksipisang;
CREATE TABLE pisang_segar (id INT AUTO_INCREMENT PRIMARY KEY, jumlah INT);
CREATE TABLE pisang_busuk (id INT AUTO_INCREMENT PRIMARY KEY, jumlah INT);
```

---

### 3️⃣ ESP32 Setup

- Upload sketch Arduino di file `esp32_detector.ino`.
- Pastikan WiFi SSID & Password sesuai.
- Sambungkan servo ke pin **GPIO 23**.
- Sambungkan buzzer ke pin **GPIO 13**.

---

### 4️⃣ Menjalankan Server Python

```bash
python app.py
```
Akses melalui browser:  
`http://localhost:5000`

---

## 🎯 Tampilan Web

- `/` — Live video dari kamera dengan deteksi YOLO.
- `/get_counts` — API untuk mengambil total deteksi pisang segar & busuk.
- `/camera_control` — Mengaktifkan atau mematikan kamera.

---

## 📡 Cara Kerja ESP32

- **/control_servo**: Servo akan bergerak 90° selama 1 detik, lalu kembali ke posisi awal.
- **/control_buzzer**: Buzzer akan aktif selama 1 detik, lalu mati otomatis.

ESP32 berkomunikasi dengan Python Flask melalui HTTP POST request.

---

## 📌 Catatan

- Pastikan IP ESP32 dan port database dikonfigurasi sesuai pada script Python.
- YOLO model (`best.pt`) bisa dilatih sendiri atau ganti dengan model deteksi lain sesuai kebutuhan.
- Pastikan kamera terdeteksi di `cv2.VideoCapture()`.

---

## 📷 Contoh Deteksi

> Tambahkan screenshot hasil deteksi YOLO di sini!

---

## 💻 Lisensi

MIT License — bebas digunakan dan dikembangkan, silakan kembangkan sistem ini untuk pertanian atau industri buah lokal! 🚜🍌
