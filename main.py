import pygame
import tkinter as tk
from tkinter import filedialog
import random
import os

pygame.init()
pygame.mixer.init()

current_song = ""
path = ""
songs = []
songs_completed = []
shuffle = False
paused = False

def loadSongs():
    global songs
    songs = []
    if os.path.isdir(path):
        songs = sorted([f for f in os.listdir(path) if f.lower().endswith((".mp3",".wav",".ogg"))])

def removeUnpathSelected():
    no_path_selected.pack_forget()

def updateText():
    currently_playing.config(text=current_song,font=("Arial",16),wraplength=500,justify="center")
    pygame.mixer.music.load(os.path.join(path,current_song))
    pygame.mixer.music.play()

def getnewSong():
    global current_song, paused, songs_completed
    if not songs:
        currently_playing.config(text="No music found")
        return
    paused=False
    play_button.config(text="Pause")
    if not shuffle:
        if len(songs_completed)>=len(songs):
            songs_completed.clear()
        for s in songs:
            if s not in songs_completed:
                songs_completed.append(s)
                current_song=s
                updateText()
                return
    else:
        if len(songs_completed)>=len(songs):
            songs_completed.clear()
        available=[s for s in songs if s!=current_song and s not in songs_completed]
        if not available:
            return
        current_song=random.choice(available)
        songs_completed.append(current_song)
        updateText()

def playSong():
    global paused
    if not path or not os.path.isdir(path):
        no_path_selected.pack()
        app.after(1000,removeUnpathSelected)
        return
    if current_song=="":
        getnewSong()
        return
    if paused:
        paused=False
        pygame.mixer.music.unpause()
        play_button.config(text="Pause")
    else:
        paused=True
        pygame.mixer.music.pause()
        play_button.config(text="Play")

def turnonShuffle():
    global shuffle,songs_completed
    songs_completed.clear()
    shuffle=not shuffle
    c="green" if shuffle else "white"
    shuffle_button.config(bg=c,highlightbackground=c)

def checkSongEnd():
    if current_song and not paused and not pygame.mixer.music.get_busy():
        getnewSong()
    app.after(200,checkSongEnd)

def change_path():
    global path,current_song,songs_completed
    new=filedialog.askdirectory(title="Select folder")
    if new:
        path=new
        current_song=""
        songs_completed.clear()
        loadSongs()
        with open("data.txt","w") as f:
            f.write(path)

def checkVolume(event=None):
    pygame.mixer.music.set_volume(volume_slider.get()/100)

app=tk.Tk()
app.title("Music Player")
app.geometry("600x800")

if os.path.exists("data.txt"):
    with open("data.txt") as f:
        path=f.read().strip()
    loadSongs()

tk.Label(app,text="Music Player",font=("Helvetica",18)).pack(pady=10)
tk.Button(app,text="Choose Playlist Path",font=("Arial",16),command=change_path).pack(pady=10)

no_path_selected=tk.Label(app,text="No valid playlist selected",fg="red",font=("Arial",14))

currently_playing=tk.Label(app,text="",font=("Arial",16),wraplength=500)
currently_playing.pack(pady=80)

tk.Label(app,text="Volume").pack()
volume_slider=tk.Scale(app,from_=0,to=100,orient="horizontal",command=checkVolume)
volume_slider.set(100)
volume_slider.pack()
pygame.mixer.music.set_volume(1.0)

tk.Button(app,text="Skip",font=("Arial",16),command=getnewSong).pack(pady=5)
play_button=tk.Button(app,text="Play",font=("Arial",16),command=playSong)
play_button.pack(pady=5)
shuffle_button=tk.Button(app,text="Shuffle",font=("Arial",16),command=turnonShuffle)
shuffle_button.pack(pady=5)

checkSongEnd()
app.mainloop()
