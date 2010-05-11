#!/usr/bin/env python

from runnable import Runnable
from g19_receivers import G19Receiver
from logitech.g19 import *
from logitech.g19_keys import Key
from logitech.g19_receivers import *
#try:
#    for f in os.listdir("logitech/applets/"):
#        if os.path.isdir(os.path.join("logitech/applets/", f)):
#            call = f.split("_")
#            appletname = call[len(call)-1]
#            exec 'from logitech.applets.' + f + '.' + f + ' import '+ appletname
#except:
#    print "IO Exception"

import sys
import threading
import time
import usb
import PIL.Image as Img
import os
import ImageFont
import Image, ImageDraw

class G19Menu(object):
    def __init__(self, lg19):
        self.__applet_dir = "logitech/applets/"
        self.__lg19 = lg19
        self.__applets = []
        self.__menuOnly = False
        self.__selectedItem = 1
        self.__inputProcessor = MenuInputProcessor(self)
        try:
            for f in os.listdir(self.__applet_dir):
                if os.path.isdir(os.path.join(self.__applet_dir, f)):
                    self.__applets.append(f)
        except:
            print "IO Exception"
        self.showMenu(self.__applets)
    
    def getMenuOnly(self):
        return self.__menuOnly
    
    def changeSelection(self, direction):
        if direction == -1:
            if self.__selectedItem > 1:
                self.__selectedItem = self.__selectedItem - 1
        if direction == 1:
            if self.__selectedItem < len(self.__applets):
                 self.__selectedItem = self.__selectedItem + 1
        self.showMenu(self.__applets)
    
    def get_input_processor(self):
        return self.__inputProcessor
    
    def startSelected(self):
        g19 = self.__lg19        
        try:
            applet = self.__applets[self.__selectedItem-1]
            call = applet.split("_")
            appletname = call[len(call)-1]
            exec 'from logitech.applets.' + applet + '.' + applet + ' import '+ appletname
            exec 'selectedApplet ='+ appletname+'(g19)'
#            g19.remove_applet(self)
            self.__menuOnly = True
#            g19.add_applet(self)
            g19.add_applet(selectedApplet)

            self.__selectedApplet = selectedApplet
#            while True:
#                time.sleep(10)
        finally:
            i = 1
#            selectedApplet.stop()
#            self.showMenu(self.__applets)

    def stopSelected(self):
        self.__selectedApplet.stop()
        self.__lg19.remove_applet(self.__selectedApplet)
        self.__menuOnly = False
#        g19.add_applet(self)
        self.showMenu(self.__applets)
        


    def showMenu(self, menuEntries):
        i = 1
        j=1
        self.__lg19.clear_text()
        for f in menuEntries:
            if i == self.__selectedItem:
                self.__lg19.load_text("-> "+f, i)
            else:
                self.__lg19.load_text(f, i)
            i = i+1
        self.__lg19.set_text()

class MenuInputProcessor(InputProcessor):
    '''Map the keys to the functions'''

    def __init__(self, menu):
        self.__menu = menu

    def process_input(self, inputEvent):
        processed = False
        if not self.__menu.getMenuOnly():
            if Key.UP in inputEvent.keysDown:
                self.__menu.changeSelection(-1)
                processed = True
        
            if Key.DOWN in inputEvent.keysDown:
                self.__menu.changeSelection(1)
                processed = True
            
            if Key.OK in inputEvent.keysDown:
                self.__menu.startSelected()
        
        if Key.MENU in inputEvent.keysDown:
            self.__menu.stopSelected()                

        return processed
    
