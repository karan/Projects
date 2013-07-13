"""
Alarm Clock - A simple clock where it plays a sound after
X number of minutes/seconds or at a particular time.

Dependencies:
pyglet
    pip install pyglet
"""

import time
import winsound
import pyglet

if __name__ == '__main__':
    hh = input('What hour do you want to wake up (0-23)? ')
    mm = input('What minute do you want to wake up (0-59)? ')

    not_alarmed = 1

    while(not_alarmed):
        cur_time = list(time.localtime()) # get the time right now
        hour = cur_time[3] # find the hour
        minute = cur_time[4] # and the minute
        if hour == hh and minute == mm:
            song = pyglet.media.load('bin/sound.wav')
            song.play() # play the sound
            pyglet.app.run()
            not_alarmed = 0 # stop the loop

