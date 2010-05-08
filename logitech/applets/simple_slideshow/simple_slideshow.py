from logitech.g19 import *
from logitech.g19_keys import Key
from logitech.g19_receivers import *
from logitech.runnable import Runnable

import multiprocessing
import os
import tempfile
import threading
import time

class SlideshowInputProcessor(InputProcessor):
    '''Map the keys to the functions'''

    def __init__(self, slideshowrun):
        self.__slideshowrun = slideshowrun

    def process_input(self, inputEvent):
        processed = False
        if Key.RIGHT in inputEvent.keysDown:
            try:
                self.__slideshowrun.changeI("f")
                processed = True
            except IOError:
                print "File not found+"
        if Key.LEFT in inputEvent.keysDown:
            try:
                self.__slideshowrun.changeI("r")
                processed = True
            except IOError:
                print "File not found -"
                
        if Key.OK in inputEvent.keysDown:
            processed = True
            self.__slideshowrun.switchIsStarted()
            
        return processed

class SlideshowRun(Runnable):
    '''Lists Files in the given Directory and shows them on the screen'''
    def __init__(self, lg19, moviePath):
        if not os.path.isdir(moviePath):
            print "ERROR: Directory not found: "+moviePath
        else:
            Runnable.__init__(self)
            self.__i = 1
            self.__lg19 = lg19
            self.__location = moviePath
            self.__arrFiles = []
            self.__isStarted = False
##        if os.path.isdir(self.__location):
            try:
                for f in os.listdir(self.__location):
                    if os.path.isfile(os.path.join(self.__location, f)):
                        self.__arrFiles.append(f)
                        self.__i = self.__i+1
            except:
                print "IO Exception"
            self.update(0)
        Runnable.__init__(self)
##        else:
##            print "Folder "+self.__location+" not found"


    def execute(self):      
        if self.__isStarted:
            self.changeI("f")
        time.sleep(5)
    
    def switchIsStarted(self):
        self.__isStarted = not self.__isStarted

    def update(self, i):
        try:
            self.__lg19.load_image(os.path.join(self.__location, self.__arrFiles[i]))
        except IOError:            
            print "File "+ os.path.join(self.__location, self.__arrFiles[i])+" not found"
    def changeI(self, direction):
        if direction == "f":
            if self.__i < len(self.__arrFiles)-1:
                self.__i = self.__i+1
            else:
                self.__i = 0
            self.update(self.__i)
        if direction == "r":
            if self.__i == 0:
                self.__i = len(self.__arrFiles)-1
            else:
                self.__i = self.__i-1
            self.update(self.__i)
        return True

class Slideshow(object):

    def __init__(self, lg19, moviePath):
        if not os.path.isdir(moviePath):
            print "\n! ! !  ERROR: Directory not found: "+moviePath+" ! ! !\n"
            
        else:
            self.__lg19 = lg19
            self.__moviePath = moviePath
            self.__slideshowrun = SlideshowRun(lg19,self.__moviePath)        
            self.__inputProcessor = SlideshowInputProcessor(self.__slideshowrun)
            self.start()
        
    
    def get_input_processor(self):
        return self.__inputProcessor
    
    def start(self):
        t = threading.Thread(target=self.__slideshowrun.run)
        t.start()
    
    def stop(self):
        self.__slideshowrun.stop()

if __name__ == '__main__':
    lg19 = G19()
    slideshow = Slideshow(lg19)
    slideshow.start()
    try:
        while True:
            time.sleep(10)
    finally:
        slideshow.stop()