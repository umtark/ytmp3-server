from flask import Flask, request, send_file, abort
import yt_dlp
import tempfile
import os

app = Flask(__name__)

@app.route('/mp3')
def mp3():
    url = request.args.get('url')
    if not url:
        return "URL parametresi eksik", 400

    try:
        with tempfile.TemporaryDirectory() as tmp:
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
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'
            
            if not os.path.exists(filename):
                return "MP3 dosyası oluşturulamadı", 500
            
            return send_file(filename, as_attachment=True)
    
    except yt_dlp.utils.DownloadError:
        return "Video indirilemedi veya desteklenmeyen URL", 400
    except Exception as e:
        # Loglama için sunucu loguna yazdırabiliriz, burada sadece mesaj dönüyoruz
        return f"Sunucu hatası: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
