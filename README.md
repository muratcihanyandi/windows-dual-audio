# Windows Dual Audio (Dual Audio Bridge) 🎧🎧

Windows 11 (ve 10) üzerinde **iki farklı kulaklığa** (veya hoparlöre) aynı anda, sıfır gecikmeyle ses çıkışı vermenizi sağlayan hafif ve açık kaynaklı ses köprüsü.

Arkadaşınızla aynı bilgisayardan kulaklıklarla ders videosu, film veya YouTube izlemek istediğinizde mükemmel çözümdür.

---

## 🚀 Özellikler

- **Sıfır Gecikme:** Windows'un en alt ses katmanı olan **WASAPI Loopback** mimarisini kullanır.
- **Akıllı Frekans Senkronizasyonu (Ultra-Fast Resampling):** Farklı frekanstaki aygıtları (örneğin 44.100 Hz Bluetooth kulaklık ile 48.000 Hz Realtek ses kartı) 0.06 milisaniyede dinamik olarak senkronize eder. Ses bozulmaz, çatlamaz.
- **Otomatik Aygıt Tespiti:** Sistemdeki birincil çıkış aygıtını ve diğer tüm çıkışları (Bluetooth, 3.5mm jak, USB kulaklık) otomatik listeler.
- **Sanal Kablo / Ağır Program Gerektirmez:** Ekstra hantal sanal kablo sürücülerine ihtiyaç duymaz.

---

## 🛠️ Kurulum

Python 3.8+ yüklü olduğundan emin olun.

Gerekli kütüphaneleri yükleyin:
```bash
pip install pyaudiowpatch numpy
```

---

## 💻 Kullanım

1. 1. kulaklığınız bilgisayara bağlı ve varsayılan ses aygıtı olsun.
2. 2. kulaklığınızı bağlayın (3.5mm jak, USB veya Bluetooth).
3. Scripti çalıştırın:
```bash
python dual_audio_bridge.py
```
Eğer sistemde tek bir 2. aygıt varsa otomatik olarak sesi kopyalamaya başlar. Birden fazla aygıt varsa seçim yapmanız için numaralandırır.

İşiniz bittiğinde terminal penceresinde `Ctrl + C` tuşlarına basarak durdurabilirsiniz.

---

## 📄 Lisans
MIT License
