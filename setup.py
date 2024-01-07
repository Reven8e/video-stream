import os
import subprocess
import sys
import os

print("Installing Python Dependencies...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

movie_path = input("Enter the path to your movie: ")

print("Converting video to HLS format...")
movie_name = os.path.basename(movie_path).replace(".mp4", "")

movie_dir = os.path.join("src/static/movies", movie_name)
os.makedirs(movie_dir, exist_ok=True)

low_dir = os.path.join(movie_dir, "low")
high_dir = os.path.join(movie_dir, "high")

os.makedirs(low_dir, exist_ok=True)
os.makedirs(high_dir, exist_ok=True)

print("Converting video to HLS format (1080p)...")
subprocess.call([
    'ffmpeg', '-i', movie_path,
    '-c:v', 'libx264', '-profile:v', 'high', '-level', '4.0', '-b:v', '5000k',
    '-c:a', 'aac', '-b:a', '192k',
    '-s', '1920x1080',
    '-start_number', '0',
    '-hls_time', '10',
    '-hls_list_size', '0',
    '-f', 'hls', f'src/static/movies/{movie_name}/high/output.m3u8'
])

print("Converting video to HLS format (144p)...")
subprocess.call([
    'ffmpeg', '-i', movie_path,
    '-c:v', 'libx264', '-profile:v', 'baseline', '-level', '3.0', '-b:v', '95k',
    '-c:a', 'aac', '-b:a', '64k',
    '-s', '256x144',
    '-start_number', '0',
    '-hls_time', '10',
    '-hls_list_size', '0',
    '-f', 'hls', f'src/static/movies/{movie_name}/low/output.m3u8'
])

print("Creating HLS master.m3u8 file...")
with open(f"src/static/movies/{movie_name}/master.m3u8", 'a+') as f:
    text = """#EXTM3U
#EXT-X-STREAM-INF:BANDWIDTH=4000000,AVERAGE-BANDWIDTH=4000000,RESOLUTION=1920x1080,CODECS="avc1.640028,mp4a.40.2"
high/output.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=500000,AVERAGE-BANDWIDTH=500000,RESOLUTION=256x144,CODECS="avc1.42001E,mp4a.40.2"
low/output.m3u8"""
    f.write(text)

print("Installation completed successfully!")
print(f"Movie files can be found in src/static/movies/{movie_name}")
print(f"SQL Query: INSERT INTO movies (movie_title, movie_path, movie_thumbnail) VALUES ('<movie_title>', 'static/movies/{movie_name}/master.m3u8', '<movie_thumbnail_url>');")