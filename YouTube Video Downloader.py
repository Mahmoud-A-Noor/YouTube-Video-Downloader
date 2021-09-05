import pafy
import os
from moviepy.editor import *
import requests
from bs4 import BeautifulSoup
import re


#link = "https://www.youtube.com/watch?v=11CG88oR0Fg"

#playlist = "https://www.youtube.com/playlist?list=PLvyTazcWChK8S7iF7XUG1XwnFfakh0PBf"
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

def get_playlist_videoes(purl):
    html_page = requests.get(purl)
    soup = BeautifulSoup(html_page.content,'html.parser')
    web = str(soup.prettify())
    links = re.findall(r"/watch..=...........\\.........\=..................................",web)
    links = list(set(links))
    return links

def download_playlist():
    l = input("enter YouTube playlist URL you want to download : ")
    links = get_playlist_videoes(l)
    isaudio = input("do you want to download this playlist as audio : ")
    quality = -1
    for link in links:
        video = pafy.new(link)
        video_streams = video.videostreams
        audio_streams = video.audiostreams
        video_name = video.title

        if(isaudio =='y' or isaudio=='Y'):
            if(quality == -1):
                for c,i in enumerate(audio_streams):
                    print(f"{c+1}- {str(i).split('@')[-1]}   {str(i).split('@')[0].split(':')[-1]}")
                quality = int(input("enter number of quality you want to download : "))
        else:
            if(quality == -1):
                for c,i in enumerate(video_streams):
                    print(f"{c+1}- {str(i).split('x')[-1]}   {str(i).split('@')[0].split(':')[-1]}")
                quality = int(input("enter number of quality you want to download : "))
        
        if(isaudio =='y' or isaudio=='Y'):
            if(audio_streams.length<quality):
                video.getbestaudio().download(download_path)
            else:
                audio_streams[quality - 1].download(download_path)
        else:
            video.getbestaudio().download(download_path)
            files = getfilewithextension(video_name)
            if(video_streams.length<quality):
                video.getbestvideo().download(download_path)
            else:
                video_streams[quality - 1].download(download_path)
            files += getfilewithextension(video_name,files)
            combine_audio_video(files,video_name)
        

choice = input("do you want to download a playlist")
if(choice == 'y' or choice == 'Y'):
    download_playlist()
else:
    download_single_video()
