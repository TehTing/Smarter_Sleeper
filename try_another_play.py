# another player
# implement alert

import vlc
from gpiozero import Button
from time import sleep

vlc_instance = vlc.Instance("--input-repeat=999")
player = vlc_instance.media_player_new()
song = vlc_instance.media_new("/home/pi/Music/alert.mp3")

player.set_media(song)
player.audio_set_volume(100)
player.play()
 
Button.was_held = False

def held(btn):
    print("Button held ")
    #btn.was_held = True
    player.stop()
    return 0

def released(btn):
    print("Button released ")
    #if not btn.was_held:
    #    pressed()
    #btn.was_held = False

def pressed():
    print("Button pressed ")
    #player.pause()

btn = Button(17, hold_time=2)

btn.when_held = held
btn.when_released = released

while True: pass