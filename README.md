# Windows Dual Audio Bridge

Windows 11 / 10 üzerinde **aynı sesi iki farklı çıkış aygıtına** (iki kulaklık,
kulaklık + hoparlör) aynı anda veren tek dosyalık ses köprüsü.

Tek bilgisayardan iki kişi film/ders/YouTube izleyecekken gerekli. Sanal kablo
sürücüsü, ek kurulum, arayüz yok — `python dual_audio_bridge.py`.

```bash
pip install pyaudiowpatch numpy
python dual_audio_bridge.py
```

---

## Nasıl çalışıyor

WASAPI Loopback ile **varsayılan çıkış aygıtının kendi sesini** yakalar ve ikinci
aygıta yeniden gönderir. Sistem sesini "kopyalamak" için ses sürücüsüne dokunmaz.

```
Varsayılan çıkış (kulaklık A)
        │  WASAPI Loopback capture  (non-blocking, <5 µs callback)
        ▼
   jitter buffer (thread-safe queue, 3 paket ön dolum)
        │  gerçek zamanlı numpy resampling (48 kHz ↔ 44.1 kHz)
        ▼
İkinci çıkış (kulaklık B / hoparlör)
```

### Çözülen üç somut problem

| Problem | Çözüm |
|---|---|
| Capture callback'i bloklarsa **ana cihazda ses cızırdar** | Yakalama callback'i sadece kuyruğa yazar; çalma ayrı bir thread'de yürür. Ana cihazın sesi hiçbir koşulda kesilmez. |
| Bluetooth kulaklıkta **paket düzensizliği** (jitter) | 3 paketlik ön dolum + thread-safe queue. Bluetooth'un düzensiz zamanlaması tamponla yutulur. |
| İki aygıt farklı örnekleme hızında (48 kHz vs 44.1 kHz) → **perde kayması** | Her paket için anlık numpy resampling; cihazlar arası hız farkı dinamik kapatılır. |

Ek olarak: hedef aygıt seçilmezse isim üzerinden akıllı seçim yapar
(`headphone`, `buds`, `airpod`, `wireless` gibi anahtar kelimeler öncelikli),
böylece hoparlör yerine kulaklığa yönlenir.

---

## Kullanım

1. Birinci kulaklık bağlı ve **varsayılan çıkış** olsun.
2. İkinci aygıtı bağla (3.5 mm, USB veya Bluetooth).
3. Çalıştır:

```bash
python dual_audio_bridge.py
```

Tek aday aygıt varsa doğrudan başlar; birden fazlaysa numaralı liste verir.
Belirli bir aygıtı zorlamak için:

```bash
python dual_audio_bridge.py --target 14
```

Durdurmak için `Ctrl + C`.

---

## Gereksinimler

- Windows 10 / 11
- Python 3.8+
- `pyaudiowpatch`, `numpy`

---

## Lisans

MIT
