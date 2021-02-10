#!/bin/python3
import tkinter as tk
import time
import i3ipc
import os
#############
#	Globals	#
#############
TD_W = 48
TD_H = 20
ICON_W = 48
ICON_H = 48
HOVBG='#303030'
INCON_BG='black'
dock = None
i3=i3ipc.Connection()
fpath='/usr/local/share/i3touchdock/res/'
isDockFloating = False
#####################
#	Functions dock	#
#####################
#---- Close dock
def mouseClickDockClose(arg):
	global dock
#	print('close dock')
	dock.destroy()
	root.deiconify()

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

def windowToUp(arg):
	i3.command('move up')

def windowToDown(arg):
	i3.command('move down')

def windowToLeft(arg):
	i3.command('move left')

def windowToRight(arg):
	i3.command('move right')

def windowMaximizeToggle(arg):
	i3.command('fullscreen toggle')

def windowFloatingToggle(arg):
	i3.command('floating toggle')

superKeyPress=False
canvasWindowMove = None
def windowMove(arg):
	global superKeyPress
	global canvasWindowMove
	if superKeyPress:
		superKeyPress=False
		os.system('xdotool keyup Super_L')
		canvasWindowMove.configure(bg='black')
	else:
		superKeyPress=True
		os.system('xdotool keydown Super_L')
		canvasWindowMove.configure(bg='blue')

def windowClose(arg):
	i3.command('kill')

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

#########################
#	Functions teardrop	#
#########################
#---- Open dock
def mouseClickRootEvent(arg):
	print('open dock')
	global dock
	global canvasWindowMove
	root.withdraw()
	dock = tk.Toplevel(root, bg='black', borderwidth=0, highlightthickness=0)
	dock.title("dock")
	dock.geometry('800x48')
	dockCheckFullScreen(force=True)
	#dock.attributes('-type','dock')
	canvasDockHide				= tk.Canvas(dock, bd=0, highlightthickness=0, bg=INCON_BG, width=ICON_W, height=ICON_H)
	canvasWorkspacePrev			= tk.Canvas(dock, bd=0, highlightthickness=0, bg=INCON_BG, width=ICON_W, height=ICON_H)
	canvasWorkspaceNext			= tk.Canvas(dock, bd=0, highlightthickness=0, bg=INCON_BG, width=ICON_W, height=ICON_H)
	canvasWindowToWorkspacePrev	= tk.Canvas(dock, bd=0, highlightthickness=0, bg=INCON_BG, width=ICON_W, height=ICON_H)
	canvasWindowToWorkspaceNext	= tk.Canvas(dock, bd=0, highlightthickness=0, bg=INCON_BG, width=ICON_W, height=ICON_H)
	canvasWindowToLeft			= tk.Canvas(dock, bd=0, highlightthickness=0, bg=INCON_BG, width=ICON_W, height=ICON_H)
	canvasWindowToUp			= tk.Canvas(dock, bd=0, highlightthickness=0, bg=INCON_BG, width=ICON_W, height=ICON_H)
	canvasWindowToDown			= tk.Canvas(dock, bd=0, highlightthickness=0, bg=INCON_BG, width=ICON_W, height=ICON_H)
	canvasWindowToRight			= tk.Canvas(dock, bd=0, highlightthickness=0, bg=INCON_BG, width=ICON_W, height=ICON_H)
	canvasWindowFloatingToggle	= tk.Canvas(dock, bd=0, highlightthickness=0, bg=INCON_BG, width=ICON_W, height=ICON_H)
	canvasWindowMaximizeToggle	= tk.Canvas(dock, bd=0, highlightthickness=0, bg=INCON_BG, width=ICON_W, height=ICON_H)
	canvasWindowMove			= tk.Canvas(dock, bd=0, highlightthickness=0, bg=INCON_BG, width=ICON_W, height=ICON_H)
	canvasWindowClose			= tk.Canvas(dock, bd=0, highlightthickness=0, bg=INCON_BG, width=ICON_W, height=ICON_H)
	
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
	canvasWindowClose			.bind('<Button-1>', windowClose				)
	
	canvasDockHide				.pack(side=tk.RIGHT)
	canvasWorkspacePrev			.pack(side=tk.LEFT)
	canvasWorkspaceNext			.pack(side=tk.LEFT)
	canvasWindowToWorkspacePrev	.pack(side=tk.LEFT)
	canvasWindowToWorkspaceNext	.pack(side=tk.LEFT)
	canvasWindowToLeft			.pack(side=tk.LEFT)
	canvasWindowToUp			.pack(side=tk.LEFT)
	canvasWindowToDown			.pack(side=tk.LEFT)
	canvasWindowToRight			.pack(side=tk.LEFT)
	canvasWindowFloatingToggle	.pack(side=tk.LEFT)
	canvasWindowMaximizeToggle	.pack(side=tk.LEFT)
	canvasWindowMove			.pack(side=tk.LEFT)
	canvasWindowClose			.pack(side=tk.LEFT)
	
	canvasDockHide				.create_image(ICON_W/2,ICON_H/2,image=png_dockHide				)
	canvasWorkspacePrev			.create_image(ICON_W/2,ICON_H/2,image=png_workspacePrev			)
	canvasWorkspaceNext			.create_image(ICON_W/2,ICON_H/2,image=png_workspaceNext			)
	canvasWindowToWorkspacePrev	.create_image(ICON_W/2,ICON_H/2,image=png_windowToWorkspacePrev	)
	canvasWindowToWorkspaceNext	.create_image(ICON_W/2,ICON_H/2,image=png_windowToWorkspaceNext	)
	canvasWindowToLeft			.create_image(ICON_W/2,ICON_H/2,image=png_windowToLeft			)
	canvasWindowToUp			.create_image(ICON_W/2,ICON_H/2,image=png_windowToUp			)
	canvasWindowToDown			.create_image(ICON_W/2,ICON_H/2,image=png_windowToDown			)
	canvasWindowToRight			.create_image(ICON_W/2,ICON_H/2,image=png_windowToRight			)
	canvasWindowFloatingToggle	.create_image(ICON_W/2,ICON_H/2,image=png_windowFloating		)
	canvasWindowMaximizeToggle	.create_image(ICON_W/2,ICON_H/2,image=png_windowMaximize		)
	canvasWindowMove			.create_image(ICON_W/2,ICON_H/2,image=png_windowMove			)
	canvasWindowClose			.create_image(ICON_W/2,ICON_H/2,image=png_windowClose			)

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

pngPath = fpath + "x48/"
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
png_windowFloating			= tk.PhotoImage(file = pngPath + "window-floating.png")
png_windowMaximize			= tk.PhotoImage(file = pngPath + "window-maximize.png")
png_windowMove				= tk.PhotoImage(file = pngPath + "window-move.png")
png_windowClose				= tk.PhotoImage(file = pngPath + "window-close.png")

# display teardrop
canvasTeardrop = tk.Canvas(root, bg=INCON_BG, width=TD_W, height=TD_H)
canvasTeardrop.config(highlightthickness=1)
canvasTeardrop.bind('<Button-1>', mouseClickRootEvent)
canvasTeardrop.pack()
canvasTeardrop.create_image(TD_W/2,TD_H/2,image=png_teardropDock)

root.mainloop()
