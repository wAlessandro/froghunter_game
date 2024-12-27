
from tkinter import *
from sprites import SPRITE
import configs
from time import sleep
import math
#WINDOW
class Main(Tk):
    def __init__(self):
        super().__init__()

        self.title("FrogHunter")
        self.geometry(f"{configs.SCREENWIDHT}x{configs.SCREENHEIGHT}")
        self.resizable(False,False)
        self.config(bg="black")
        #IMAGES
        self.BACKGROUNDIMAGE = PhotoImage(file=SPRITE["lakebackground"])
        self.PLAYERRIGHT = PhotoImage(file=SPRITE["playerright"])
        self.PLAYERLEFT = PhotoImage(file=SPRITE["playerleft"])
        self.PLAYERATACKLEFT = PhotoImage(file=SPRITE["playeratackleft"])
        self.PLAYERATACKRIGHT = PhotoImage(file=SPRITE["playeratackright"])
        self.HEARTICON = PhotoImage(file=SPRITE["hearticon"])
        self.DAMAGEICON = PhotoImage(file=SPRITE["damageicon"])
        self.BOSSESICONS = [SPRITE["frogbossicon"],]
        self.FROGBOSSICON = PhotoImage(file=self.BOSSESICONS[0])
        self.FROGBOSSIMAGE = PhotoImage(file=SPRITE["frogboss"])
        self.SLEEPBOSS = PhotoImage(file=SPRITE["sleepingfrogboss"])
        #INTERFACE
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,weight=1)
        self.player_status = Frame(self,width=800,)
        self.player_status.grid(
            row=2,
            column=0,
            ipady=0,
            sticky="sw"
            )
        self.heart = [
            i for i in range(configs.PLAYERHEALTH)
            ]
        for column in range(configs.PLAYERHEALTH):
            self.heart[column] = Label(
                self.player_status,
                  image=self.HEARTICON,
                  name=str(column),
                  bg="black",
                  )
            self.heart[column].grid(row=0,column=column)
        self.playerat_ackicon = Label(
            self.player_status,
            bg="black",
            image=self.DAMAGEICON
            )
        self.playerat_ackicon.grid(
            row=0,
            column=configs.PLAYERHEALTH+1,
            sticky="e",
            )
        self.player_atacklabel = Label(
                                        self.player_status,
                                        text=configs.PLAYERDAMAGE,
                                        fg="red",
                                        font=("Arial Black",10),bg="black"
            )
        self.player_atacklabel.grid(
                                    row=0,
                                    column=configs.PLAYERHEALTH+1,
                                    sticky="nw",
            )
        self.canvas = Canvas(
                            self,
                            width=configs.SCREENWIDHT-80,
                            height=configs.SCREENHEIGHT-50,
                            bg="black",borderwidth=5,
                            highlightthickness=0
            )
        self.canvas.grid(
                        row=1,
                        column=0,
                        sticky="nswe",
                        pady=0
                        )
        self.bosshealth = Label(
                                self,
                                text=configs.BOSSHEALTH,
                                bg="#df0808",
                                width=configs.BOSSHEALTH,
                                height=1,
                                font=("Arial Black",10)
            )
        self.bosshealth.grid(
                            row=1,
                            column=0,
                            sticky="n"
                            )
        self.BACKGROUND = self.canvas.create_image(
                                                    450,
                                                    290,
                                                    image=self.BACKGROUNDIMAGE
                                                    )
        #GAME
        self.PLAYER = self.canvas.create_image(
                                                20,
                                                20,
                                                image=self.PLAYERRIGHT
                                                )
        self.pwidht = self.PLAYERRIGHT.width() + 40
        self.pheight = self.PLAYERRIGHT.height() + 40
        self.BOSS = self.canvas.create_image(
                                            580,
                                            270,
                                            image=self.FROGBOSSIMAGE
                                            )
        self.bwidth = self.FROGBOSSIMAGE.width() - 40
        self.bheight = self.FROGBOSSIMAGE.height() - 40
        #FUCTIONS
        self.mouse_eventvar = BooleanVar()
        self.mouse_eventvar.set(False)
        self.movingsym = StringVar()
        while True:
            self.canvas.bind("<Button-1>", self.checkMouseClick)
            playercoords = self.canvas.coords(self.PLAYER)
            self.px = playercoords[0]
            self.py = playercoords[1]
            bosscoords = self.canvas.coords(self.BOSS)
            self.bx = bosscoords[0]
            self.by = bosscoords[1]
            self.playerProximityCheck()
            self.bind('a', self.playerMoving)
            self.bind('d', self.playerMoving)
            self.bind('w', self.playerMoving)
            self.bind('s', self.playerMoving)
            self.damageOnPlayer()
            self.enemieMoving(playercoords,bosscoords)
            self.playerProximityCheck()
            self.playerAtack()
            self.update()
    def damageOnNPC(self,npchealthbar):
        if (configs.BOSSHEALTH > 0):
            configs.BOSSHEALTH -= configs.PLAYERDAMAGE
            npchealthbar.configure(text=configs.BOSSHEALTH, width=configs.BOSSHEALTH)
            sleep(0.05)
    def damageOnPlayer(self):
        if (configs.BOSSHEALTH > 0 
            and self.colisionDetection()
            and configs.PLAYERHEALTH > 0):
            def damage():
                configs.PLAYERHEALTH -= configs.BOSSDAMAGE
                self.heart[configs.PLAYERHEALTH].destroy()
            self.canvas.after(100, damage())
            return True
        else:
            return False
    def playerMoving(self,bindarg=None):
        if (configs.PLAYERHEALTH > 0):
            if (bindarg.keysym == "d"):
                self.canvas.itemconfig(self.PLAYER, image=self.PLAYERRIGHT)
                self.canvas.move(self.PLAYER, configs.PLAYERSPEED,0)
                self.movingsym.set("right")
            elif (bindarg.keysym == "a"):
                self.canvas.itemconfig(self.PLAYER, image=self.PLAYERLEFT)
                self.canvas.move(self.PLAYER, -configs.PLAYERSPEED,0)
                self.movingsym.set("left")
            elif (bindarg.keysym == "w"):
                self.canvas.move(self.PLAYER, 0,-configs.PLAYERSPEED)
            elif (bindarg.keysym == "s"):
                self.canvas.move(self.PLAYER, 0,configs.PLAYERSPEED)
    def colisionDetection(self,):
        if (self.px < self.bx + self.bwidth 
            and self.px + self.pwidht >self.bx
            and self.py < self.by + self.bheight 
            and self.py + self.pheight > self.by):
            return True
        return False
    def checkMouseClick(self, event):
        self.mouse_eventvar.set(True)
        if (configs.PLAYERHEALTH > 0):
            if (self.movingsym.get() == "left"):
                self.canvas.itemconfig(self.PLAYER, image=self.PLAYERATACKLEFT)
                self.canvas.after(100, 
                                  lambda: self.canvas.itemconfig(
                                        self.PLAYER,
                                        image=self.PLAYERLEFT)
                                  )
            elif (self.movingsym.get() == "right"):
                self.canvas.itemconfig(self.PLAYER, image=self.PLAYERATACKRIGHT)
                self.canvas.after(
                    100,
                    lambda:self.canvas.itemconfig(
                        self.PLAYER,
                          image=self.PLAYERRIGHT)
                          )
    def playerProximityCheck(self):
        pwidht = self.PLAYERRIGHT.width() + 90
        pheight = self.PLAYERRIGHT.height() + 90
        bwidth = self.FROGBOSSIMAGE.width() + 10
        bheight = self.FROGBOSSIMAGE.height() + 10
        if (self.px < self.bx + bwidth
                and self.px + pwidht >self.bx 
                and self.py < self.by + bheight 
                and self.py + pheight > self.by):
            return True
        return False
    def bossProximityCheck(self):
        pwidht = self.PLAYERRIGHT.width() + 180
        pheight = self.PLAYERRIGHT.height() + 180
        bwidth = self.FROGBOSSIMAGE.width() + 90
        bheight = self.FROGBOSSIMAGE.height() + 90
        if (self.px < self.bx + bwidth 
                and self.px + pwidht >self.bx
                and self.py < self.by + bheight 
                and self.py + pheight > self.by):
            return True
        return False
    def playerAtack(self):
        if (self.playerProximityCheck()
                and self.mouse_eventvar.get()
                and configs.BOSSHEALTH > 0\
                and configs.PLAYERHEALTH > 0):
            self.damageOnNPC(self.bosshealth)
            self.mouse_eventvar.set(False)
    def enemieMoving(
            self,
            posenemie,
            posplayer):
        dx = posenemie[0] - posplayer[0]
        dy = posenemie[1] - posplayer[1]
        distance = math.hypot(dx,dy)
        if distance > 0:
            dx = dx / distance
            dy = dy / distance
        posenemie[0] += dx * 2
        posenemie[1] += dy * 2
        if (self.bossProximityCheck()
        and configs.BOSSHEALTH > 0
        and configs.PLAYERHEALTH > 0):
            self.canvas.move(self.BOSS, dx / 20, dy / 20)
            self.canvas.itemconfig(self.BOSS, image=self.FROGBOSSIMAGE)
        else:
            self.canvas.itemconfig(self.BOSS, image=self.SLEEPBOSS)
if __name__ == "__main__":
    window = Main()
    window.mainloop()

