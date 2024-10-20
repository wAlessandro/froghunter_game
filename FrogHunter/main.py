
from tkinter import *
from tkinter import font
from objects import Background
from assets import SPRITE
import configs
from time import sleep
import math
#WINDOW
window = Tk()
window.title("FrogHunter")
window.geometry(f"{configs.SCREENWIDHT}x{configs.SCREENHEIGHT}")
window.resizable(False,False)
window.config(bg="black")
#IMAGES
BACKGROUNDIMAGE = PhotoImage(file=SPRITE["lakebackground"])
PLAYERRIGHT = PhotoImage(file=SPRITE["playerright"])
PLAYERLEFT = PhotoImage(file=SPRITE["playerleft"])
PLAYERATACKLEFT = PhotoImage(file=SPRITE["playeratackleft"])
PLAYERATACKRIGHT = PhotoImage(file=SPRITE["playeratackright"])
HEARTICON = PhotoImage(file=SPRITE["hearticon"])
DAMAGEICON = PhotoImage(file=SPRITE["damageicon"])
BOSSESICONS = [SPRITE["frogbossicon"],]
FROGBOSSICON = PhotoImage(file=BOSSESICONS[0])
FROGBOSSIMAGE = PhotoImage(file=SPRITE["frogboss"])
SLEEPBOSS = PhotoImage(file=SPRITE["sleepingfrogboss"])
#INTERFACE
window.rowconfigure(0,weight=1)
window.rowconfigure(1,weight=1)
window.rowconfigure(2,weight=1)
window.columnconfigure(0,weight=1)
player_status = Frame(window,width=800,)
player_status.grid(row=2,column=0,ipady=0,sticky="sw")
heart = [i for i in range(configs.PLAYERHEALTH)]
for column in range(configs.PLAYERHEALTH):
    heart[column] = Label(player_status, image=HEARTICON,name=str(column),bg="black",)
    heart[column].grid(row=0,column=column)
playerat_ackicon = Label(player_status,bg="black",image=DAMAGEICON)
playerat_ackicon.grid(row=0,column=configs.PLAYERHEALTH+1,sticky="e")
player_atacklabel = Label(player_status, text=configs.PLAYERDAMAGE,fg="red",\
     font=("Arial Black",10),bg="black")
player_atacklabel.grid(row=0,column=configs.PLAYERHEALTH+1,sticky="nw")
canvas = Canvas(window,width=configs.SCREENWIDHT-80,height=configs.SCREENHEIGHT-50,\
    bg="black",borderwidth=5,highlightthickness=0)
canvas.grid(row=1,column=0,sticky="nswe",pady=0)
bosshealth = Label(window, text=configs.BOSSHEALTH,bg="#df0808",width=configs.BOSSHEALTH,height=1,font=("Arial Black",10))
bosshealth.grid(row=1,column=0,sticky="n")
BACKGROUND = canvas.create_image(450,290,image=BACKGROUNDIMAGE)
#PLAYERS
PLAYER = canvas.create_image(20,20, image=PLAYERRIGHT)
pwidht = PLAYERRIGHT.width() + 40
pheight = PLAYERRIGHT.height() + 40
BOSS = canvas.create_image(580,270, image=FROGBOSSIMAGE)
bwidth = FROGBOSSIMAGE.width() - 40
bheight = FROGBOSSIMAGE.height() - 40
#FUCTIONS
mouse_eventvar = BooleanVar()
mouse_eventvar.set(False)
def damageonnpc(npchealthbar):
    if configs.BOSSHEALTH > 0:
        configs.BOSSHEALTH -= configs.PLAYERDAMAGE
        npchealthbar.configure(text=configs.BOSSHEALTH, width=configs.BOSSHEALTH)
        sleep(0.05)
def damageonplayer():
    if configs.BOSSHEALTH > 0 and colision_Detection()\
     and configs.PLAYERHEALTH > 0:
        def damage():
            configs.PLAYERHEALTH -= configs.BOSSDAMAGE
            heart[configs.PLAYERHEALTH].destroy()
        canvas.after(100, damage())
        return True
    else:
        return False
