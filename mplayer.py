import os
import pygame

# pygame.mixer.init()
#pygame.mixer.music.load("/home/pi/Music/alert.mp3")
#pygame.mixer.music.play()
#while pygame.mixer.music.get_busy() == True:
#	pass

# action=" mplayer /home/pi/Music/alert.mp3"
os.system('mpg321 /home/pi/Music/alert.mp3 &')

#from light_driver import LightDriver
#import os
#from mplayer import Player, CmdPrefix
#player.loadfile('mplayer /home/pi/Music/alert.mp3')

# def main():
#    driver = LightDriver()
#    driver.on()
#    os.system("mplayer /home/pi/Music/alert.mp3")
#if __name__ == "__main__":
#	main()