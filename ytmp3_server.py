import base64
import tempfile
import os
from flask import Flask, request, send_file
import yt_dlp

app = Flask(__name__)

@app.route('/mp3')
def mp3():
    url = request.args.get('url')
    if not url:
        print("[HATA] URL parametresi eksik.")
        return "URL parametresi eksik", 400

    try:
        with tempfile.TemporaryDirectory() as tmp:
            cookie_path = None
            cookies_b64 = os.environ.get('COOKIES_JSON')

            if cookies_b64:
                print("[BİLGİ] Cookie ortam değişkeni bulundu, çözümleniyor...")
                cookie_path = os.path.join(tmp, 'cookies.txt')
                with open(cookie_path, 'wb') as f:
                    f.write(base64.b64decode(cookies_b64))
                print(f"[BİLGİ] Cookie dosyası oluşturuldu: {cookie_path}")
            else:
                print("[UYARI] Cookie ortam değişkeni bulunamadı veya boş.")

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(tmp, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
                'no_warnings': True,
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'nooverwrites': True,
                'noplaylist': True,
            }

            if cookie_path:
                ydl_opts['cookiefile'] = cookie_path
                print("[BİLGİ] yt-dlp cookie dosyası kullanacak.")

            print(f"[BİLGİ] İndirme işlemi başlıyor: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if info is None:
                    print("[HATA] Video indirilemedi veya desteklenmeyen URL.")
                    return "Video indirilemedi veya desteklenmeyen URL", 400

                filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'
                print(f"[BİLGİ] İndirilen dosya: {filename}")

            if not os.path.exists(filename):
                print("[HATA] Dosya oluşturulamadı.")
                return "Dosya oluşturulamadı", 500

            print("[BİLGİ] Dosya başarıyla hazır, gönderiliyor...")
            return send_file(filename, as_attachment=True)

    except Exception as e:
        print(f"[HATA] İndirme sırasında hata oluştu: {str(e)}")
        return f"İndirme sırasında hata oluştu: {str(e)}", 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"[BİLGİ] Uygulama başlatılıyor, port: {port}")
    app.run(host='0.0.0.0', port=port)
