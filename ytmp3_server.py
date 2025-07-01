from flask import Flask, request, send_file
import yt_dlp
import tempfile
import os

app = Flask(__name__)

@app.route('/mp3')
def mp3():
    url = request.args.get('url')
    if not url:
        return "URL parametresi eksik", 400

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
        return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
