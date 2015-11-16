'''
Project Kasebsu (Music Player)
@ver: v0.02
@Authors: Nikhil Kartha, Rohit J. Sebastian, Nandu Sunil
'''
from pygame import *
from pygbutton import PygButton as b
import os,random
from glob import glob

dim = (320,300)
framerate = 1000
cwd = os.path.abspath(os.path.dirname(__file__)) #file's current working directory
bg = image.load(cwd + "\\bg.jpg") # CHANGE THIS WHEN ELSEWHERE
bgRect = bg.get_rect()
prevButton = b((12, 30, 60, 30), '<')
playButton = b((12+2*60, 30, 60, 30), 'PLAY')
pauseButton = b((12+60, 30, 60, 30), 'PAUSE')
stopButton = b((12+3*60, 30, 60, 30), 'STOP')
nextButton = b((12+4*60, 30, 60, 30), '>')
volDownButton = b((50,70,30,30), '-')
volUpButton = b((80,70,30,30), '+')
shuffleButton = b((70,200,80,30), 'SHUFFLE')
repeatButton = b((170,200,80,30), 'REPEAT')
A = b((212,70,30,30), 'A')
B = b((242,70,30,30), 'B')
searchButton = b((120,250,80,30), 'SEARCH')
playlist = []

def play(songpath):
    print "Loading", os.path.basename(songpath).split('.')[0],"..."
    mixer.music.load(songpath)
    print "Playing..."
    mixer.music.play()
    '''while mixer.music.get_busy(): #Loop when you don't have display
         time.Clock().tick(1000) #Forcing framrate so that mixer plays music
         if mixer.music.get_pos()%10000==0 :
            print mixer.music.get_pos()/1000,"seconds played"'''
    if not mixer.music.get_busy(): print "Music Over!"

def showList(playlist):
        print "\nThere are", len(playlist),"songs in this playlist:"
        for song in playlist:
            print os.path.basename(song)
        print

