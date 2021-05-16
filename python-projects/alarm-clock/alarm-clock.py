#!/usr/local/bin/python3.9

import time
from string import whitespace
from playsound import playsound
from termcolor import colored
from sys import exit
import signal

class Alarm(object):
    def __init__(self):
        self.t = self.set()
        signal.signal(signal.SIGINT,self.catch)
    def ring(self):
        for i in range(5):
            alarm_file = "sounds/alarm.mp3"
            playsound(alarm_file)
    def activate(self):
       while True:
        if time.time() == self.t:
                self.ring()
                break                 
    def set(self):
        try:
            prompt = colored("[Day] [Month] [Hour] [Min] [Sec] [Year]\n","blue",attrs=["bold"])
            day, month, hour, minute, sec, year = input(prompt).split()
            time_input = day + whitespace + month + whitespace + hour + whitespace + minute + whitespace + sec + whitespace + year
            t = time.strptime(time_input,"%d %B %H %M %S %Y") #time struct
            msg = colored("Alarm set for ","red")
            msg_time = colored(time.asctime(t),"red",attrs=["blink"])
            print(msg,end="")
            print(msg_time)
    
            return time.mktime(t) # time float
        except (TypeError,ValueError):
            print("Wrong input")
            exit(-1)
    def catch(self, signum,frame):
        print("Alarm cancelled")
        exit(1)


def main():
    a = Alarm()
    a.activate()
     
if __name__ == "__main__": main()



        


