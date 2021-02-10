#!/bin/python3
import tkinter as tk
import time
import i3ipc
import os
from enum import Enum
#############
#	Enums	#
#############
class i3Mode(Enum):
	DEFAULT	= 0
	RESIZE	= 1
#############
#	Globals	#
#############
#---- Constants
TD_W = 48
TD_H = 20
ICON_W = 48
ICON_H = 48
HOVBG='#303030'
ICON_BG1='gray14'
ICON_BG2='gray20'
ICON_FG1='darkorange4'
#---- Files paths
fpath='/usr/local/share/i3touchdock/res/'
pngPath = fpath + "x48/"
#---- Flags
isDockFloating = False
superKeyPress=False
mode = i3Mode.DEFAULT
#---- i3ipc instance
i3=i3ipc.Connection()
#---- Tk instances
dock = None
canvasWindowToLeft	= None
canvasWindowToUp	= None
canvasWindowToDown	= None
canvasWindowToRight	= None
canvasModeResize	= None
#---- Images png
png_windowToUp		= None
png_windowToDown	= None
png_windowToLeft	= None
png_windowToRight	= None
png_growW			= None
png_growH			= None
png_shrinkW			= None
png_shrinkH			= None
#---- Tk images
image_left	= None
image_up	= None
image_down	= None
image_right	= None
#####################
#	Functions dock	#
#####################
#---- Close dock
def mouseClickDockClose(arg):
	global dock
#	print('close dock')
	dock.destroy()
	root.deiconify()
	
#---- Workspaces managment
def workspacePrev(arg):
	wsNum = int(i3.get_tree().find_focused().workspace().name.split(':')[0])
	if wsNum > 1:
		wsNum -= 1
		i3.command('workspace number ' + str(wsNum))

def workspaceNext(arg):
	wsNum = int(i3.get_tree().find_focused().workspace().name.split(':')[0])
	if wsNum < 10:
		wsNum += 1
		i3.command('workspace number ' + str(wsNum))

def windowToWorkspacePrev(arg):
	wsNum = int(i3.get_tree().find_focused().workspace().name.split(':')[0])
	if wsNum > 1:
		wsNum -= 1
		i3.command('move to workspace number ' + str(wsNum))

def windowToWorkspaceNext(arg):
	wsNum = int(i3.get_tree().find_focused().workspace().name.split(':')[0])
	if wsNum < 10:
		wsNum += 1
		i3.command('move to workspace number ' + str(wsNum))

#---- Windows move in workspace
def windowToUp(arg):
	i3.command('move up')

def windowToDown(arg):
	i3.command('move down')

def windowToLeft(arg):
	i3.command('move left')

def windowToRight(arg):
	i3.command('move right')

canvasWindowMove = None
def windowMove(arg):
	global superKeyPress
	global canvasWindowMove
	if superKeyPress:
		superKeyPress=False
		os.system('xdotool keyup Super_L')
		canvasWindowMove.configure(bg=ICON_BG2)
	else:
		superKeyPress=True
		os.system('xdotool keydown Super_L')
		canvasWindowMove.configure(bg=ICON_FG1)

