import pafy
import os
from moviepy.editor import *
import requests
from bs4 import BeautifulSoup
import re
import time


download_path = os.path.dirname(os.path.realpath(__file__))

def getfilewithextension(title,files=[]):
    list = []
    for file in os.listdir(f'{download_path}\\'):
        if(file.startswith(title+".")):
            if file not in files:
                list.append(file)
                break
    return list

def combine_audio_video(files):
    with open(f'{download_path}\\{files[1]}') as videofile:
        with open(f'{download_path}\\{files[0]}') as audiofile:
            videoclip = VideoFileClip(videofile)
            audioclip = AudioFileClip(audiofile)
            video = videoclip.set_audio(audioclip)
            if not os.path.exists(f'{download_path}\\output'):
                os.makedirs(f'{download_path}\\output')
            video.write_videofile(f'{download_path}\\output\\{files[1]}')
    os.remove(f'{download_path}\\{files[0]}')
    os.remove(f'{download_path}\\{files[1]}')

def download_single_video():
    link = input("Enter YouTube video URL you want to download : ")
    video = pafy.new(link)
    print(">>>>>>>>>>> Format <<<<<<<<<<<\n")
    print("1- Download as Audio")
    print("2- Download as Video")
    isaudio = input(">> ")
    os.system('cls')
    video_streams = [i for i in video.videostreams if str(i).split('@')[0].split(':')[-1] != "webm"]
    audio_streams = video.audiostreams
    video_name = video.title
    
    print(">>>>>>>>>>> Choose Quality <<<<<<<<<<<\n")
    if(isaudio == 1):
        for c,i in enumerate(audio_streams):
            print(f"{c+1}- {str(i).split('@')[-1]}   {str(i).split('@')[0].split(':')[-1]}")
        choice = int(input("enter number of quality you want to download : "))
        os.system('cls')
    else:
        for c,i in enumerate(video_streams):
            print(f"{c+1}- {str(i).split('x')[-1]}   {str(i).split('@')[0].split(':')[-1]}")
        choice = int(input("enter number of quality you want to download : "))
        os.system('cls')
    
    if(isaudio == 1):
        audio_streams[choice - 1].download(download_path)
    else:
        video.getbestaudio().download(download_path)
        files = getfilewithextension(video_name)
        video_streams[choice - 1].download(download_path)
        files += getfilewithextension(video_name,files)
        combine_audio_video(files)
        
    print("the video has been successfully downloaded")
    time.sleep(2)
    os.system('cls')

def get_playlist_videoes(purl):
    html_page = requests.get(purl)
    soup = BeautifulSoup(html_page.content,'html.parser')
    web = str(soup.prettify())
    links = re.findall(r"/watch..=...........\\.........\=..................................",web)
    links = list(set(links))
    for i,li in enumerate(links):
        links[i]="https://www.youtube.com"+str(li).split('\\')[0]
    return links

def download_playlist():
    l = input("enter YouTube playlist URL you want to download : ")
    os.system('cls')
    links = get_playlist_videoes(l)
    print(">>>>>>>>>>> Choose Format <<<<<<<<<<<\n")
    print("1- Download as Audio")
    print("2- Download as Video")
    isaudio = input(">> ")
    os.system('cls')
    quality = -1
    for link in links:
        video = pafy.new(link)
        video_streams = [i for i in video.videostreams if str(i).split('@')[0].split(':')[-1] != "webm"]
        audio_streams = video.audiostreams
        video_name = video.title

        if(isaudio == 1):
            if(quality == -1):
                print(">>>>>>>>>>> Choose Quality <<<<<<<<<<<\n")
                for c,i in enumerate(audio_streams):
                    print(f"{c+1}- {str(i).split('@')[-1]}   {str(i).split('@')[0].split(':')[-1]}")
                quality = int(input("enter number of quality you want to download : "))
                quality = audio_streams[quality-1]
                os.system('cls')
        else:
            if(quality == -1):
                print(">>>>>>>>>>> Choose Quality <<<<<<<<<<<\n")
                for c,i in enumerate(video_streams):
                    print(f"{c+1}- {str(i).split('x')[-1]}   {str(i).split('@')[0].split(':')[-1]}")
                quality = int(input("enter number of quality you want to download : "))
                quality = str(video_streams[quality-1]).split('x')[-1]
                os.system('cls')
        
        if(isaudio == 1):
            found = False
            for i in audio_streams:
                if i==quality:
                    i.download(download_path)
                    found = True
                    break
            if not found:
                print(f"Error the chosen quality for this video : {video_name} couldn't be found try to download it by choosing another quality using the Download YouTube Video option")
        else:
            found = False
            for i in video_streams:
                if str(i).split('x')[-1]==quality:
                    video.getbestaudio().download(download_path)
                    files = getfilewithextension(video_name)
                    i.download(download_path)
                    files += getfilewithextension(video_name,files)
                    combine_audio_video(files)
                    found = True
                    break
            if not found:
                print(f"Error the chosen quality for this video : {video_name} couldn't be found try to download it by choosing another quality using the Download YouTube Video option")
    print("the playlist has been successfully downloaded")
        
while True:
    print(">>>>>>>>>>> YouTube Video Downloader <<<<<<<<<<<\n")
    print("1- Download YouTube Playlist")
    print("2- Download YouTube Video")
    choice = int(input(">> "))
    os.system('cls')
    if choice == 1:
        download_playlist()
    elif choice == 2:
        download_single_video()
