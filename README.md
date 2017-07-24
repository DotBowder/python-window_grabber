## python-window_grabber
Adds a python 'window' class that uses the linux cli tool, 'xdotool' to retrieve any window's position, size, and other information.

## Dependancies:
> os

> sys

> subprocess

> termcolor

> xdotool

## Usage:
Create a window object by initializing the class.
The input_id can be specified with the xdotool window id.
The search_term can be specified to initiate a window search. The search will prompt the user to select one of the windows discovered by the search.
If no parameters are specified, or if the parameters are set to "", the user will be asked to provide a search term, and select a discovered window.

> window_object = window_grab.window(input_id="",search_term="")

After the window object is created, the object has 5 variables associated with it. These are the meat of the program, the very reason the program exists is to have access to these variables.

> window_object.name # Name of window

> window_object.xdotool_id # xdotool window id

> window_object.pid # PID of window

> window_object.pos # Position of window (x,y)

> window_object.size # Size of window (x,y)

Now that you have these variables, you can use them for anything.

To Update the window object with the new window position and size, call the xdotool_window_stat function attached to the window class. The update flag will update the class variables.

> window_object.xdotool_window_stat(update=True)

Now our window object has updated stats for the window we selected.
