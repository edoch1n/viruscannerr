<!DOCTYPE html>
<html>
<head>
<style>
@keyframes glow {
    0% { text-shadow: 0 0 5px #00ff88; }
    50% { text-shadow: 0 0 20px #00ff88, 0 0 30px #00aa44; }
    100% { text-shadow: 0 0 5px #00ff88; }
}

@keyframes slideIn {
    from { transform: translateX(-100px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

@keyframes typing {
    from { width: 0; }
    to { width: 100%; }
}

@keyframes blink-cursor {
    from, to { border-color: transparent; }
    50% { border-color: #00ff88; }
}

body {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
    color: #00ff88;
    font-family: 'Segoe UI', 'Courier New', monospace;
    padding: 30px;
    margin: 0;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    background: rgba(0,0,0,0.7);
    border-radius: 20px;
    padding: 40px;
    border: 1px solid #00ff88;
    box-shadow: 0 0 50px rgba(0,255,136,0.2);
}

h1 {
    text-align: center;
    font-size: 48px;
    animation: glow 2s infinite, slideIn 1s ease;
}

h1::before {
    content: "🛡️ ";
}

h2 {
    color: #ff6600;
    border-left: 4px solid #00ff88;
    padding-left: 15px;
    margin-top: 30px;
}

.badge-container {
    text-align: center;
    margin: 20px 0;
    animation: pulse 2s infinite;
}

.badge {
    display: inline-block;
    background: #1a1a2e;
    border: 1px solid #00ff88;
    border-radius: 20px;
    padding: 8px 16px;
    margin: 5px;
    font-size: 14px;
    transition: all 0.3s;
}

.badge:hover {
    transform: scale(1.1);
    background: #00ff88;
    color: #0a0a0a;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin: 30px 0;
}

.feature-card {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    transition: transform 0.3s;
    border: 1px solid #00ff88;
}

.feature-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 10px 30px rgba(0,255,136,0.3);
}

.feature-card .icon {
    font-size: 48px;
    display: block;
    animation: float 3s infinite;
}

.feature-card h3 {
    color: #00ff88;
    margin: 10px 0;
}

.screenshot {
    background: #0a0a0a;
    border-radius: 15px;
    padding: 30px;
    margin: 30px 0;
    text-align: center;
    border: 2px dashed #00ff88;
    animation: pulse 3s infinite;
}

.screenshot-placeholder {
    background: linear-gradient(45deg, #1a1a2e, #2a2a3e);
    border-radius: 10px;
    padding: 60px;
    font-family: monospace;
    color: #666;
}

code {
    background: #0a0a0a;
    border: 1px solid #00ff88;
    border-radius: 8px;
    padding: 2px 8px;
    font-family: 'Courier New', monospace;
    color: #00ff88;
}

pre {
    background: #0a0a0a;
    border: 1px solid #00ff88;
    border-radius: 10px;
    padding: 20px;
    overflow-x: auto;
    position: relative;
}

pre::before {
    content: "⚡ RUST ⚡";
    position: absolute;
    top: -12px;
    left: 10px;
    background: #0a0a0a;
    padding: 0 10px;
    color: #00ff88;
    font-size: 10px;
}

.terminal {
    background: #0a0a0a;
    border-radius: 10px;
    padding: 20px;
    font-family: 'Courier New', monospace;
    border: 1px solid #00ff88;
}

.terminal .line {
    white-space: nowrap;
    overflow: hidden;
    animation: typing 3s steps(40, end);
    border-right: 2px solid #00ff88;
    animation-fill-mode: forwards;
    width: 0;
}

.terminal .line:nth-child(1) { animation-duration: 2s; animation-delay: 0s; }
.terminal .line:nth-child(2) { animation-duration: 2s; animation-delay: 2s; }
.terminal .line:nth-child(3) { animation-duration: 2s; animation-delay: 4s; }
.terminal .line:nth-child(4) { animation-duration: 2s; animation-delay: 6s; }

.stats {
    display: flex;
    justify-content: space-around;
    margin: 40px 0;
    flex-wrap: wrap;
}

.stat {
    text-align: center;
    animation: pulse 2s infinite;
}

.stat-number {
    font-size: 48px;
    font-weight: bold;
    color: #00ff88;
}

.stat-label {
    color: #ff6600;
    font-size: 14px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}

th, td {
    border: 1px solid #00ff88;
    padding: 12px;
    text-align: left;
}

th {
    background: rgba(0,255,136,0.1);
    color: #00ff88;
}

tr:hover {
    background: rgba(0,255,136,0.05);
}

.button {
    display: inline-block;
    background: linear-gradient(135deg, #00ff88, #00cc66);
    color: #0a0a0a;
    padding: 12px 24px;
    border-radius: 30px;
    text-decoration: none;
    font-weight: bold;
    transition: transform 0.3s;
    margin: 10px;
}

.button:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 20px rgba(0,255,136,0.5);
}

.footer {
    text-align: center;
    margin-top: 50px;
    padding-top: 30px;
    border-top: 1px solid #00ff88;
    color: #666;
    font-size: 12px;
}

.blink {
    animation: blink 1s infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}

.warning {
    background: rgba(255,0,0,0.1);
    border-left: 4px solid #ff4444;
    padding: 15px;
    border-radius: 10px;
    margin: 20px 0;
}
</style>
</head>
<body>
<div class="container">

<h1>🛡️ Virus Scanner Pro</h1>

<div class="badge-container">
    <span class="badge">🐍 Python 3.7+</span>
    <span class="badge">🖥️ Tkinter GUI</span>
    <span class="badge">🔗 VirusTotal API v3</span>
    <span class="badge">🛡️ 70+ Antivirüs</span>
    <span class="badge">📁 Sürükle-Bırak</span>
    <span class="badge">🌐 URL Tarama</span>
</div>

<p align="center">
    <img src="https://img.shields.io/badge/Version-2.0.0-brightgreen" alt="Version">
    <img src="https://img.shields.io/badge/License-MIT-blue" alt="License">
    <img src="https://img.shields.io/badge/Python-3.7+-blue" alt="Python">
    <img src="https://img.shields.io/badge/API-VirusTotal-orange" alt="API">
    <img src="https://img.shields.io/badge/Status-Active-brightgreen" alt="Status">
</p>

<hr>

<h2>🎯 Proje Hakkında</h2>

<p><strong>Virus Scanner Pro</strong>, VirusTotal API'sini kullanan, <strong>70+ antivirüs motoru</strong> ile dosyaları ve URL'leri tarayan, modern <strong>Tkinter arayüzüne</strong> sahip profesyonel bir güvenlik aracıdır. Eğitim amaçlı olarak geliştirilmiştir ve sadece kendi laboratuvar ortamınızda kullanılmalıdır.</p>

<div class="warning">
    ⚠️ <strong>UYARI:</strong> Bu araç SADECE eğitim ve araştırma amaçlıdır. Yetkisiz sistemlerde kullanmak yasa dışıdır!
</div>

<h2>✨ Özellikler</h2>

<div class="feature-grid">
    <div class="feature-card">
        <span class="icon">🦠</span>
        <h3>70+ Antivirüs Motoru</h3>
        <p>VirusTotal API ile tüm büyük antivirüs motorlarından sonuç</p>
    </div>
    
    <div class="feature-card">
        <span class="icon">📁</span>
        <h3>Sürükle-Bırak Desteği</h3>
        <p>Dosyaları pencereye sürükleyerek hızlı tarama</p>
    </div>
    
    <div class="feature-card">
        <span class="icon">📂</span>
        <h3>Toplu Tarama</h3>
        <p>Dizin içindeki tüm dosyaları tarayabilme</p>
    </div>
    
    <div class="feature-card">
        <span class="icon">🌐</span>
        <h3>URL Tarama</h3>
        <p>Şüpheli linkleri kontrol etme</p>
    </div>
    
    <div class="feature-card">
        <span class="icon">📊</span>
        <h3>Detaylı Raporlama</h3>
        <p>JSON ve TXT formatında rapor çıktısı</p>
    </div>
    
    <div class="feature-card">
        <span class="icon">🎨</span>
        <h3>Modern Arayüz</h3>
        <p>Koyu tema, sekme düzeni, animasyonlar</p>
    </div>
</div>

<h2>📸 Ekran Görüntüleri</h2>

<div class="screenshot">
    <div class="screenshot-placeholder">
        <pre style="background: none; border: none;">
╔══════════════════════════════════════════════════════════════╗
║                    VIRUS SCANNER PRO                         ║
╠══════════════════════════════════════════════════════════════╣
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ 📁 DOSYALARI BURAYA SÜRÜKLEYİN                          │ ║
║  │                   veya                                  │ ║
║  │              [📂 Gözat]                                 │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  🔍 TARAMAYI BAŞLAT     🗑️ Temizle                         ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │ 🟢 AVG: Clean                                           │ ║
║  │ 🔴 Kaspersky: Trojan.Win32.Generic                     │ ║
║  │ 🟡 McAfee: Suspicious                                  │ ║
║  └────────────────────────────────────────────────────────┘ ║
╚══════════════════════════════════════════════════════════════╝
        </pre>
    </div>
</div>

<h2>🚀 Kurulum</h2>

<h3>Gereksinimler</h3>
<pre><code>pip install requests tkinterdnd2 pillow</code></pre>

<h3>API Anahtarı Alma</h3>
<div class="terminal">
    <div class="line">$ 1. https://www.virustotal.com adresine git</div>
    <div class="line">$ 2. Ücretsiz hesap oluştur</div>
    <div class="line">$ 3. API anahtarını al</div>
    <div class="line">$ 4. Uygulamaya gir ve anahtarı yapıştır</div>
</div>

<h3>Çalıştırma</h3>
<pre><code>python virus_scanner_gui.py</code></pre>

<h2>📊 Teknik Özellikler</h2>

<table>
    <tr>
        <th>Özellik</th>
        <th>Değer</th>
    </tr>
    <tr>
        <td>Antivirüs Motoru Sayısı</td>
        <td>70+</td>
    </tr>
    <tr>
        <td>Hash Algoritmaları</td>
        <td>MD5, SHA1, SHA256</td>
    </tr>
    <tr>
        <td>API Versiyonu</td>
        <td>VirusTotal API v3</td>
    </tr>
    <tr>
        <td>Ücretsiz API Limiti</td>
        <td>4 istek/dakika</td>
    </tr>
    <tr>
        <td>Dosya Boyut Limiti</td>
        <td>32 MB (ücretsiz API ile yükleme yok)</td>
    </tr>
    <tr>
        <td>Desteklenen Platformlar</td>
        <td>Windows, Linux, macOS</td>
    </tr>
</table>

<h2>🎯 Kullanım</h2>

<div class="stats">
    <div class="stat">
        <div class="stat-number">📁</div>
        <div class="stat-label">Dosya Seç</div>
    </div>
    <div class="stat">
        <div class="stat-number">🔍</div>
        <div class="stat-label">Tara</div>
    </div>
    <div class="stat">
        <div class="stat-number">📊</div>
        <div class="stat-label">Sonuç</div>
    </div>
    <div class="stat">
        <div class="stat-number">💾</div>
        <div class="stat-label">Rapor</div>
    </div>
</div>

<h3>Test için EICAR Dosyası</h3>
<pre><code>echo 'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*' > test_eicar.com</code></pre>

<h2>📁 Proje Yapısı</h2>

<pre><code>virus_scanner_pro/
│
├── virus_scanner_gui.py      # Ana uygulama
├── requirements.txt           # Gereksinimler
├── README.md                  # Bu dosya
└── scan_report.json           # Tarama raporları (otomatik oluşur)</code></pre>

<h2>🔧 Sık Sorulan Sorular</h2>

<p><strong>❓ Ücretsiz API ile dosya yükleyebilir miyim?</strong><br>
Hayır, ücretsiz API sadece hash sorgulama yapabilir. Dosya yüklemek için Premium API gerekir.</p>

<p><strong>❓ Kaç antivirüs motoru kullanılıyor?</strong><br>
VirusTotal 70+ antivirüs motoru kullanır. Tüm sonuçları görebilirsiniz.</p>

<p><strong>❓ Sürükle-bırak neden çalışmıyor?</strong><br>
tkinterdnd2 kütüphanesini yükleyin: <code>pip install tkinterdnd2</code></p>

<p><strong>❓ Linux'ta çalışır mı?</strong><br>
Evet, tamamen cross-platform çalışır.</p>

<h2>🌟 Gelecek Özellikler</h2>

<ul>
    <li>✅ Gerçek zamanlı izleme</li>
    <li>✅ Tarama planlama</li>
    <li>✅ Çoklu API desteği</li>
    <li>✅ Ransomware simülasyonu</li>
    <li>✅ Ağ taraması</li>
    <li>✅ Webhook bildirimleri</li>
</ul>

<h2>🤝 Katkıda Bulunma</h2>

<p>Projeye katkıda bulunmak isterseniz:</p>
<ol>
    <li>Fork yapın</li>
    <li>Yeni branch oluşturun (<code>git checkout -b feature/yenilik</code>)</li>
    <li>Değişikliklerinizi commit edin (<code>git commit -m 'Yeni özellik eklendi'</code>)</li>
    <li>Push yapın (<code>git push origin feature/yenilik</code>)</li>
    <li>Pull Request oluşturun</li>
</ol>

<h2>📞 İletişim</h2>

<p>
    <a href="#" class="button">🐙 GitHub</a>
    <a href="#" class="button">📧 E-posta</a>
    <a href="#" class="button">📱 Telegram</a>
</p>

<h2>📜 Lisans</h2>

<p>Bu proje <strong>MIT Lisansı</strong> ile lisanslanmıştır.</p>

<h2>⚠️ Sorumluluk Reddi</h2>

<div class="warning">
    <strong>⚠️ ÖNEMLİ:</strong> Bu yazılım SADECE eğitim ve araştırma amaçlıdır. Yetkisiz sistemlerde kullanmak YASA DIŞIDIR. Tüm yasal sorumluluk kullanıcıya aittir. Bu aracı kullanarak, yasalara tamamen uyacağınızı kabul etmiş olursunuz.
</div>

<hr>

<div class="footer">
    <span class="blink">⬤</span> Virus Scanner Pro v2.0 | Made with 🐍 Python | 70+ Antivirüs Motoru <span class="blink">⬤</span><br>
    <span style="color: #666;">Sadece eğitim amaçlıdır. Yasal sorumluluk kullanıcıya aittir.</span>
</div>

</div>
</body>
</html>