#---- Windows resize
def modeResizeToggle(arg):
	global mode
	global canvasWindowToLeft
	global canvasWindowToUp
	global canvasWindowToDown
	global canvasWindowToRight
	global canvasModeResize
	global png_windowToUp		
	global png_windowToDown	
	global png_windowToLeft	
	global png_windowToRight	
	global png_growW			
	global png_growH			
	global png_shrinkW			
	global png_shrinkH			
	global image_left
	global image_up
	global image_down
	global image_right
	
	if not mode == i3Mode.RESIZE:
		mode = i3Mode.RESIZE
		i3.command('mode resize')
		canvasModeResize.configure(bg=ICON_FG1)
		# Change icons for resize mode
		canvasWindowToLeft	.itemconfig(image_left	,image=png_shrinkW	)
		canvasWindowToUp	.itemconfig(image_up	,image=png_shrinkH	)
		canvasWindowToDown	.itemconfig(image_down	,image=png_growH	)
		canvasWindowToRight	.itemconfig(image_right	,image=png_growW	)
		# Change bindings for resize mode
		canvasWindowToLeft			.bind('<Button-1>', windowShrinkWidth)
		canvasWindowToUp			.bind('<Button-1>', windowShrinkHeight)
		canvasWindowToDown			.bind('<Button-1>', windowGrowHeight	)
		canvasWindowToRight			.bind('<Button-1>', windowGrowWidth	)
	else:
		mode = i3Mode.DEFAULT
		i3.command('mode default')
		canvasModeResize.configure(bg=ICON_BG1)
		# Revert icons for default mode
		canvasWindowToLeft	.itemconfig(image_left	,image=png_windowToLeft	)
		canvasWindowToUp	.itemconfig(image_up	,image=png_windowToUp	)
		canvasWindowToDown	.itemconfig(image_down	,image=png_windowToDown	)
		canvasWindowToRight	.itemconfig(image_right	,image=png_windowToRight)
		# Revert bindings for default mode
		canvasWindowToLeft			.bind('<Button-1>', windowToLeft	)
		canvasWindowToUp			.bind('<Button-1>', windowToUp		)
		canvasWindowToDown			.bind('<Button-1>', windowToDown	)
		canvasWindowToRight			.bind('<Button-1>', windowToRight	)

def windowGrowHeight(arg):
	i3.command('resize grow height 10 px or 5 ppt')

def windowShrinkHeight(arg):
	i3.command('resize shrink height 10 px or 5 ppt')

def windowGrowWidth(arg):
	i3.command('resize grow width 10 px or 5 ppt')

def windowShrinkWidth(arg):
	i3.command('resize shrink width 10 px or 5 ppt')

def windowMaximizeToggle(arg):
	i3.command('fullscreen toggle')

def windowFloatingToggle(arg):
	i3.command('floating toggle')

#---- Handle Dock layout to be always visible
def dockCheckFullScreen(force=False):
	global dock
	global isDockFloating
	dock.after(500, dockCheckFullScreen)
	cur_ws = i3.get_tree().find_focused().workspace().leaves()
	topWinCnt = 0
	flag = False
	if cur_ws:
		for child in cur_ws:
			if child.fullscreen_mode > 0:
				topWinCnt += 1
			if child.floating.find('on') > 1:
				topWinCnt += 1
		if topWinCnt > 0:
			if not isDockFloating or force:
				print('float')
				isDockFloating = True
				flag = True
				dock.withdraw()
				dock.overrideredirect(1)
				dock.attributes('-type','utility')
				#dock.attributes('-topmost','true')
		else:
			if isDockFloating or force:
				print('un-float')
				isDockFloating = False
				flag = True
				dock.withdraw()
				dock.attributes('-type','dock')
				dock.overrideredirect(0)
	elif force:
		print('desktop')
		isDockFloating = False
		flag = True
		dock.withdraw()
		dock.attributes('-type','dock')
		dock.overrideredirect(0)
	if flag:
		dock.after(10,dock.deiconify)

#---- Window close
def windowClose(arg):
	i3.command('kill')