movingsym = StringVar()
def moving(bindarg=None):
    if configs.PLAYERHEALTH > 0:
        if bindarg.keysym == "d":
            canvas.itemconfig(PLAYER, image=PLAYERRIGHT)
            canvas.move(PLAYER, configs.PLAYERSPEED,0)
            movingsym.set("right")
        elif bindarg.keysym == "a":
            canvas.itemconfig(PLAYER, image=PLAYERLEFT)
            canvas.move(PLAYER, -configs.PLAYERSPEED,0)
            movingsym.set("left")
        elif bindarg.keysym == "w":
            canvas.move(PLAYER, 0,-configs.PLAYERSPEED)
            # movingsym.set("w")
        elif bindarg.keysym == "s":
            canvas.move(PLAYER, 0,configs.PLAYERSPEED)
            # movingsym.set("s")
def colision_Detection():
    if px < bx + bwidth and px + pwidht >bx and \
    py < by + bheight and py + pheight > by:
        return True
    return False
def checkmouse_Click(event):
    mouse_eventvar.set(True)
    if configs.PLAYERHEALTH > 0:
        if movingsym.get() == "left":
            canvas.itemconfig(PLAYER, image=PLAYERATACKLEFT)
            canvas.after(100, lambda:canvas.itemconfig(PLAYER, image=PLAYERLEFT))
        elif movingsym.get() == "right":
            canvas.itemconfig(PLAYER, image=PLAYERATACKRIGHT)
            canvas.after(100, lambda:canvas.itemconfig(PLAYER, image=PLAYERRIGHT))
def player_Proximity_check():
    pwidht = PLAYERRIGHT.width() + 90
    pheight = PLAYERRIGHT.height() + 90
    bwidth = FROGBOSSIMAGE.width() + 10
    bheight = FROGBOSSIMAGE.height() + 10
    if px < bx + bwidth and px + pwidht >bx and \
    py < by + bheight and py + pheight > by:
        return True
    return False
def boss_Proximity_check():
    pwidht = PLAYERRIGHT.width() + 180
    pheight = PLAYERRIGHT.height() + 180
    bwidth = FROGBOSSIMAGE.width() + 90
    bheight = FROGBOSSIMAGE.height() + 90
    if px < bx + bwidth and px + pwidht >bx and \
    py < by + bheight and py + pheight > by:
        return True
    return False
def player_Atack():
    if player_Proximity_check() and mouse_eventvar.get() and configs.BOSSHEALTH > 0\
    and configs.PLAYERHEALTH > 0:
        damageonnpc(bosshealth)
        mouse_eventvar.set(False)
def enemie_Moving(posenemie, posplayer):
    dx = posenemie[0] - posplayer[0]
    dy = posenemie[1] - posplayer[1]
    distance = math.hypot(dx,dy)
    if distance > 0:
        dx = dx / distance
        dy = dy / distance
    posenemie[0] += dx * 2
    posenemie[1] += dy * 2
    if boss_Proximity_check() and configs.BOSSHEALTH > 0 and configs.PLAYERHEALTH > 0:
        canvas.move(BOSS, dx / 20, dy / 20)
        canvas.itemconfig(BOSS, image=FROGBOSSIMAGE)
    else:
        canvas.itemconfig(BOSS, image=SLEEPBOSS)
while True:
    canvas.bind("<Button-1>", checkmouse_Click)
    playercoords = canvas.coords(PLAYER)
    px = playercoords[0]
    py = playercoords[1]
    bosscoords = canvas.coords(BOSS)
    bx = bosscoords[0]
    by = bosscoords[1]
    player_Proximity_check()
    window.bind('a', moving)
    window.bind('d', moving)
    window.bind('w', moving)
    window.bind('s', moving)

    damageonplayer()
    enemie_Moving(playercoords,bosscoords)
    player_Proximity_check()
    player_Atack()
    window.update()
window.mainloop()

