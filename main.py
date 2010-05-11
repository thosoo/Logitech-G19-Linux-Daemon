from logitech.g19 import G19
from logitech.g19_menu import G19Menu
#from logitech.applets.xplanet.xplanet import xplanet

import time

if __name__ == '__main__':
    lg19 = G19(True)
    lg19.start_event_handling()
    try:
        menu = G19Menu(lg19)
        lg19.add_applet(menu)
#        lg19.reset()
#        xplanet = xplanet(lg19)
#        lg19.add_applet(xplanet)

        while True:
            time.sleep(10)
    finally:
#        xplanet.stop()
        lg19.stop_event_handling()