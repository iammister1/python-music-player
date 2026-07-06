import pygame
import tkinter
import random
import os
from tkinter import filedialog

pygame.init()

current_song = ""
path = ""

songs_completed = []

shuffle = False
paused = False

def removeUnpathSelected():
    no_path_selected.forget()


def updateText():
    texlen = 20

    print(songs_completed)


    if len(current_song) > 35:
        texlen = 10

    currently_playing.config(
        text=current_song,
        font=("Arial", texlen)
    )

    pygame.mixer.music.load(
        os.path.join(path, current_song)
    )
    pygame.mixer.music.play()


def getnewSong():
    global current_song
    global paused

    songs = sorted(
        [
            file
            for file in os.listdir(path)
            if file.endswith((".mp3", ".wav", ".ogg"))
        ]
    )

    paused = False
    play_button.config(text="Pause")

    if not shuffle:
        if len(songs_completed) >= len(songs):
            songs_completed.clear()

        for song in songs:
            if song not in songs_completed:
                songs_completed.append(song)
                current_song = song
                updateText()
                print(songs_completed)
                return

    else:
        print("shuffle is ON")

        if len(songs) <= 1:
            return

        if len(songs_completed) >= len(songs):
            songs_completed.clear()

        while True:
            random_song = random.choice(songs)

            if random_song != current_song and random_song not in songs_completed:
                current_song = random_song
                songs_completed.append(random_song)
                updateText()
                return


def playSong():
    global paused, no_path_selected
    if path == "":
        print("no path selected")
        no_path_selected.pack()
        app.after(1000, removeUnpathSelected)
        return
    else:
        if current_song == "":
            getnewSong()
            return

        if not paused:
            paused = True
            pygame.mixer.music.pause()
            play_button.config(text="Play")
        else:
            paused = False
            pygame.mixer.music.unpause()
            play_button.config(text="Pause")


def turnonShuffle():
    global shuffle, songs_completed

    songs_completed = []

    if not shuffle:
        shuffle = True
        shuffle_button.config(
            bg="green",
            highlightbackground="green"
        )
    else:
        shuffle = False
        shuffle_button.config(
            bg="white",
            highlightbackground="white"
        )


def checkSongEnd():
    if (
        current_song != ""
        and not paused
        and not pygame.mixer.music.get_busy()
    ):
        getnewSong()

    app.after(1000, checkSongEnd)

def change_path():
    global path
    path = filedialog.askdirectory(title="Select folder")
    print(path)
    


app = tkinter.Tk()
app.title("music player")
app.geometry("600x800")

tt = tkinter.Label(
    app,
    text="music player",
    font=("Helvetica", 18)
)
tt.pack(padx=10, pady=10)

choose_path = tkinter.Button(
    app,
    text="Choose Playlist Path",
    font=("Arial", 16),
    command=change_path
)
choose_path.pack(padx=10, pady=10)

no_path_selected = tkinter.Button(
    app,
    text="No path selected",
    font=("Arial", 18),
    fg="Red"
)

currently_playing = tkinter.Label(
    app,
    text="",
    font=("Arial", 16)
)
currently_playing.pack(
    padx=10,
    pady=100
)

skip_button = tkinter.Button(
    app,
    text="Skip",
    font=("Arial", 16),
    command=getnewSong
)
skip_button.pack()

play_button = tkinter.Button(
    app,
    text="Play",
    font=("Arial", 16),
    command=playSong
)
play_button.pack()

shuffle_button = tkinter.Button(
    app,
    text="Shuffle",
    font=("Arial", 16),
    command=turnonShuffle
)
shuffle_button.pack()

checkSongEnd()

app.mainloop()
