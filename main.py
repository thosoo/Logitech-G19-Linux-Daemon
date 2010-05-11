from logitech.g19 import G19
from logitech.g19_menu import G19Menu
#from logitech.applets.simple_slideshow.simple_slideshow import slideshow
#from logitech.applets.simple_clock.simple_clock import clock

import time

if __name__ == '__main__':
    lg19 = G19(True)
    lg19.start_event_handling()
    try:
#        menu = G19Menu(lg19)
#        lg19.add_applet(menu)

#        clock = clock(lg19)
#        lg19.add_applet(clock)
##
##        xplanet = Xplanet(lg19)
##        lg19.add_applet(xplanet)
##
##        displayBrightness = SimpleDisplayBrightness(lg19)
##        lg19.add_applet(displayBrightness)

#        slideshow = slideshow(lg19, "logitech/applets/simple_slideshow/pics")
#        lg19.add_applet(slideshow)

        while True:
            time.sleep(10)
    finally:
#        clock.stop()
##        xplanet.stop()
#        slideshow.stop()
        lg19.stop_event_handling()