class Player():
    def __init__(self):
        print "Initializing..."
        init()
        mixer.init()
        mixer.music.set_volume(1.0)
        print "============================\n Kasebsu Music Player v0.01\n============================"

    def loop(self, screen):
        A.bgcolor = (100,200,100)
        playlist = glob("A\\*.ogg") + glob("A\\*.mp3") + glob("A\\*.mid")
        showList(playlist)
        paused = True
        repeat = False
        i = 0
        while True:
            delta_t = time.Clock().tick(framerate)
            # handle input events
            for ev in event.get():
                    if ev.type == QUIT:
                        return # closing the window, end of the game loop
                    elif 'click' in playButton.handleEvent(ev):
                        if mixer.music.get_busy() and paused:
                            mixer.music.unpause()
                            print "Resuming..."
                            paused = False
                        elif 0 <= i < len(playlist):
                            play(playlist[i])
                            paused = False
                        else:
                            print "O_O Unexpected error!"
                    elif 'click' in pauseButton.handleEvent(ev):
                        if paused and mixer.music.get_busy():
                            print ">_< Already Paused! Press Play to Resume."
                        elif mixer.music.get_busy():
                            paused = True
                            mixer.music.pause()
                            print "Paused"
                        else:
                            print "No music playing to pause"
                    elif 'click' in stopButton.handleEvent(ev):
                        if mixer.music.get_busy():
                            mixer.music.stop()
                            print "Song stopped"
                        else:
                            print ">_< There's no music playing to stop!"
                    elif 'click' in nextButton.handleEvent(ev) or (ev.type == KEYDOWN and ev.key == K_RIGHT):
                        if i>=len(playlist)-1:
                            print "Can't go any further"
                        else:
                            print "Going to next song..."
                            i = i + 1
                            paused = False
                            play(playlist[i])
                    elif 'click' in prevButton.handleEvent(ev) or (ev.type == KEYDOWN and ev.key == K_LEFT):
                        if i<=0:
                            print "(!) Can't go any more back"
                        else:
                            print "Going to previous song..."
                            i = i - 1
                            paused = False
                            play(playlist[i])
                    elif 'click' in volUpButton.handleEvent(ev) or (ev.type == KEYDOWN and ev.key == K_UP):
                        mixer.music.set_volume(mixer.music.get_volume() + 0.1)
                        print "Volume Increased to " + str(int(mixer.music.get_volume()*100)) + "%"
                    elif 'click' in volDownButton.handleEvent(ev) or (ev.type == KEYDOWN and ev.key == K_DOWN):
                        mixer.music.set_volume(mixer.music.get_volume() - 0.1)
                        print "Volume Decreased to " + str(int(mixer.music.get_volume()*100)) + "%"
                    elif 'click' in shuffleButton.handleEvent(ev) or (ev.type == KEYDOWN and ev.key == K_s):
                        i = 0
                        print "Shuffling..."
                        random.shuffle(playlist)
                        print "The shuffled playlist is:"
                        for song in playlist:
                            print os.path.basename(song)
                    elif 'click' in repeatButton.handleEvent(ev):
                        if mixer.music.get_busy():
                            pos = mixer.music.get_pos()
                            if repeat:
                                print "Repeat turned off"
                                repeat = False
                                repeatButton.bgcolor = (212,208,200)
                                mixer.music.play(0,pos)
                                if not mixer.music.get_busy():
                                    print "Music Over!"
                            else:
                                print "Repeat on for " + os.path.basename(playlist[i]).split('.')[0]
                                mixer.music.play(-1, pos)
                                repeat = True
                                repeatButton.bgcolor = (200,100,50)
                        else:
                            print ">_< No music to repeat!"
                    elif 'click' in searchButton.handleEvent(ev):
                        i = 0
                        A.bgcolor,B.bgcolor,searchButton.bgcolor = (212,208,200),(212,208,200),(100,200,100)
                        searchTerm = raw_input(" >> What do you want to search for? :")
                        playlist = [s for s in glob("*\\*.ogg") if searchTerm in s]
                        showList(playlist)
                    elif 'click' in A.handleEvent(ev):
                        i = 0
                        A.bgcolor,B.bgcolor,searchButton.bgcolor = (100,200,100),(212,208,200),(212,208,200)
                        playlist = glob("A\\*.ogg") + glob("A\\*.mp3") + glob("A\\*.mid")
                        showList(playlist)
                    elif 'click' in B.handleEvent(ev):
                        i = 0
                        A.bgcolor,B.bgcolor,searchButton.bgcolor = (212,208,200),(100,200,100),(212,208,200)
                        playlist = glob("B\\*.ogg") + glob("B\\*.mp3") + glob("B\\*.mid")
                        showList(playlist)
                
            # render game screen
            screen.fill( (0,0,0) ) # black background
            screen.blit(transform.scale(bg, dim), (0, 0),bgRect)
            prevButton.draw(screen)
            playButton.draw(screen)
            pauseButton.draw(screen)
            stopButton.draw(screen)
            nextButton.draw(screen)
            volUpButton.draw(screen)
            volDownButton.draw(screen)
            draw.rect(screen,(255 - mixer.music.get_volume()*100,mixer.music.get_volume()*100,200),(111,70,mixer.music.get_volume()*100,30))
            shuffleButton.draw(screen)
            repeatButton.draw(screen)
            A.draw(screen)
            B.draw(screen)
            searchButton.draw(screen)
            # update display
            display.update() # or display.flip()

    def quit(self):
        print "*** (^_^) Thank you for using this program! ***"


def main():
    screen = display.set_mode( dim, RESIZABLE)
    display.set_caption('Kasebsu Music Player')
    mouse.set_visible(True)

    player = Player()
    player.loop( screen )
    player.quit()

    quit()

if __name__ == '__main__':
    main()
