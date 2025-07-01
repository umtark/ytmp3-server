import base64
import tempfile
import os
from flask import Flask, request, send_file
import yt_dlp

app = Flask(__name__)

COOKIES_BASE64 = """
IyBOZXRzY2FwZSBIVFRQIENvb2tpZSBGaWxlDQojIFRoaXMgZmlsZSB3YXMgZ2VuZXJhdGVkIGF1dG9tYXRpY2FsbHkuDQoNCi55b3V0dWJlLmNvbQlUUlVFCS8JVFJVRQkxNzg1NzU3NjU0CV9fU2VjdXJlLTNQU0lECWcuYTAwMHlnaXFIMjRTLVpkbk1xWVdiV3JJSFRCRmJqRXM5TkpuYk15aDlpb2lnUUJfam9jT3Q3eGJ6LWRlWldjbXp1eEZaZkh1NndBQ2dZS0FUa1NBUkVTRlFIR1gyTWl4MjJrY2gyVXlnNlM3LXltX2tXTkxSb1ZBVUY4eUtyR05Kdm9USE05ajhjaExYeFhLbWtaMDA3Ng0KLnlvdXR1YmUuY29tCVRSVUUJLwlUUlVFCTE3ODI5MjAzMTIJX19TZWN1cmUtMVBTSURUUwlzaWR0cy1DakFCNUgwM1A1NGRsX3FtNzhCc3lrNFh1Tml2QVh1bG5nTlEwa3RYWTEwSXRhamhHcnc1ZURmZ3NUX2xoMEhTTWpjUUFBDQoueW91dHViZS5jb20JVFJVRQkvCVRSVUUJMTc4NTc1NzY1NAlTQVBJU0lECWxHOUpQMzMzNlJpNkE5VzcvQXNqd2FhQVk1U0NzSWFjbUsNCi55b3V0dWJlLmNvbQlUUlVFCS8JVFJVRQkxNzgyOTIwMzE3CV9fU2VjdXJlLTFQU0lEQ0MJQUtFeVh6VTNTbjJJaHVvZjFvQTctdWNfbl9wV1poWG01Y3poQ3MwZGt3NXd1U2k1UDFpVlBtVm5pdUtmekJSY3I5bEJ1dm8NCi55b3V0dWJlLmNvbQlUUlVFCS8JVFJVRQkxNzg1NzU3NjU0CVNTSUQJQS1oVElFMkUwTkRBRkI4VUQNCi55b3V0dWJlLmNvbQlUUlVFCS8JVFJVRQkxNzg1NzU3NjU0CV9fU2VjdXJlLTFQQVBJU0lECWxHOUpQMzMzNlJpNkE5VzcvQXNqd2FhQVk1U0NzSWFjbUsNCi55b3V0dWJlLmNvbQlUUlVFCS8JVFJVRQkxNzg1NzU3NjU0CV9fU2VjdXJlLTFQU0lECWcuYTAwMHlnaXFIMjRTLVpkbk1xWVdiV3JJSFRCRmJqRXM5TkpuYk15aDlpb2lnUUJfam9jT0JtZ05pRndhbXBYMDh1R0lRaVhkOFFBQ2dZS0FVWVNBUkVTRlFIR1gyTWlYeENvMVZSTmU1cVBHc1lSZHc4aU5ob1ZBVUY4eUtxajZiWXlRRmxRS0FLTG5Bd1VLdDVuMDA3Ng0KLnlvdXR1YmUuY29tCVRSVUUJLwlUUlVFCTE3ODU3NTc2NTQJX19TZWN1cmUtM1BBUElTSUQJbEc5SlAzMzM2Umk2QTlXNy9Bc2p3YWFBWTVTQ3NJYWNtSw0KLnlvdXR1YmUuY29tCVRSVUUJLwlUUlVFCTE3ODI5MjAzMTcJX19TZWN1cmUtM1BTSURDQwlBS0V5WHpXc2toaHFpc2pmQnliZDRDV01RdEJJQUlPQnpSWU1GT3NtYWE1ZXJDN3c2U3owTzFNc3N6Z3B5azZxa052MVVMZnkNCi55b3V0dWJlLmNvbQlUUlVFCS8JVFJVRQkxNzgyOTIwMzEyCV9fU2VjdXJlLTNQU0lEVFMJc2lkdHMtQ2pBQjVIMDNQNTRkbF9xbTc4QnN5azRYdU5pdkFYdWxuZ05RMGt0WFkxMEl0YWpoR3J3NWVEZmdzVF9saDBIU01qY1FBQQ0KLnlvdXR1YmUuY29tCVRSVUUJLwlUUlVFCTE3ODU3NTc0MjkJTE9HSU5fSU5GTwlBRm1tRjJzd1JnSWhBS2RxRk5uSTB4MUp6bjhVRnFrUThPb0lrQlJMcnN2cndoWWE1M1RNYlRLV0FpRUFocHRIUl9RRWdYd0ZDMXp1aWhpbV9fMWV4dk4tQlRfVkNwVHlTR05KSUR3OlFVUTNNak5tZUdoRlNGcHlPR1IxWkhGYVdtTktSVkpTVm5CTlh6QkhkbTExVldORFEyTlVVemwwYmpKUlpuUkJkMFpPT0doTE1VTkJXVUZZYkZaNU5XSk9lbVpqYm5GbGNqUkxjbmN4VUhGVWNtcEdhakZhTm1GalNpMUpNVVpET0cxaE9XUnJXRXRUV2t4NWJWQmZRVm93VUhWNVUzTkdka1Z2UnpCSFpWRjRZbDlWUjNscVVsRTRSRTUxUm1ZMVUwbE1MVmRKTnpGeVZIVjViWEZPVWpaUg0KLnlvdXR1YmUuY29tCVRSVUUJLwlUUlVFCTE3ODU5NDQzMDkJUFJFRglmNj00MDAwMDA4MCZmNz00MTUwJnR6PUFzaWEuQmFnaGRhZCZmNT0zMDAwMA0K
""".strip()

@app.route('/mp3')
def mp3():
    url = request.args.get('url')
    if not url:
        print("[HATA] URL parametresi eksik.")
        return "URL parametresi eksik", 400

    try:
        with tempfile.TemporaryDirectory() as tmp:
            cookie_path = None

            if COOKIES_BASE64:
                print("[BİLGİ] Gömülü cookie bulundu, çözümleniyor...")
                try:
                    decoded = base64.b64decode(COOKIES_BASE64)
                except Exception as e:
                    print(f"[HATA] Cookie base64 decode hatası: {e}")
                    return "Cookie decode edilirken hata oluştu", 500

                cookie_path = os.path.join(tmp, 'cookies.txt')
                with open(cookie_path, 'wb') as f:
                    f.write(decoded)
                print(f"[BİLGİ] Cookie dosyası oluşturuldu: {cookie_path}")
            else:
                print("[UYARI] Gömülü cookie boş veya eksik.")

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(tmp, '%(title)s.%(ext)s'),
                'ffmpeg_location': '/app/ffmpeg',  
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

    except yt_dlp.utils.DownloadError as dl_err:
        print(f"[HATA] İndirme hatası: {dl_err}")
        return f"İndirme hatası: {dl_err}", 500
    except Exception as e:
        print(f"[HATA] Genel hata: {str(e)}")
        return f"Genel hata: {str(e)}", 500

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', '5000'))
    except ValueError:
        print("[UYARI] PORT ortam değişkeni geçersiz, 5000 olarak ayarlanacak.")
        port = 5000
    print(f"[BİLGİ] Uygulama başlatılıyor, port: {port}")
    app.run(host='0.0.0.0', port=port)
