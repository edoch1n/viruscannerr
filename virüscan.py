#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║         VIRUS SCANNER PRO - Tkinter ile Grafik Arayüz           ║
║                                                                  ║
║  Özellikler:                                                    ║
║  • Sürükle-Bırak desteği                                        ║
║  • 70+ antivirüs motoru                                         ║
║  • Detaylı raporlama                                            ║
║  • Toplu dosya tarama                                           ║
║  • URL tarama                                                   ║
║  • Modern arayüz                                                ║
╚══════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import hashlib
import requests
import json
import os
import sys
import threading
import time
from datetime import datetime
from tkinterdnd2 import DND_FILES, TkinterDnD  # Sürükle-bırak için

# Gerekli kütüphaneleri kontrol et
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# ==================== RENK TEMALARI ====================
COLORS = {
    "bg_dark": "#0a0a0a",
    "bg_card": "#1a1a2e",
    "bg_input": "#16213e",
    "text_primary": "#00ff88",
    "text_secondary": "#aaaaaa",
    "text_error": "#ff4444",
    "text_warning": "#ffaa00",
    "text_success": "#00ff88",
    "border": "#00ff88",
    "button": "#00ff88",
    "button_hover": "#00cc66",
    "progress_bg": "#333333",
    "progress_fg": "#00ff88"
}

class VirusScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ Virus Scanner Pro - 70+ Antivirüs Motoru")
        self.root.geometry("1200x700")
        self.root.configure(bg=COLORS["bg_dark"])
        self.root.minsize(1000, 600)
        
        # API anahtarı (kullanıcı girecek)
        self.api_key = None
        
        # Tarama sonuçları
        self.scan_results = []
        
        # Style
        self.setup_styles()
        
        # UI oluştur
        self.setup_ui()
        
        # Sürükle-bırak desteği
        self.setup_drag_drop()
        
        # API anahtarı sorma
        self.ask_api_key()
    
    def setup_styles(self):
        """ttk stillerini ayarla"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Custom.TFrame", background=COLORS["bg_dark"])
        style.configure("Card.TFrame", background=COLORS["bg_card"], relief="flat")
        
        style.configure("Custom.TLabel", background=COLORS["bg_dark"], foreground=COLORS["text_secondary"])
        style.configure("Title.TLabel", background=COLORS["bg_dark"], foreground=COLORS["text_primary"], font=("Segoe UI", 16, "bold"))
        
        style.configure("Custom.TButton", background=COLORS["button"], foreground=COLORS["bg_dark"], 
                       font=("Segoe UI", 10, "bold"), padding=8)
        style.map("Custom.TButton",
                  background=[('active', COLORS["button_hover"]), ('pressed', COLORS["button_hover"])])
        
        style.configure("Custom.TProgressbar", background=COLORS["progress_fg"], troughcolor=COLORS["progress_bg"])
        
        style.configure("Treeview", background=COLORS["bg_input"], foreground=COLORS["text_secondary"],
                       fieldbackground=COLORS["bg_input"], borderwidth=0)
        style.configure("Treeview.Heading", background=COLORS["bg_card"], foreground=COLORS["text_primary"],
                       font=("Segoe UI", 10, "bold"))
    
    def setup_ui(self):
        """Ana arayüzü oluştur"""
        # Ana container
        main_container = ttk.Frame(self.root, style="Custom.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header
        header_frame = ttk.Frame(main_container, style="Custom.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Logo ve başlık
        title_label = ttk.Label(header_frame, text="🛡️ VIRUS SCANNER PRO", style="Title.TLabel")
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = ttk.Label(header_frame, text="| 70+ Antivirüs Motoru | VirusTotal API v3", style="Custom.TLabel")
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # API durumu
        self.api_status = ttk.Label(header_frame, text="⚠️ API Anahtarı Gerekli", foreground=COLORS["text_warning"])
        self.api_status.pack(side=tk.RIGHT)
        
        # Notebook (sekmeler)
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Sekme 1: Dosya Tarama
        self.file_tab = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.notebook.add(self.file_tab, text="📁 Dosya Tarama")
        self.setup_file_tab()
        
        # Sekme 2: Toplu Tarama
        self.batch_tab = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.notebook.add(self.batch_tab, text="📂 Toplu Tarama")
        self.setup_batch_tab()
        
        # Sekme 3: URL Tarama
        self.url_tab = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.notebook.add(self.url_tab, text="🌐 URL Tarama")
        self.setup_url_tab()
        
        # Sekme 4: Raporlar
        self.report_tab = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.notebook.add(self.report_tab, text="📊 Raporlar")
        self.setup_report_tab()
        
        # Durum çubuğu
        self.status_bar = ttk.Label(main_container, text="Hazır", style="Custom.TLabel", anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def setup_drag_drop(self):
        """Sürükle-bırak desteği"""
        try:
            # Dosya sürükleme alanı
            self.drop_area = tk.Label(self.file_tab, text="📁 DOSYALARI BURAYA SÜRÜKLEYİN\n\nveya\n\nAŞAĞIDAKİ BUTONU KULLANIN",
                                     bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
                                     font=("Segoe UI", 12), height=8, relief="solid", bd=2)
            self.drop_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Sürükle-bırak olayları
            self.drop_area.drop_target_register(DND_FILES)
            self.drop_area.dnd_bind('<<Drop>>', self.on_drop)
        except:
            # TkinterDnD yoksa normal buton kullan
            pass
    
    def setup_file_tab(self):
        """Dosya tarama sekmesi"""
        # Orta alan
        center_frame = ttk.Frame(self.file_tab, style="Custom.TFrame")
        center_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Dosya seçim alanı
        file_frame = ttk.Frame(center_frame, style="Card.TFrame")
        file_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(file_frame, text="Dosya Seç:", style="Custom.TLabel").pack(side=tk.LEFT, padx=10)
        
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, font=("Consolas", 10))
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        browse_btn = ttk.Button(file_frame, text="📂 Gözat", command=self.browse_file, style="Custom.TButton")
        browse_btn.pack(side=tk.RIGHT, padx=10)
        
        # Dosya bilgileri
        info_frame = ttk.LabelFrame(center_frame, text="Dosya Bilgileri", style="Custom.TFrame")
        info_frame.pack(fill=tk.X, pady=10)
        
        self.info_text = scrolledtext.ScrolledText(info_frame, height=8, bg=COLORS["bg_input"],
                                                    fg=COLORS["text_secondary"], font=("Consolas", 9),
                                                    relief="flat", bd=0)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # İlerleme çubuğu
        self.progress = ttk.Progressbar(center_frame, style="Custom.TProgressbar", mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=10)
        
        # Butonlar
        button_frame = ttk.Frame(center_frame, style="Custom.TFrame")
        button_frame.pack(fill=tk.X, pady=10)
        
        self.scan_btn = ttk.Button(button_frame, text="🔍 TARAMAYI BAŞLAT", command=self.start_file_scan,
                                   style="Custom.TButton")
        self.scan_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(button_frame, text="🗑️ Temizle", command=self.clear_info, style="Custom.TButton")
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Sonuç tablosu
        result_frame = ttk.LabelFrame(center_frame, text="Tarama Sonuçları", style="Custom.TFrame")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview
        columns = ("engine", "result", "category")
        self.result_tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=8)
        
        self.result_tree.heading("engine", text="Antivirüs Motoru")
        self.result_tree.heading("result", text="Tespit")
        self.result_tree.heading("category", text="Kategori")
        
        self.result_tree.column("engine", width=200)
        self.result_tree.column("result", width=300)
        self.result_tree.column("category", width=150)
        
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scrollbar.set)
        
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_batch_tab(self):
        """Toplu tarama sekmesi"""
        center_frame = ttk.Frame(self.batch_tab, style="Custom.TFrame")
        center_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Dizin seçimi
        dir_frame = ttk.Frame(center_frame, style="Card.TFrame")
        dir_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(dir_frame, text="Dizin Seç:", style="Custom.TLabel").pack(side=tk.LEFT, padx=10)
        
        self.dir_path_var = tk.StringVar()
        dir_entry = ttk.Entry(dir_frame, textvariable=self.dir_path_var, font=("Consolas", 10))
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        browse_dir_btn = ttk.Button(dir_frame, text="📁 Gözat", command=self.browse_directory, style="Custom.TButton")
        browse_dir_btn.pack(side=tk.RIGHT, padx=10)
        
        # Dosya uzantıları filtresi
        ext_frame = ttk.Frame(center_frame, style="Card.TFrame")
        ext_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(ext_frame, text="Dosya Uzantıları (virgülle ayırın, boş bırakın tüm dosyalar):", 
                 style="Custom.TLabel").pack(side=tk.LEFT, padx=10)
        
        self.ext_var = tk.StringVar()
        ext_entry = ttk.Entry(ext_frame, textvariable=self.ext_var, width=40)
        ext_entry.pack(side=tk.LEFT, padx=10)
        
        # Tarama butonu
        self.batch_scan_btn = ttk.Button(center_frame, text="🔍 DİZİNİ TARA", command=self.start_batch_scan,
                                         style="Custom.TButton")
        self.batch_scan_btn.pack(pady=20)
        
        # Sonuç listesi
        result_frame = ttk.LabelFrame(center_frame, text="Tarama Sonuçları", style="Custom.TFrame")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.batch_result_text = scrolledtext.ScrolledText(result_frame, height=15, bg=COLORS["bg_input"],
                                                            fg=COLORS["text_secondary"], font=("Consolas", 9))
        self.batch_result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def setup_url_tab(self):
        """URL tarama sekmesi"""
        center_frame = ttk.Frame(self.url_tab, style="Custom.TFrame")
        center_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # URL girişi
        url_frame = ttk.Frame(center_frame, style="Card.TFrame")
        url_frame.pack(fill=tk.X, pady=20)
        
        ttk.Label(url_frame, text="URL:", style="Custom.TLabel", font=("Segoe UI", 12)).pack(side=tk.LEFT, padx=15)
        
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, font=("Consolas", 11), width=60)
        url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15)
        
        self.scan_url_btn = ttk.Button(center_frame, text="🌐 URL'Yİ TARA", command=self.start_url_scan,
                                       style="Custom.TButton")
        self.scan_url_btn.pack(pady=20)
        
        # Sonuç
        result_frame = ttk.LabelFrame(center_frame, text="URL Tarama Sonucu", style="Custom.TFrame")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.url_result_text = scrolledtext.ScrolledText(result_frame, height=20, bg=COLORS["bg_input"],
                                                         fg=COLORS["text_secondary"], font=("Consolas", 10))
        self.url_result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def setup_report_tab(self):
        """Raporlar sekmesi"""
        center_frame = ttk.Frame(self.report_tab, style="Custom.TFrame")
        center_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # İstatistikler
        stats_frame = ttk.LabelFrame(center_frame, text="Tarama İstatistikleri", style="Custom.TFrame")
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=8, bg=COLORS["bg_input"],
                                                    fg=COLORS["text_secondary"], font=("Consolas", 10))
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Rapor düğmeleri
        button_frame = ttk.Frame(center_frame, style="Custom.TFrame")
        button_frame.pack(fill=tk.X, pady=10)
        
        save_btn = ttk.Button(button_frame, text="💾 Raporu Kaydet", command=self.save_report, style="Custom.TButton")
        save_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(button_frame, text="🗑️ Geçmişi Temizle", command=self.clear_history, style="Custom.TButton")
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Rapor görüntüleme
        report_frame = ttk.LabelFrame(center_frame, text="Tarama Geçmişi", style="Custom.TFrame")
        report_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.report_text = scrolledtext.ScrolledText(report_frame, height=15, bg=COLORS["bg_input"],
                                                     fg=COLORS["text_secondary"], font=("Consolas", 9))
        self.report_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def ask_api_key(self):
        """API anahtarı sorma penceresi"""
        dialog = tk.Toplevel(self.root)
        dialog.title("VirusTotal API Anahtarı")
        dialog.geometry("500x250")
        dialog.configure(bg=COLORS["bg_dark"])
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="🔑 VirusTotal API Anahtarı", style="Title.TLabel").pack(pady=20)
        ttk.Label(dialog, text="https://www.virustotal.com adresinden ücretsiz API anahtarı alabilirsiniz",
                 style="Custom.TLabel").pack()
        
        api_frame = ttk.Frame(dialog, style="Custom.TFrame")
        api_frame.pack(pady=20)
        
        self.api_key_var = tk.StringVar()
        api_entry = ttk.Entry(api_frame, textvariable=self.api_key_var, width=50, show="*")
        api_entry.pack(side=tk.LEFT, padx=10)
        
        def save_key():
            self.api_key = self.api_key_var.get()
            if self.api_key:
                dialog.destroy()
                self.api_status.config(text="✅ API Bağlı", foreground=COLORS["text_success"])
                self.update_status("API anahtarı başarıyla yüklendi")
            else:
                messagebox.showwarning("Uyarı", "API anahtarı girmeden devam edemezsiniz!")
        
        save_btn = ttk.Button(dialog, text="Kaydet", command=save_key, style="Custom.TButton")
        save_btn.pack(pady=10)
    
    def browse_file(self):
        """Dosya seç"""
        file_path = filedialog.askopenfilename(title="Dosya Seç")
        if file_path:
            self.file_path_var.set(file_path)
            self.show_file_info(file_path)
    
    def browse_directory(self):
        """Dizin seç"""
        dir_path = filedialog.askdirectory(title="Dizin Seç")
        if dir_path:
            self.dir_path_var.set(dir_path)
    
    def on_drop(self, event):
        """Sürükle-bırak olayı"""
        files = event.data
        if files:
            # TkinterDnD formatını temizle
            files = files.strip('{}')
            file_path = files
            self.file_path_var.set(file_path)
            self.show_file_info(file_path)
    
    def show_file_info(self, file_path):
        """Dosya bilgilerini göster"""
        if not os.path.exists(file_path):
            return
        
        self.info_text.delete(1.0, tk.END)
        
        # Dosya bilgilerini hesapla
        file_size = os.path.getsize(file_path)
        if file_size < 1024:
            size_str = f"{file_size} bytes"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.2f} KB"
        else:
            size_str = f"{file_size / (1024 * 1024):.2f} MB"
        
        # Hash hesapla
        md5_hash = hashlib.md5()
        sha1_hash = hashlib.sha1()
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                md5_hash.update(chunk)
                sha1_hash.update(chunk)
                sha256_hash.update(chunk)
        
        info = f"""
