from tkinter import Label, Button, PhotoImage, StringVar, Tk, Canvas
from __alien__ import *
from pathlib import Path
from __player__ import *
from __wall__ import *


class Game:
    def __init__(self):
        self.window = Tk()
        self.window.title("Space Invader")

        self.newGameButton = Button(self.window, text="New Game", command=self.start)
        self.newGameButton.grid(column=2, row=2)

        self.quitButton = Button(self.window, text="Quit Game", command=self.window.destroy)
        self.quitButton.grid(column=2, row=3)

        self.livesTxt = StringVar()
        self.livesInt = 3
        self.livesTxt.set("Lives : 3")
        self.livesLabel = Label(self.window, textvariable=self.livesTxt)
        self.livesLabel.grid(column=2, row=1)

        self.scoreTxt = StringVar()
        self.scoreInt = 0
        self.add_score(0)
        self.scoreLabel = Label(self.window, textvariable=self.scoreTxt)
        self.scoreLabel.grid(column=1, row=1)

        self.canvas = Canvas(self.window, height=400, width=600)
        self.canvas.focus_set()

        self.imagepath = Path.cwd() / 'image' / 'background.png'
        self.image = PhotoImage(file=str(self.imagepath))
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")
        self.canvas.grid(column=1, row=2, rowspan=2)

        self.window.geometry("675x425")
        self.window.resizable(height=False, width=False)

        self.nbAliens = None
        self.aliens = None
        self.player = None

        self.firstGame = True

        self.wallX_list = [100, 120, 140, 100, 120, 140, 200, 220, 240, 200, 220, 240, 300, 320, 340, 300, 320, 340,
                           400, 420, 440, 400, 420, 440, 500, 520, 540, 500, 520, 540]
        self.wallY_list = [300, 300, 300, 320, 320, 320, 300, 300, 300, 320, 320, 320, 300, 300, 300, 320, 320, 320,
                           300, 300, 300, 320, 320, 320, 300, 300, 300, 320, 320, 320]
        self.walls = []
        self.create_walls()

    #Cette fonction permet de lancer une nouvelle partie
    def start(self):

        if self.firstGame is False:
            self.regenerate_walls()
            for i in range(len(self.aliens)):
                self.canvas.delete(self.aliens[i].alien)
            try:
                self.canvas.delete(self.player.spaceship)
            except AttributeError:
                pass

        self.nbAliens = 3
        self.aliens = []

        for i in range(self.nbAliens):
            self.aliens.append(Alien(self, self.window, self.canvas, i))

        self.scoreTxt.set("Score : 0")
        self.scoreInt = 0
        self.livesTxt.set("Lives : 3")
        self.livesInt = 3

        self.player = Player(self, self.window, self.canvas, self.aliens, self.nbAliens)
        self.canvas.bind('<Key>', self.player.keypress)

        # Setter pour récupérer le player dans l'objet alien
        for i in range(self.nbAliens):
            self.aliens[i].set_player(self.player)

        if self.firstGame is True:

            self.firstGame = False

            self.window.mainloop()

    #Cette fonction permet de passer au niveau suivant quand tous les aliens sont éliminés
    def level_up(self):
        self.regenerate_walls()
        self.nbAliens += 2
        self.aliens = []

        for i in range(self.nbAliens):
            self.aliens.append(Alien(self, self.window, self.canvas, i))

        self.canvas.delete(self.player.spaceship)
        self.player = Player(self, self.window, self.canvas, self.aliens, self.nbAliens)
        self.canvas.bind('<Key>', self.player.keypress)

    #Permet d'ajouter du score au joueur
    def add_score(self, score):
        self.scoreInt += score
        self.scoreTxt.set("Score : {}".format(self.scoreInt))

    #Permet de supprimer un alien du jeu quand il est touché ou qu'il atteint le joueur
    def alien_killed(self, alien_obj):
        self.add_score(10)

        self.canvas.delete(alien_obj.alien)
        self.aliens.remove(alien_obj)

        if len(self.aliens) == 0:
            self.level_up()

    #On utilise alien_obj=None dans le cas où la perte d'une vie est causée par un laser.
    #Dans ce cas l'alien ne disparait pas
    def loose_life(self, alien_obj=None):
        if self.livesInt > 0:
            self.livesInt -= 1
            self.livesTxt.set("Lives : {}".format(self.livesInt))
        if alien_obj is not None:
            self.aliens.remove(alien_obj)
        if self.livesInt == 0:
            #Game Over
            self.livesTxt.set("Game Over")
            for i in range(len(self.aliens)):
                if self.aliens[i].laseralien is not None:
                    self.canvas.delete(self.aliens[i].laseralien)
                self.canvas.delete(self.aliens[i].alien)
            self.canvas.delete(self.player.spaceship)
            self.aliens = []
            self.player = None
        elif len(self.aliens) == 0:
            self.level_up()

    #Régénère les obstacles
    def regenerate_walls(self):
        for i in range(len(self.wallX_list)):
            self.walls[i].destroyed = False
            self.canvas.itemconfigure(self.walls[i].wallSquare, state='normal')

    #Crée les obstacles au lancement du jeu
    def create_walls(self):
        for i in range(len(self.wallX_list)):
            self.walls.append(Wall(self, self.wallX_list[i], self.wallY_list[i], self.canvas))

    #Permet de détruire un mur touché par un laser
    def wall_detroyed(self, wall):
        for i in range(len(self.walls)):
            if self.walls[i] == wall:
                self.walls[i].destroyed = True
                self.canvas.itemconfigure(self.walls[i].wallSquare, state='hidden')
