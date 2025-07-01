# YTMP3-Server

YouTube videolarından MP3 formatında ses dosyası indirmek için Python tabanlı basit ve hızlı bir sunucu uygulaması.

---

## Özellikler

- YouTube videolarını MP3’e dönüştürür ve indirilebilir hale getirir.
- Basit API ile kolay entegrasyon.
- Railway, Heroku, vs. gibi platformlarda kolay deploy imkanı.
- Nixpacks ile otomatik ortam yapılandırma.

---

## Gereksinimler

- Python 3.8+
- `pip` paket yöneticisi
- `yt-dlp`, `flask`, `pydub` gibi paketler (requirements.txt içinde)

---

## Kurulum

1. Repoyu klonlayın:

   ```bash
   git clone https://github.com/umtark/ytmp3-server.git
   cd ytmp3-server
