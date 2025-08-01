import argparse
from pathlib import Path
import ffmpeg
from yt_dlp import YoutubeDL

def download_youtube(url, output_dir):
    path_out_dir = Path(output_dir)
    path_webm = path_out_dir / "out.webm"
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': str(path_webm)
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        
    path_out_dir = Path(output_dir)
    path_mp4 = path_out_dir / "out.mp4"
    path_mp3 = path_out_dir / "out.mp3"

    ffmpeg.input(str(path_webm)).output(str(path_mp4), vcodec="libx264").run()
    ffmpeg.input(str(path_mp4)).output(str(path_mp3)).run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='YouTubeの動画をダウンロードし、音声を分離します。')
    parser.add_argument('--url', '-i', type=str, help='YouTubeの動画URL')
    parser.add_argument('--output-dir', '-o', type=str, default='./movie', help='出力先ディレクトリ')

    args = parser.parse_args()

    download_youtube(args.url, args.output_dir)