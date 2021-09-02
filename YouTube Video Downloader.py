import pafy
import os
from moviepy.editor import *


download_path = os.path.dirname(os.path.realpath(__file__))

def getfilewithextension(title,files=[]):
    list = []
    for file in os.listdir(f'{download_path}\\'):
        if(file.startswith(title+".")):
            if(file not in files):
                list.append(file)
    return list

def combine_audio_video(files,title):
    videoclip = VideoFileClip(f'{download_path}\\{files[1]}')
    audioclip = AudioFileClip(f'{download_path}\\{files[0]}')
    video = videoclip.set_audio(audioclip)
    if not os.path.exists(f'{download_path}\\output'):
        os.makedirs(f'{download_path}\\output')
    video.write_videofile(f'{download_path}\\output\\{files[1]}')
    os.remove(f'{download_path}\\{files[0]}')
    os.remove(f'{download_path}\\{files[1]}')

def download_single_video():
    link = input("enter video YouTube URL you want to download : ")
    video = pafy.new(link)
    isaudio = input("do you want to download this video as audio : ")
    video_streams = video.videostreams
    audio_streams = video.audiostreams
    video_name = video.title

    if(isaudio =='y' or isaudio=='Y'):
        for c,i in enumerate(audio_streams):
            print(f"{c+1}- {str(i).split('@')[-1]}   {str(i).split('@')[0].split(':')[-1]}")
        choice = int(input("enter number of quality you want to download : "))
    else:
        for c,i in enumerate(video_streams):
            print(f"{c+1}- {str(i).split('x')[-1]}   {str(i).split('@')[0].split(':')[-1]}")
        choice = int(input("enter number of quality you want to download : "))
    
    if(isaudio =='y' or isaudio=='Y'):
        audio_streams[choice - 1].download(download_path)
    else:
        video.getbestaudio().download(download_path)
        files = getfilewithextension(video_name)
        video_streams[choice - 1].download(download_path)
        files += getfilewithextension(video_name,files)
        print(files)
        combine_audio_video(files,video_name)


download_single_video()