╔══════════════════════════════════════════════════════════════╗
║ DOSYA BİLGİLERİ                                              ║
╠══════════════════════════════════════════════════════════════╣
║ 📄 Dosya Adı: {os.path.basename(file_path)}
║ 📁 Dizin: {os.path.dirname(file_path)}
║ 📦 Boyut: {size_str}
║ 🔐 MD5: {md5_hash.hexdigest()}
║ 🔐 SHA1: {sha1_hash.hexdigest()}
║ 🔐 SHA256: {sha256_hash.hexdigest()}
║ 🕐 Son Değiştirme: {datetime.fromtimestamp(os.path.getmtime(file_path))}
╚══════════════════════════════════════════════════════════════╝
        """
        self.info_text.insert(1.0, info)
    
    def clear_info(self):
        """Bilgi alanını temizle"""
        self.info_text.delete(1.0, tk.END)
        self.file_path_var.set("")
        self.result_tree.delete(*self.result_tree.get_children())
    
    def update_status(self, message):
        """Durum çubuğunu güncelle"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
    
    def start_file_scan(self):
        """Dosya taramasını başlat (thread ile)"""
        if not self.api_key:
            messagebox.showerror("Hata", "API anahtarı gerekli!")
            return
        
        file_path = self.file_path_var.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Hata", "Geçerli bir dosya seçin!")
            return
        
        self.scan_btn.config(state=tk.DISABLED, text="⏳ TARANIYOR...")
        self.progress.start(10)
        self.result_tree.delete(*self.result_tree.get_children())
        
        thread = threading.Thread(target=self.scan_file_thread, args=(file_path,))
        thread.daemon = True
        thread.start()
    
    def scan_file_thread(self, file_path):
        """Dosya tarama işlemi (thread içinde)"""
        try:
            # Hash hesapla
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    sha256_hash.update(chunk)
            file_hash = sha256_hash.hexdigest()
            
            self.update_status(f"Hash hesaplandı: {file_hash[:32]}...")
            
            # VirusTotal sorgula
            url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
            headers = {"x-apikey": self.api_key}
            
            response = requests.get(url, headers=headers, timeout=30)
            
            self.root.after(0, self.process_scan_result, response, file_path, file_hash)
            
        except Exception as e:
            self.root.after(0, self.scan_error, str(e))
    
    def process_scan_result(self, response, file_path, file_hash):
        """Tarama sonucunu işle"""
        self.progress.stop()
        self.scan_btn.config(state=tk.NORMAL, text="🔍 TARAMAYI BAŞLAT")
        
        if response.status_code == 200:
            data = response.json()
            attributes = data.get("data", {}).get("attributes", {})
            stats = attributes.get("last_analysis_stats", {})
            
            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            
            # Sonuçları treeview'a ekle
            results = attributes.get("last_analysis_results", {})
            
            for engine, result in results.items():
                category = result.get("category", "undetected")
                if category == "malicious":
                    tag = "malicious"
                elif category == "suspicious":
                    tag = "suspicious"
                else:
                    tag = "clean"
                
                self.result_tree.insert("", tk.END, values=(
                    engine,
                    result.get("result", "Clean"),
                    category.upper()
                ), tags=(tag,))
            
            # Renk tagları
            self.result_tree.tag_configure("malicious", background="#330000", foreground="#ff4444")
            self.result_tree.tag_configure("suspicious", background="#332200", foreground="#ffaa00")
            self.result_tree.tag_configure("clean", background="#003300", foreground="#00ff88")
            
            # Özet bilgi
            result_text = f"""
╔══════════════════════════════════════════════════════════════╗
║ TARAMA SONUCU                                                ║
╠══════════════════════════════════════════════════════════════╣
║ 📄 Dosya: {os.path.basename(file_path)}
║ 🔐 SHA256: {file_hash[:32]}...
║                                                              ║
║ 🔴 Zararlı Tespiti: {malicious}
║ 🟡 Şüpheli Tespit: {suspicious}
║ 🟢 Temiz Motor: {stats.get("harmless", 0)}
║ ⚪ Tespit Edilemeyen: {stats.get("undetected", 0)}
║                                                              ║
║ 🛡️ TOPLAN MOTOR: {stats.get("harmless", 0) + stats.get("malicious", 0) + stats.get("suspicious", 0) + stats.get("undetected", 0)}
╚══════════════════════════════════════════════════════════════╝
            """
            
            self.info_text.insert(tk.END, "\n" + result_text)
            
            if malicious > 0:
                self.update_status(f"⚠️ UYARI: {malicious} antivirüs dosyayı zararlı olarak tespit etti!")
                messagebox.showwarning("Tehdit Tespit Edildi!", 
                                      f"Dosya {malicious} antivirüs motoru tarafından ZARARLI olarak tespit edildi!")
            else:
                self.update_status("✅ Tarama tamamlandı. Tehdit tespit edilmedi.")
            
            # Geçmişe ekle
            self.scan_results.append({
                "file": file_path,
                "timestamp": str(datetime.now()),
                "malicious": malicious,
                "suspicious": suspicious,
                "total_engines": stats.get("harmless", 0) + malicious + suspicious + stats.get("undetected", 0)
            })
            
            self.update_report_tab()
            
        elif response.status_code == 404:
            self.info_text.insert(tk.END, "\n[!] Dosya VirusTotal veritabanında bulunamadı. Yükleme gerekli (Premium API gerektirir).")
            self.update_status("Dosya veritabanında bulunamadı")
        else:
            self.info_text.insert(tk.END, f"\n[!] API Hatası: {response.status_code}")
            self.update_status(f"API Hatası: {response.status_code}")
    
    def scan_error(self, error):
        """Tarama hatası"""
        self.progress.stop()
        self.scan_btn.config(state=tk.NORMAL, text="🔍 TARAMAYI BAŞLAT")
        self.update_status(f"Hata: {error}")
        messagebox.showerror("Tarama Hatası", str(error))
    
    def start_batch_scan(self):
        """Toplu tarama başlat"""
        dir_path = self.dir_path_var.get()
        if not dir_path or not os.path.isdir(dir_path):
            messagebox.showerror("Hata", "Geçerli bir dizin seçin!")
            return
        
        self.batch_scan_btn.config(state=tk.DISABLED, text="⏳ TARANIYOR...")
        self.batch_result_text.delete(1.0, tk.END)
        
        thread = threading.Thread(target=self.batch_scan_thread, args=(dir_path,))
        thread.daemon = True
        thread.start()
    
    def batch_scan_thread(self, dir_path):
        """Toplu tarama thread'i"""
        extensions = [ext.strip().lower() for ext in self.ext_var.get().split(",") if ext.strip()]
        
        files_to_scan = []
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if extensions:
                    if any(file.lower().endswith(ext) for ext in extensions):
                        files_to_scan.append(os.path.join(root, file))
                else:
                    files_to_scan.append(os.path.join(root, file))
        
        self.root.after(0, lambda: self.batch_result_text.insert(tk.END, f"📁 {len(files_to_scan)} dosya bulundu.\n\n"))
        
        for i, file_path in enumerate(files_to_scan[:20]):  # API limiti için 20 dosya ile sınırlı
            # Hash hesapla
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    sha256_hash.update(chunk)
            file_hash = sha256_hash.hexdigest()
            
            url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
            headers = {"x-apikey": self.api_key}
            
            try:
                response = requests.get(url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                    malicious = stats.get("malicious", 0)
                    
                    if malicious > 0:
                        status = f"🦠 ZARARLI ({malicious} tespit)"
                    else:
                        status = "✅ Temiz"
                    
                    result_line = f"[{i+1}/{len(files_to_scan)}] {os.path.basename(file_path)}: {status}\n"
                    self.root.after(0, lambda l=result_line: self.batch_result_text.insert(tk.END, l))
                    
                time.sleep(0.5)  # API limiti
                
            except Exception as e:
                self.root.after(0, lambda: self.batch_result_text.insert(tk.END, f"Hata: {e}\n"))
        
        self.root.after(0, lambda: self.batch_scan_btn.config(state=tk.NORMAL, text="🔍 DİZİNİ TARA"))
        self.root.after(0, lambda: self.update_status("Toplu tarama tamamlandı"))
    
    def start_url_scan(self):
        """URL tarama başlat"""
        url = self.url_var.get()
        if not url:
            messagebox.showerror("Hata", "URL girin!")
            return
        
        self.scan_url_btn.config(state=tk.DISABLED, text="⏳ TARANIYOR...")
        self.url_result_text.delete(1.0, tk.END)
        
        thread = threading.Thread(target=self.url_scan_thread, args=(url,))
        thread.daemon = True
        thread.start()
    
    def url_scan_thread(self, url):
        """URL tarama thread'i"""
        try:
            headers = {"x-apikey": self.api_key}
            
            # URL'yi gönder
            scan_url = "https://www.virustotal.com/api/v3/urls"
            data = {"url": url}
            
            response = requests.post(scan_url, headers=headers, data=data, timeout=30)
            
            if response.status_code == 200:
                result_data = response.json()
                analysis_id = result_data.get("data", {}).get("id")
                
                # Analizi bekle
                time.sleep(15)
                
                # Sonucu al
                result_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
                result_response = requests.get(result_url, headers=headers, timeout=30)
                
                if result_response.status_code == 200:
                    analysis_data = result_response.json()
                    stats = analysis_data.get("data", {}).get("attributes", {}).get("stats", {})
                    
                    malicious = stats.get("malicious", 0)
                    
                    result_text = f"""
╔══════════════════════════════════════════════════════════════╗
║ URL TARAMA SONUCU                                            ║
╠══════════════════════════════════════════════════════════════╣
║ 🌐 URL: {url}
║                                                              ║
║ 🔴 Zararlı: {malicious}
║ 🟡 Şüpheli: {stats.get("suspicious", 0)}
║ 🟢 Temiz: {stats.get("harmless", 0)}
║ ⚪ Tespit Edilemeyen: {stats.get("undetected", 0)}
║                                                              ║
║ 📊 SONUÇ: {"🦠 TEHLİKELİ" if malicious > 0 else "✅ GÜVENLİ"}
╚══════════════════════════════════════════════════════════════╝
                    """
                    self.root.after(0, lambda: self.url_result_text.insert(1.0, result_text))
                    
                    if malicious > 0:
                        self.root.after(0, lambda: messagebox.showwarning("URL Tehdidi", f"URL {malicious} antivirüs tarafından engellendi!"))
                    
                else:
                    self.root.after(0, lambda: self.url_result_text.insert(1.0, f"API Hatası: {result_response.status_code}"))
            else:
                self.root.after(0, lambda: self.url_result_text.insert(1.0, f"API Hatası: {response.status_code}\n{response.text}"))
                
        except Exception as e:
            self.root.after(0, lambda: self.url_result_text.insert(1.0, f"Hata: {str(e)}"))
        
        self.root.after(0, lambda: self.scan_url_btn.config(state=tk.NORMAL, text="🌐 URL'Yİ TARA"))
    
    def update_report_tab(self):
        """Rapor sekmesini güncelle"""
        self.report_text.delete(1.0, tk.END)
        
        for result in self.scan_results:
            report_line = f"""
[{result['timestamp']}]
Dosya: {result['file']}
Zararlı: {result['malicious']} | Şüpheli: {result['suspicious']} | Toplam Motor: {result['total_engines']}
{'═' * 50}
"""
            self.report_text.insert(tk.END, report_line)
        
        # İstatistikler
        total_scans = len(self.scan_results)
        malicious_files = sum(1 for r in self.scan_results if r.get("malicious", 0) > 0)
        
        stats = f"""
╔══════════════════════════════════════════════════════════════╗
║ TARAMA İSTATİSTİKLERİ                                        ║
╠══════════════════════════════════════════════════════════════╣
║ Toplam Tarama: {total_scans}
║ Zararlı Dosya: {malicious_files}
║ Temiz Dosya: {total_scans - malicious_files}
║                                                              ║
║ Son Tarama: {self.scan_results[-1]['timestamp'] if self.scan_results else 'Henüz yok'}
╚══════════════════════════════════════════════════════════════╝
        """
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats)
    
    def save_report(self):
        """Raporu kaydet"""
        if not self.scan_results:
            messagebox.showwarning("Uyarı", "Kaydedilecek rapor yok!")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("Text files", "*.txt")])
        
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.scan_results, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Başarılı", f"Rapor kaydedildi: {file_path}")
    
    def clear_history(self):
        """Geçmişi temizle"""
        self.scan_results = []
        self.update_report_tab()
        self.update_status("Tarama geçmişi temizlendi")

# ==================== ANA UYGULAMA ====================
def main():
    # TkinterDnD desteği (sürükle-bırak için)
    try:
        from tkinterdnd2 import TkinterDnD
        root = TkinterDnD.Tk()
    except ImportError:
        root = tk.Tk()
        print("[!] Sürükle-bırak desteği için: pip install tkinterdnd2")
    
    app = VirusScannerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
