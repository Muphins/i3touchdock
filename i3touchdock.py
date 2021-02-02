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
HOVBG='#303030'
dock = None
i3=i3ipc.Connection()
fpath='/usr/local/share/i3touchdock/res/'
isDockFloating = False
#####################
#	Functions dock	#
#####################
#---- Close dock
def mouseClickDockClose():
	global dock
#	print('close dock')
	dock.destroy()
	root.deiconify()

def workspacePrev():
	wsNum = int(i3.get_tree().find_focused().workspace().name.split(':')[0])
	if wsNum > 1:
		wsNum -= 1
		i3.command('workspace number ' + str(wsNum))

def workspaceNext():
	wsNum = int(i3.get_tree().find_focused().workspace().name.split(':')[0])
	if wsNum < 10:
		wsNum += 1
		i3.command('workspace number ' + str(wsNum))

def windowToWorkspacePrev():
	wsNum = int(i3.get_tree().find_focused().workspace().name.split(':')[0])
	if wsNum > 1:
		wsNum -= 1
		i3.command('move to workspace number ' + str(wsNum))

def windowToWorkspaceNext():
	wsNum = int(i3.get_tree().find_focused().workspace().name.split(':')[0])
	if wsNum < 10:
		wsNum += 1
		i3.command('move to workspace number ' + str(wsNum))

def windowToUp():
	i3.command('move up')

def windowToDown():
	i3.command('move down')

def windowToLeft():
	i3.command('move left')

def windowToRight():
	i3.command('move right')

def windowMaximizeToggle():
	i3.command('fullscreen toggle')

def windowFloatingToggle():
	i3.command('floating toggle')

superKeyPress=False
buttonWindowMove = None
def windowMove():
	global superKeyPress
	global buttonWindowMove
	if superKeyPress:
		superKeyPress=False
		os.system('xdotool keyup Super_L')
		buttonWindowMove.configure(bg='black', activebackground=HOVBG)
	else:
		superKeyPress=True
		os.system('xdotool keydown Super_L')
		buttonWindowMove.configure(bg='blue', activebackground='blue')

def windowClose():
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
	global buttonWindowMove
	root.withdraw()
	dock = tk.Toplevel(root, bg='black', borderwidth=0, highlightthickness=0)
	dock.title("dock")
	dock.geometry('800x48')
	dockCheckFullScreen(force=True)
	#dock.attributes('-type','dock')
	buttonDockHide				= tk.Button(dock, bd=0, highlightthickness=0, bg='black', activebackground=HOVBG, image=png_dockHide				, command=mouseClickDockClose	).pack(side=tk.RIGHT)
	buttonWorkspacePrev			= tk.Button(dock, bd=0, highlightthickness=0, bg='black', activebackground=HOVBG, image=png_workspacePrev			, command=workspacePrev			).pack(side=tk.LEFT)
	buttonWorkspaceNext			= tk.Button(dock, bd=0, highlightthickness=0, bg='black', activebackground=HOVBG, image=png_workspaceNext			, command=workspaceNext			).pack(side=tk.LEFT)
	buttonWindowToWorkspacePrev	= tk.Button(dock, bd=0, highlightthickness=0, bg='black', activebackground=HOVBG, image=png_windowToWorkspacePrev	, command=windowToWorkspacePrev	).pack(side=tk.LEFT)
	buttonWindowToWorkspaceNext	= tk.Button(dock, bd=0, highlightthickness=0, bg='black', activebackground=HOVBG, image=png_windowToWorkspaceNext	, command=windowToWorkspaceNext	).pack(side=tk.LEFT)
	buttonWindowToLeft			= tk.Button(dock, bd=0, highlightthickness=0, bg='black', activebackground=HOVBG, image=png_windowToLeft			, command=windowToLeft			).pack(side=tk.LEFT)
	buttonWindowToUp			= tk.Button(dock, bd=0, highlightthickness=0, bg='black', activebackground=HOVBG, image=png_windowToUp				, command=windowToUp			).pack(side=tk.LEFT)
	buttonWindowToDown			= tk.Button(dock, bd=0, highlightthickness=0, bg='black', activebackground=HOVBG, image=png_windowToDown			, command=windowToDown			).pack(side=tk.LEFT)
	buttonWindowToRight			= tk.Button(dock, bd=0, highlightthickness=0, bg='black', activebackground=HOVBG, image=png_windowToRight			, command=windowToRight			).pack(side=tk.LEFT)
	buttonWindowFloatingToggle	= tk.Button(dock, bd=0, highlightthickness=0, bg='black', activebackground=HOVBG, image=png_windowFloating			, command=windowFloatingToggle	).pack(side=tk.LEFT)
	buttonWindowMaximizeToggle	= tk.Button(dock, bd=0, highlightthickness=0, bg='black', activebackground=HOVBG, image=png_windowMaximize			, command=windowMaximizeToggle	).pack(side=tk.LEFT)
	buttonWindowMove			= tk.Button(dock, bd=0, highlightthickness=0, bg='black', activebackground=HOVBG, image=png_windowMove				, command=windowMove			)
	buttonWindowMove.pack(side=tk.LEFT)
	buttonWindowClose			= tk.Button(dock, bd=0, highlightthickness=0, bg='black', activebackground=HOVBG, image=png_windowClose				, command=windowClose			).pack(side=tk.LEFT)

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
canvas = tk.Canvas(root, bg='black', width=TD_W, height=TD_H)
canvas.config(highlightthickness=1)
canvas.bind('<Button-1>', mouseClickRootEvent)
canvas.pack()
canvas.create_image(TD_W/2,TD_H/2,image=png_teardropDock)

root.mainloop()