#########################
#	Functions teardrop	#
#########################
#---- Open dock
def mouseClickDockOpen(arg):
	print('open dock')
	global dock
	global canvasWindowToLeft
	global canvasWindowToUp
	global canvasWindowToDown
	global canvasWindowToRight
	global canvasWindowMove
	global canvasModeResize
	global image_left
	global image_up
	global image_down
	global image_right
	root.withdraw()
	dock = tk.Toplevel(root, bg=ICON_BG1, borderwidth=0, highlightthickness=0)
	dock.title("dock")
	dock.geometry('800x48')
	dockCheckFullScreen(force=True)
	#dock.attributes('-type','dock')
	canvasWorkspacePrev			= tk.Canvas(dock, bd=0, highlightthickness=0, bg=ICON_BG2, width=ICON_W, height=ICON_H)
	canvasWorkspaceNext			= tk.Canvas(dock, bd=0, highlightthickness=0, bg=ICON_BG2, width=ICON_W, height=ICON_H)
	canvasWindowToWorkspacePrev	= tk.Canvas(dock, bd=0, highlightthickness=0, bg=ICON_BG1, width=ICON_W, height=ICON_H)
	canvasWindowToWorkspaceNext	= tk.Canvas(dock, bd=0, highlightthickness=0, bg=ICON_BG1, width=ICON_W, height=ICON_H)
	canvasWindowToLeft			= tk.Canvas(dock, bd=0, highlightthickness=0, bg=ICON_BG2, width=ICON_W, height=ICON_H)
	canvasWindowToRight			= tk.Canvas(dock, bd=0, highlightthickness=0, bg=ICON_BG2, width=ICON_W, height=ICON_H)
	canvasWindowToUp			= tk.Canvas(dock, bd=0, highlightthickness=0, bg=ICON_BG2, width=ICON_W, height=ICON_H)
	canvasWindowToDown			= tk.Canvas(dock, bd=0, highlightthickness=0, bg=ICON_BG2, width=ICON_W, height=ICON_H)
	canvasModeResize			= tk.Canvas(dock, bd=0, highlightthickness=0, bg=ICON_BG1, width=ICON_W, height=ICON_H)
	canvasWindowFloatingToggle	= tk.Canvas(dock, bd=0, highlightthickness=0, bg=ICON_BG2, width=ICON_W, height=ICON_H)
	canvasWindowMove			= tk.Canvas(dock, bd=0, highlightthickness=0, bg=ICON_BG2, width=ICON_W, height=ICON_H)
	canvasWindowMaximizeToggle	= tk.Canvas(dock, bd=0, highlightthickness=0, bg=ICON_BG1, width=ICON_W, height=ICON_H)
	canvasWindowClose			= tk.Canvas(dock, bd=0, highlightthickness=0, bg=ICON_BG2, width=ICON_W, height=ICON_H)
	canvasDockHide				= tk.Canvas(dock, bd=0, highlightthickness=0, bg=ICON_BG1, width=ICON_W, height=ICON_H)
	
	canvasDockHide				.bind('<Button-1>', mouseClickDockClose		)
	canvasWorkspacePrev			.bind('<Button-1>', workspacePrev			)
	canvasWorkspaceNext			.bind('<Button-1>', workspaceNext			)
	canvasWindowToWorkspacePrev	.bind('<Button-1>', windowToWorkspacePrev	)
	canvasWindowToWorkspaceNext	.bind('<Button-1>', windowToWorkspaceNext	)
	canvasWindowToLeft			.bind('<Button-1>', windowToLeft			)
	canvasWindowToUp			.bind('<Button-1>', windowToUp				)
	canvasWindowToDown			.bind('<Button-1>', windowToDown			)
	canvasWindowToRight			.bind('<Button-1>', windowToRight			)
	canvasWindowFloatingToggle	.bind('<Button-1>', windowFloatingToggle	)
	canvasWindowMaximizeToggle	.bind('<Button-1>', windowMaximizeToggle	)
	canvasWindowMove			.bind('<Button-1>', windowMove				)
	canvasModeResize			.bind('<Button-1>', modeResizeToggle		)
	canvasWindowClose			.bind('<Button-1>', windowClose				)
	
	canvasWorkspacePrev			.pack(side=tk.LEFT)
	canvasWorkspaceNext			.pack(side=tk.LEFT)
	canvasWindowToWorkspacePrev	.pack(side=tk.LEFT)
	canvasWindowToWorkspaceNext	.pack(side=tk.LEFT)
	canvasWindowToLeft			.pack(side=tk.LEFT)
	canvasWindowToRight			.pack(side=tk.LEFT)
	canvasWindowToUp			.pack(side=tk.LEFT)
	canvasWindowToDown			.pack(side=tk.LEFT)
	canvasModeResize			.pack(side=tk.LEFT)
	canvasWindowFloatingToggle	.pack(side=tk.LEFT)
	canvasWindowMove			.pack(side=tk.LEFT)
	canvasWindowMaximizeToggle	.pack(side=tk.LEFT)
	canvasWindowClose			.pack(side=tk.LEFT)
	canvasDockHide				.pack(side=tk.RIGHT)
	
	canvasDockHide				.create_image(ICON_W/2,ICON_H/2,image=png_dockHide				)
	canvasWorkspacePrev			.create_image(ICON_W/2,ICON_H/2,image=png_workspacePrev			)
	canvasWorkspaceNext			.create_image(ICON_W/2,ICON_H/2,image=png_workspaceNext			)
	canvasWindowToWorkspacePrev	.create_image(ICON_W/2,ICON_H/2,image=png_windowToWorkspacePrev	)
	canvasWindowToWorkspaceNext	.create_image(ICON_W/2,ICON_H/2,image=png_windowToWorkspaceNext	)
	canvasWindowFloatingToggle	.create_image(ICON_W/2,ICON_H/2,image=png_windowFloating		)
	canvasWindowMaximizeToggle	.create_image(ICON_W/2,ICON_H/2,image=png_windowMaximize		)
	canvasWindowMove			.create_image(ICON_W/2,ICON_H/2,image=png_windowMove			)
	canvasModeResize			.create_image(ICON_W/2,ICON_H/2,image=png_modeResize			)
	canvasWindowClose			.create_image(ICON_W/2,ICON_H/2,image=png_windowClose			)
	image_left	= canvasWindowToLeft	.create_image(ICON_W/2,ICON_H/2,image=png_windowToLeft			)
	image_up 	= canvasWindowToUp		.create_image(ICON_W/2,ICON_H/2,image=png_windowToUp			)
	image_down	= canvasWindowToDown	.create_image(ICON_W/2,ICON_H/2,image=png_windowToDown			)
	image_right	= canvasWindowToRight	.create_image(ICON_W/2,ICON_H/2,image=png_windowToRight			)

