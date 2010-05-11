=== Logitech G19 Linux support ===

This is work in progress and considered absolutely alpha.  It SHOULD work, but no
guarantees are given.  If your keyboard goes up in flames, explodes and rapes
your hamster, don't say I didn't warn you!

This are my (sBlatt) additions to MultiCoreNOPs code, search für him @ gitHub if you want the original code


=== What you need to use this ===

Python 2.6
pyusb

optional:
PySide (not yet)

=== How to install ===

- Get the code
- unzip to any location
- start a terminal
- cd to the folder
- type sudo python main.py (usb needs root, change your permissions if you want to start this as a normal user)

=== How it works ===

- The menu shows your installed applets. As of now (11.5.10) only the simple_slideshow and simple_clock-applets have been tested, the others might work
- Navigate with your display-keys
- Press OK to start an applet
- Press MENU to go back to the Menu (there is a chance the applet wil reapear on its own, just press MENU again)

- if anything goes wrong: sudo killall python (might kill some other processes)

==== Special Keys ====
- After starting, you can map the G-Keys like any other Multimedia-Key (in Gnome: Menu->System->Preferences-> Keyboard Shortcuts
- The Standardkeys (Play, Mute, ...) should already be mapped, if not you can map them like the G-Keys

==== Slideshow ====

- Put pictures to logitech/applets/simple_slideshow/pics/ (or change path in the simple_slideshow.py file)
- Press OK to start automated slideshow
- Press UP/DOWN to change slideshow-delay (standard is 5sec, 1sec/step)


=== Infos for developers ===

==== Naming convention ====

- ATM you have to name your applet file the same as your applet folder (otherwise the menu won't find it)
- ATM the name of your main-class has to be the same as your folder/filename after the last "_"
	exp. simple_slideshow: class name is slideshow; xplanet: class name is xplanet; simple_bg_light: class name is light 

==== Key-Problems ====

- Don't use the MENU-Key in your application, as it is used to terminate it.
- If you use the G- or MultimediaKeys, more than 1 action may be triggered




------------------------ Original readmy by MultiCoreNOP--------------------------------------




=== What I want to do ===

Refactor and build an API+framework for applets.
Developers will get a simple way to create mini-programs of any kind.  An
infrastructure providing a base menu to select/activate applets and easy
possibilities to integrate into input handling will created.

So far it does not make much sense to start developing on the current code base
(as I just started to create this one week ago).  As soon as I stopped
experimenting, I'll change this file.


=== What it does right now ===

If invoked by "python main.py":

--- Color ---

By selecting M1..3 you select red/green/blue for manipulation.  Using the scroll
you can adjust the current backlight value.


--- Color ---

If no M-button is selected, scrolling will change the display brightness.


--- Xplanet ---

If you have 'xplanet' installed, you can press the "play"/"stop" buttons to
rotate the earth in your display.

(After pressing start, 360 images will be generated using as many CPUs as you
have, but nonetheless it will take up to three minutes.)

Currently I am working on supporting Qt on the display - let's see how far I
get...


=== How you can send anything you want to your G19 ===

Fire up a python shell.  The main API is logitech.g19.G19 atm:

>>> from logitech.g19 import G19

# if you get an error: lg19 = G19(True)
>>> lg19 = G19()

# setting backlight to red
>>> lg19.set_bg_color(255, 0, 0)

# fill your display with green
>>> lg19.fill_display_with_color(0, 255, 0)

# test your screen
>>> lg19.set_display_colorful()

# set backlight to blue after reset
# this will be your backlight color after a bus reset (or switching the keyboard
# off and no)
>>> lg19.save_default_bg_color(0, 0, 255)

# send an image to display
>>> data = [...] # format described in g19.py
>>> lg19.send_frame(data)

# load an arbitrary image from disk to display (will be resized non-uniform)
>>> lg19.load_image("/path/to/myimage.jpg")

# reset the keyboard via USB
>>> lg19.reset()
# now you have to rebuild the connection:
>>> lg19 = G19()


HINT: After creating a G19 object, your "light key" will not work anymore,
      because the keyboard waits for you to read its data.  You can start doing
      so by calling lg19.start_event_handling().
      (have a look at main.py)



As soon as I reach a stable point, I promise to write a lot of documentation. ;-)
