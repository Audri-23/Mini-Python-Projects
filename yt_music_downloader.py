import static_ffmpeg
import yt_dlp

# Ensure ffmpeg and ffprobe are available in PATH
static_ffmpeg.add_paths()

url = input("Enter video URL: ").strip()
if not url:
    print("Error: No URL provided.")
    exit(1)

filename = input("Enter music filename: ").strip()
if not filename:
    filename = "song"

ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'noprogress': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '0',
    }],
    'outtmpl': f'{filename}.%(ext)s',
}

print("Downloading...")
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print(f"Download completed: {filename}.mp3")