#############
#	Main	#
#############
#---- root window definition
root = tk.Tk(className='i3touchcontrol')
root.geometry("48x20+376+0")
root.overrideredirect(1)
root.attributes('-type','utility')
#root.config(bg='black')
#---- Teardrop dock icon
png_teardropDock = tk.PhotoImage(file=fpath + "teardropDock.png")
#---- Buttons images
png_dockHide				= tk.PhotoImage(file = pngPath + "dock-hide.png")
png_workspacePrev			= tk.PhotoImage(file = pngPath + "workspace-prev.png")
png_workspaceNext			= tk.PhotoImage(file = pngPath + "workspace-next.png")
png_windowToWorkspacePrev	= tk.PhotoImage(file = pngPath + "window-to-prev.png")
png_windowToWorkspaceNext	= tk.PhotoImage(file = pngPath + "window-to-next.png")
png_windowToUp				= tk.PhotoImage(file = pngPath + "window-to-up.png")
png_windowToDown			= tk.PhotoImage(file = pngPath + "window-to-down.png")
png_windowToLeft			= tk.PhotoImage(file = pngPath + "window-to-left.png")
png_windowToRight			= tk.PhotoImage(file = pngPath + "window-to-right.png")
png_windowFloating			= tk.PhotoImage(file = pngPath + "window-floating-alt.png")
png_windowMaximize			= tk.PhotoImage(file = pngPath + "window-maximize.png")
png_windowMove				= tk.PhotoImage(file = pngPath + "window-move.png")
png_modeResize				= tk.PhotoImage(file = pngPath + "window-resize.png")
png_windowClose				= tk.PhotoImage(file = pngPath + "window-close.png")
png_growW					= tk.PhotoImage(file = pngPath + "window-grow-w.png")
png_growH					= tk.PhotoImage(file = pngPath + "window-grow-h.png")
png_shrinkW					= tk.PhotoImage(file = pngPath + "window-shrink-w.png")
png_shrinkH					= tk.PhotoImage(file = pngPath + "window-shrink-h.png")

# display teardrop
canvasTeardrop = tk.Canvas(root, bg='black', width=TD_W, height=TD_H)
canvasTeardrop.config(highlightthickness=1)
canvasTeardrop.bind('<Button-1>', mouseClickDockOpen)
canvasTeardrop.pack()
canvasTeardrop.create_image(TD_W/2,TD_H/2,image=png_teardropDock)

root.mainloop()
