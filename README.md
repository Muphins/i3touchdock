# i3 touch dock
It is a dock meant to provide basic control over the tiling window manager i3 using a touchscreen.  
I designed it to be used with a 5 inch 800x480 touchscreen with a Raspberry Pi.  
With it you can :
* Navigate through workspaces
* Move and resize windows, either as tiles or in floating mode
* Change windows state from Tiling to Floating, to Fullscreen
* Close windows

By default the dock is hiden, and a small arrow on top center of the screen allows to open it.  
  
# Dev notes
## transparency
I originaly wanted the top center arrow to be of a teardrop shape (as we see around the front facing camera of modern smartphones).  
I used Tkinter for its ease of integration. But it only allows to set the transparency of the entire window.  
Gtk+ should permit more control. But there seem to be some compatibility issue with i3.