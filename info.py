#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║     ULTIMATE LABORATUVAR ARACI - TEK DOSYA (v3.0)               ║
║     Sadece eğitim ve izole laboratuvar ortamı içindir           ║
║     Telefon + Bilgisayar entegrasyonu                           ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import socket
import subprocess
import webbrowser
import threading
import datetime
import time
import uuid
from datetime import datetime

# Flask ve ek kütüphaneler
try:
    from flask import Flask, render_template_string, send_file, request, jsonify
    import requests
except ImportError:
    print("[!] Gerekli kütüphaneler yükleniyor...")
    subprocess.run([sys.executable, "-m", "pip", "install", "flask", "requests"])
    from flask import Flask, render_template_string, send_file, request, jsonify
    import requests

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# ==================== TELEFON İÇİN SAHTE PDF SAYFASI ====================
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
        .header p { font-size: 14px; opacity: 0.9; }
        .content { padding: 30px; text-align: center; }
        .pdf-icon {
            font-size: 80px;
            margin-bottom: 20px;
        }
        .info-box {
            background: #f0fdf4;
            border-left: 4px solid #22c55e;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: left;
        }
        .info-box p { margin: 5px 0; color: #166534; }
        button {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            width: 100%;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        button:active { transform: translateY(0); }
        .warning {
            font-size: 11px;
            color: #999;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📘 TYT Biyoloji Kampı 2025</h1>
            <p>Full PDF - Konu Anlatımı + Soru Bankası</p>
        </div>
        <div class="content">
            <div class="pdf-icon">📄📚</div>
            <div class="info-box">
                <p>✅ 500+ Sayfa</p>
                <p>✅ Tüm konular özet</p>
                <p>✅ 2000+ çözümlü soru</p>
                <p>✅ Akıllı tahta uyumlu</p>
            </div>
            <form action="/indir" method="POST">
                <button type="submit">📥 PDF'i Hemen İndir (EXE)</button>
            </form>
            <p class="warning">⚠️ Bu dosya sadece laboratuvar test içindir. Gerçek içerik değildir.</p>
        </div>
    </div>
</body>
</html>
"""

# ==================== TELEFONA İNECEK TEST DOSYASI ====================
TEST_DOSYA_KODU = '''
import tkinter as tk
from tkinter import messagebox
import platform
import socket
from datetime import datetime

def main():
    root = tk.Tk()
    root.withdraw()
    
    bilgi = f"Laboratuvar Test Dosyası\\n\\nCihaz: {platform.system()} {platform.release()}\\nHostname: {socket.gethostname()}\\nTarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\nBu bir eğitim testidir.\\nHiçbir veri toplanmamıştır."
    
    messagebox.showinfo("🔬 Laboratuvar Test", bilgi)
    root.destroy()

if __name__ == "__main__":
    main()
'''

# ==================== EĞİTİM ARAÇLARI (BİLGİSAYAR) ====================
class EgitimAraclari:
    
    @staticmethod
    def ip_konum(ip=None):
        """IP adresine göre konum bilgisi"""
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
                    "bolge": data['regionName'],
                    "enlem": data['lat'],
                    "boylam": data['lon'],
                    "isp": data['isp'],
                    "posta_kodu": data['zip'],
                    "zaman_dilimi": data['timezone']
                }
            return {"hata": "IP bulunamadı"}
        except Exception as e:
            return {"hata": str(e)}
    
    @staticmethod
    def kendi_ip():
        """Kendi genel IP'ni bul"""
        try:
            ip = requests.get('https://api.ipify.org').text
            return ip
        except:
            return "IP alınamadı"
    
    @staticmethod
    def sim_simulasyonu():
        """SIM bilgisi simülasyonu (eğitim için)"""
        return {
            "sim_durumu": "Simülasyon modu - Gerçek SIM verisi alınmamıştır",
            "mcc_mnc_ornek": "28601 (Türkiye - Turkcell)",
            "operador_ornek": "Turkcell / Vodafone / Türk Telekom",
            "telefon_numarasi_ornek": "+90 5XX XXX XX XX",
            "sim_seri_no_ornek": "8939012345678901234F",
            "not": "Bu veriler eğitim amaçlı örneklerdir. Gerçek SIM bilgisi için root/jailbreak gerekir."
        }
    
    @staticmethod
    def adres_bul(enlem, boylam):
        """Koordinatlardan adres bulma"""
        try:
            url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={enlem}&lon={boylam}"
            response = requests.get(url, headers={'User-Agent': 'EgitimLab/1.0'})
            data = response.json()
            if 'display_name' in data:
                return {
                    "adres": data['display_name'],
                    "ulke": data.get('address', {}).get('country', ''),
                    "sehir": data.get('address', {}).get('city', data.get('address', {}).get('town', '')),
                    "cadde": data.get('address', {}).get('road', '')
                }
            return {"hata": "Adres bulunamadı"}
        except Exception as e:
            return {"hata": str(e)}
    
    @staticmethod
    def port_tara(hedef, portlar=[80, 443, 22, 21, 8080]):
        """Basit port tarama (eğitim amaçlı)"""
        acik_portlar = []
        for port in portlar:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                sonuc = sock.connect_ex((hedef, port))
                if sonuc == 0:
                    acik_portlar.append(port)
                sock.close()
            except:
                pass
        return {"hedef": hedef, "acik_portlar": acik_portlar}
    
    @staticmethod
    def dns_sorgula(domain):
        """DNS sorgulama"""
        try:
            ip = socket.gethostbyname(domain)
            return {"domain": domain, "ip": ip}
        except:
            return {"hata": "DNS çözümlenemedi"}
    
    @staticmethod
    def whois_sorgula(domain):
        """Basit whois sorgusu (eğitim)"""
        try:
            result = subprocess.run(['whois', domain], capture_output=True, text=True, timeout=3)
            return {"whois": result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout}
        except:
            return {"hata": "whois komutu çalıştırılamadı"}
    
    @staticmethod
    def ping_test(hedef):
        """Ping testi"""
        try:
            param = '-n' if os.name == 'nt' else '-c'
            result = subprocess.run(['ping', param, '1', hedef], capture_output=True, text=True, timeout=3)
            return {"hedef": hedef, "durum": "başarılı" if result.returncode == 0 else "başarısız"}
        except:
            return {"hata": "Ping başarısız"}

# ==================== FLASK ROTALARI ====================
@app.route('/')
def index():
    """Telefon için sahte PDF indirme sayfası"""
    return render_template_string(PHISHING_PAGE)

@app.route('/indir', methods=['POST'])
def indir():
    """Telefona test dosyası indirme"""
    temp_py = os.path.join(DOWNLOAD_FOLDER, f"test_{uuid.uuid4().hex}.py")
    with open(temp_py, "w", encoding="utf-8") as f:
        f.write(TEST_DOSYA_KODU)
    
    exe_name = "TYT_Biyoloji_Kampi_Full_PDF.exe"
    output_exe = os.path.join(DOWNLOAD_FOLDER, exe_name)
    
    try:
        subprocess.run([
            "pyinstaller", "--onefile", "--noconsole",
            "--name", "TYT_Biyoloji_Kampi_Full_PDF",
            "--distpath", DOWNLOAD_FOLDER,
            "--workpath", "/tmp/build",
            "--specpath", "/tmp/spec",
            temp_py
        ], capture_output=True, timeout=30)
        
        built_exe = os.path.join(DOWNLOAD_FOLDER, "TYT_Biyoloji_Kampi_Full_PDF", "TYT_Biyoloji_Kampi_Full_PDF.exe")
        if os.path.exists(built_exe):
            os.rename(built_exe, output_exe)
        
        return send_file(output_exe, as_attachment=True, download_name=exe_name)
    except Exception as e:
        return f"Dosya oluşturulamadı: {e}"
    finally:
        if os.path.exists(temp_py):
            os.remove(temp_py)

# ==================== BİLGİSAYAR ARAYÜZÜ (HTML) ====================
LAB_ARAYUZ = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔬 Laboratuvar Eğitim Aracı</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            color: white;
        }
        .navbar {
            background: rgba(0,0,0,0.5);
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }
        .navbar h1 { font-size: 24px; }
        .navbar .info { font-size: 12px; opacity: 0.8; }
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
            font-size: 14px;
        }
        input::placeholder { color: rgba(255,255,255,0.5); }
        button {
            background: linear-gradient(135deg, #00ff88, #00cc66);
            color: #1a1a2e;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.2s;
            width: 100%;
        }
        button:hover { transform: scale(1.02); opacity: 0.9; }
        .sonuc {
            background: rgba(0,0,0,0.5);
            border-radius: 10px;
            padding: 15px;
            margin-top: 15px;
            font-family: monospace;
            font-size: 12px;
            overflow-x: auto;
            white-space: pre-wrap;
            word-break: break-all;
        }
        .status {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0,0,0,0.7);
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 11px;
        }
        hr { margin: 20px 0; border-color: rgba(255,255,255,0.1); }
        .footer { text-align: center; padding: 20px; font-size: 12px; opacity: 0.6; }
        .quick-ip {
            background: rgba(0,255,136,0.2);
            border: 1px solid #00ff88;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <h1>🔬 Laboratuvar Eğitim Aracı v3.0</h1>
        <div class="info">📡 Telefon Payload: http://<span id="localIp">...</span>:5000 | 🖥️ Eğitim Araçları</div>
    </div>
    <div class="container">
        <div class="grid">
            <!-- IP Konum -->
            <div class="card">
                <h3>📍 IP Konum Bulma</h3>
                <input type="text" id="ipInput" placeholder="IP adresi (boş bırakırsanız kendi IP'niz)">
                <button onclick="ipKonum()">🔍 Konumu Getir</button>
                <div id="ipSonuc" class="sonuc">Henüz sorgu yapılmadı...</div>
            </div>
            
            <!-- Kendi IP -->
            <div class="card quick-ip">
                <h3>🌐 Kendi IP Adresin</h3>
                <button onclick="kendiIp()">🆔 IP'mi Göster</button>
                <div id="ipKendiSonuc" class="sonuc">Henüz sorgu yapılmadı...</div>
            </div>
            
            <!-- SIM Simülasyonu -->
            <div class="card">
                <h3>📱 SIM Bilgisi (Simülasyon)</h3>
                <button onclick="simBilgisi()">📲 SIM Bilgilerini Göster</button>
                <div id="simSonuc" class="sonuc">Henüz sorgu yapılmadı...</div>
            </div>
            
            <!-- Adres Bul -->
            <div class="card">
                <h3>🏠 Koordinattan Adres Bul</h3>
                <input type="text" id="latInput" placeholder="Enlem (örnek: 41.0082)">
                <input type="text" id="lonInput" placeholder="Boylam (örnek: 28.9784)">
                <button onclick="adresBul()">📍 Adresi Getir</button>
                <div id="adresSonuc" class="sonuc">Henüz sorgu yapılmadı...</div>
            </div>
            
            <!-- Port Tarama -->
            <div class="card">
                <h3>🔌 Port Tarama</h3>
                <input type="text" id="portHedef" placeholder="Hedef IP (örn: google.com)">
                <input type="text" id="portListesi" placeholder="Portlar (örn: 80,443,22)">
                <button onclick="portTara()">🔍 Tara</button>
                <div id="portSonuc" class="sonuc">Henüz sorgu yapılmadı...</div>
            </div>
            
            <!-- DNS Sorgula -->
            <div class="card">
                <h3>🌍 DNS Sorgula</h3>
                <input type="text" id="dnsDomain" placeholder="Domain (örn: google.com)">
                <button onclick="dnsSorgula()">🔎 Sorgula</button>
                <div id="dnsSonuc" class="sonuc">Henüz sorgu yapılmadı...</div>
            </div>
            
            <!-- Ping Test -->
            <div class="card">
                <h3>📡 Ping Testi</h3>
                <input type="text" id="pingHedef" placeholder="Hedef IP/Domain">
                <button onclick="pingTest()">🏓 Ping At</button>
                <div id="pingSonuc" class="sonuc">Henüz sorgu yapılmadı...</div>
            </div>
            
            <!-- Whois -->
            <div class="card">
                <h3>📋 Whois Sorgula</h3>
                <input type="text" id="whoisDomain" placeholder="Domain">
                <button onclick="whoisSorgula()">🔎 Sorgula</button>
                <div id="whoisSonuc" class="sonuc">Henüz sorgu yapılmadı...</div>
            </div>
        </div>
        
        <hr>
        
        <div class="card">
            <h3>📊 Log / Sorgu Geçmişi</h3>
            <div id="logAlan" class="sonuc" style="max-height: 200px; overflow-y: auto;">Log boş...</div>
            <button onclick="logTemizle()" style="margin-top: 10px;">🗑️ Log Temizle</button>
        </div>
        
        <div class="footer">
            ⚠️ Bu araç SADECE eğitim ve izole laboratuvar ortamı içindir. Tüm sorgular local olarak kaydedilir.
        </div>
    </div>
    <div class="status" id="status">✅ Sistem Hazır</div>
    
    <script>
        let logList = [];
        
        function addLog(text) {
            const timestamp = new Date().toLocaleTimeString();
            logList.unshift(`[${timestamp}] ${text}`);
            if (logList.length > 20) logList.pop();
            document.getElementById('logAlan').innerHTML = logList.join('<br>');
        }
        
        async function apiCall(endpoint, data) {
            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                return await response.json();
            } catch(e) {
                addLog(`❌ Hata: ${e.message}`);
                return { hata: e.message };
            }
        }
        
        async function ipKonum() {
            const ip = document.getElementById('ipInput').value;
            addLog(`📍 IP konum sorgusu: ${ip || 'kendi IP'}`);
            const result = await apiCall('/api/ip_konum', { ip });
            document.getElementById('ipSonuc').innerHTML = JSON.stringify(result, null, 2);
        }
        
        async function kendiIp() {
            addLog(`🌐 Kendi IP sorgulanıyor...`);
            const result = await apiCall('/api/kendi_ip', {});
            document.getElementById('ipKendiSonuc').innerHTML = JSON.stringify(result, null, 2);
        }
        
        async function simBilgisi() {
            addLog(`📱 SIM simülasyonu`);
            const result = await apiCall('/api/sim_simulasyonu', {});
            document.getElementById('simSonuc').innerHTML = JSON.stringify(result, null, 2);
        }
        
        async function adresBul() {
            const lat = document.getElementById('latInput').value;
            const lon = document.getElementById('lonInput').value;
            addLog(`🏠 Adres sorgusu: ${lat}, ${lon}`);
            const result = await apiCall('/api/adres_bul', { lat, lon });
            document.getElementById('adresSonuc').innerHTML = JSON.stringify(result, null, 2);
        }
        
        async function portTara() {
            const hedef = document.getElementById('portHedef').value;
            const portlar = document.getElementById('portListesi').value;
            addLog(`🔌 Port tarama: ${hedef} - Portlar: ${portlar || 'varsayılan'}`);
            const result = await apiCall('/api/port_tara', { hedef, portlar });
            document.getElementById('portSonuc').innerHTML = JSON.stringify(result, null, 2);
        }
        
        async function dnsSorgula() {
            const domain = document.getElementById('dnsDomain').value;
            addLog(`🌍 DNS sorgusu: ${domain}`);
            const result = await apiCall('/api/dns_sorgula', { domain });
            document.getElementById('dnsSonuc').innerHTML = JSON.stringify(result, null, 2);
        }
        
        async function pingTest() {
            const hedef = document.getElementById('pingHedef').value;
            addLog(`📡 Ping testi: ${hedef}`);
            const result = await apiCall('/api/ping_test', { hedef });
            document.getElementById('pingSonuc').innerHTML = JSON.stringify(result, null, 2);
        }
        
        async function whoisSorgula() {
            const domain = document.getElementById('whoisDomain').value;
            addLog(`📋 Whois sorgusu: ${domain}`);
            const result = await apiCall('/api/whois_sorgula', { domain });
            document.getElementById('whoisSonuc').innerHTML = JSON.stringify(result, null, 2);
        }
        
        function logTemizle() {
            logList = [];
            document.getElementById('logAlan').innerHTML = 'Log temizlendi.';
            addLog('Loglar temizlendi');
        }
        
        // Local IP gösterimi
        fetch('/api/kendi_ip')
            .then(r => r.json())
            .then(data => {
                document.getElementById('localIp').innerText = data.ip || '...';
            });
    </script>
</body>
</html>
"""

# ==================== API ROTALARI ====================
egitim = EgitimAraclari()

@app.route('/lab')
def lab_arayuz():
    """Bilgisayar için eğitim arayüzü"""
    return render_template_string(LAB_ARAYUZ)

@app.route('/api/ip_konum', methods=['POST'])
def api_ip_konum():
    data = request.json
    ip = data.get('ip')
    result = egitim.ip_konum(ip if ip else None)
    return jsonify(result)

@app.route('/api/kendi_ip', methods=['POST'])
def api_kendi_ip():
    result = {"ip": egitim.kendi_ip()}
    return jsonify(result)

@app.route('/api/sim_simulasyonu', methods=['POST'])
def api_sim():
    result = egitim.sim_simulasyonu()
    return jsonify(result)

@app.route('/api/adres_bul', methods=['POST'])
def api_adres():
    data = request.json
    lat = data.get('lat')
    lon = data.get('lon')
    result = egitim.adres_bul(lat, lon)
    return jsonify(result)

@app.route('/api/port_tara', methods=['POST'])
def api_port():
    data = request.json
    hedef = data.get('hedef')
    portlar_str = data.get('portlar')
    if portlar_str:
        portlar = [int(p.strip()) for p in portlar_str.split(',')]
    else:
        portlar = [80, 443, 22, 21, 8080]
    result = egitim.port_tara(hedef, portlar)
    return jsonify(result)

@app.route('/api/dns_sorgula', methods=['POST'])
def api_dns():
    data = request.json
    domain = data.get('domain')
    result = egitim.dns_sorgula(domain)
    return jsonify(result)

@app.route('/api/whois_sorgula', methods=['POST'])
def api_whois():
    data = request.json
    domain = data.get('domain')
    result = egitim.whois_sorgula(domain)
    return jsonify(result)

@app.route('/api/ping_test', methods=['POST'])
def api_ping():
    data = request.json
    hedef = data.get('hedef')
    result = egitim.ping_test(hedef)
    return jsonify(result)

# ==================== ANA BAŞLATICI ====================
def open_browser():
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000/lab')

if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════════╗
║     ULTIMATE LABORATUVAR ARACI - TEK DOSYA (v3.0)               ║
║                                                                  ║
║  📱 TELEFON İÇİN:                                               ║
║     http://<BILGISAYAR_IP>:5000                                 ║
║                                                                  ║
║  💻 BİLGİSAYAR EĞİTİM ARAYÜZÜ:                                  ║
║     http://localhost:5000/lab                                   ║
║                                                                  ║
║  🛠️ ARAÇLAR: IP Konum | SIM Simülasyonu | Adres Bul |          ║
║            Port Tarama | DNS | Ping | Whois                     ║
║                                                                  ║
║  ⚠️ SADECE EĞİTİM VE İZOLE LABORATUVAR İÇİNDİR                 ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Tarayıcıyı otomatik aç
    threading.Thread(target=open_browser, daemon=True).start()
    
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
