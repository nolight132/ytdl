import argparse, os, subprocess
from sys import platform
from pytube.cli import on_progress
from pytube import YouTube

parser = argparse.ArgumentParser()
parser.add_argument("link")
parser.add_argument("target_resolution")
args = parser.parse_args()

def download_best(target_res, path):
    best_stream = yt.streams[0]
    for stream in yt.streams:
        if stream.resolution != None:
            stream_res = int(stream.resolution[:-1])
            best_res = int(best_stream.resolution[:-1])
            if abs(stream_res - target_res) < abs(best_res - target_res) or (abs(stream_res - target_res) <= abs(best_res - target_res) and stream.mime_type == "video/mp4" and target_res > 720):
                best_stream = stream
    if int(best_stream.resolution[:-1]) > 720:
        audio_path = yt.streams.filter(only_audio=True).get_audio_only().download("source/audio")
        video_path = best_stream.download("source/video")
        cmd = f'ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac "{path}/{best_stream.title}".mp4'
        subprocess.call(cmd, shell=True)
        print('Muxing Done')
        os.remove(video_path)
        os.remove(audio_path)
        print(f"Saved to: {path}")
    else:
        try:
            path = best_stream.download(output_path=path)
            print(f"Saved to: {path}")
        except TimeoutError as err:
            raise err

link = args.link
yt = YouTube(link,on_progress_callback=on_progress)

if platform == "win32":
    path = f"{os.path.expanduser('~')}\Downloads"
elif platform == "darwin" or platform == "linux" or platform == "linux2":
    path = f"{os.path.expanduser('~')}/Downloads"

try:
    int(args.target_resolution)
except:
    raise SyntaxError("Target resolution must be a number.")

target_res = int(args.target_resolution)
print('Downloading:', yt.title)
download_best(target_res, path)
