from g19_receivers import G19Receiver
from logitech.g19 import *
from logitech.g19_keys import Key
from logitech.g19_receivers import *

import os

class G19Menu(object):
    def __init__(self, lg19):
        self.__applet_dir = "logitech/applets/"
        self.__lg19 = lg19
        self.__applets = []
        self.__menuOnly = False
        self.__firstItem = 1
        self.__selectedItem = 1
        self.__selection = 1
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
                self.__selectedItem -= 1
            if self.__selection > 0:
                self.__selection += direction

        if direction == 1:
            if self.__selectedItem < len(self.__applets):
                 self.__selectedItem = self.__selectedItem + 1
                 self.__selection += direction

        self.showMenu(self.__applets)
    
    def get_input_processor(self):
        return self.__inputProcessor
    
    def startSelected(self):
        g19 = self.__lg19        
        try:
            applet = self.__applets[self.__selection]
            call = applet.split("_")
            appletname = call[len(call)-1]
            exec 'from logitech.applets.' + applet + '.' + applet + ' import '+ appletname
            exec 'selectedApplet ='+ appletname+'(g19)'
            self.__menuOnly = True
            g19.add_applet(selectedApplet)
            self.__selectedApplet = selectedApplet
        finally:
            pass

    def stopSelected(self):
        if self.__menuOnly == True:
            try:
                self.__selectedApplet.stop()
            finally:
                self.__lg19.remove_applet(self.__selectedApplet)
                self.__menuOnly = False
        self.showMenu(self.__applets)
        
    def showMenu(self, menuEntries):
        i = 1
        if self.__selection+1 > self.__firstItem+6:
            if self.__firstItem+6 < len(menuEntries):
                self.__firstItem +=1
            self.__selectedItem = 7
        if self.__selection+1 < self.__firstItem:
            self.__firstItem -=1
            self.__selectedItem = 1
        self.__lg19.clear_text()
        for j in range(self.__firstItem, self.__firstItem+7):
            if j <= len(menuEntries):
                if i == self.__selectedItem:
                    self.__lg19.load_text("-> "+menuEntries[j-1], i)
                    self.__selection = j-1
                else:
                    self.__lg19.load_text(menuEntries[j-1], i)
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
    
