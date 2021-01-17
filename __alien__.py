import random as rd


class Alien:
    def __init__(self, game, window, canvas, i):

        self.canvas = canvas
        self.window = window
        self.i = i
        self.column = i // 6
        self.x = 20 + 100*(i % 6)
        self.y = 100 + 50*self.column
        self.dx = 0.1
        self.dy = 0
        self.alien = canvas.create_oval(self.x - 10, self.y - 10, self.x + 10, self.y + 10, width=5, outline='black', fill='green')
        self.game = game
        self.laseralienX = 0
        self.laseralienY = 0
        self.laseraliendY = 2
        self.noLaseralien = True
        self.laseralien = None

        self.player = None

        self.shipX = 200
        self.shipY = 350

        self.walls = self.game.walls

        #Le boolean suivant permet de s'assurer que l'alien ne descendra qu'une fois
        # à chaque fois qu'il atteint la gauche de l'écran
        self.descend_left = True

        self.alien_movement()

        self.isShipHit = False
        self.isWallHit = False

    #Permet de créer un laser
    def create_laser_alien(self):
        self.laseralien = self.canvas.create_oval(self.x - 3, self.y - 3, self.x + 3, self.y + 3, width=3, outline='black', fill='red')
        self.laseralienX, self.laseralienY = self.x, self.y
        self.check_laser_alien(self.canvas, self.player)

    #Fonction pour déplacer l'alien et vérifier s'il atteint le joueur
    def alien_movement(self):
        self.dy = 0
        if self.canvas.coords(self.alien):
            if self.x + self.dx > 570:
                self.dx = -0.1
                self.dy -= -25
                self.descend_left = True
            elif self.x - self.dx < 5:
                self.dx = 0.1
                if self.descend_left is True:
                    self.dy -= -25
                    self.descend_left = False
            if self.y > 315:
                # Le joueur perd une vie et l'alien disparait
                self.game.loose_life(self)
                self.canvas.delete(self.alien)
                del self
                return
            random = rd.randint(1, 1000)
            if random == 1 and self.noLaseralien is True:
                self.create_laser_alien()
                self.noLaseralien = False
            self.canvas.move(self.alien, self.dx, self.dy)
            self.x = self.canvas.coords(self.alien)[0]
            self.y = self.canvas.coords(self.alien)[1]
            self.window.after(1, self.alien_movement)

    #Getter pour récupérer les coordonnées de l'alien
    def get_coordinates(self):
        return self.x, self.y

    #Setter pour recevoir les coordonnées du joueur
    def set_player(self, player):
        self.player = player

    #Permet de déplacer le laser et vérifier s'il atteint un obstacle, le joueur ou le bas de l'écran
    def check_laser_alien(self, canvas, player):
        try:
            self.shipX = player.shipX
            self.shipY = player.shipY
        except AttributeError:
            #Pour éviter des erreurs quand la partie se relance
            self.shipX = 0
            self.shipY = 0

        self.laseralien = self.laseralien
        self.laseralienX = self.laseralienX
        self.laseralienY = self.laseralienY
        self.laseraliendY = self.laseraliendY

        self.canvas.move(self.laseralien, 0, self.laseraliendY)
        self.noLaseralien = False
        self.isShipHit = False
        self.isWallHit = False

        if abs(self.shipX - self.laseralienX) <= 12 and abs(self.shipY - self.laseralienY) <= 12:
            # Le laser est en contact avec un alien

            self.isShipHit = True
            self.canvas.delete(self.laseralien)

            self.noLaseralien = True

            self.game.loose_life()

        for i in range(len(self.walls)):

            if self.walls[i].destroyed is False:
                if abs(self.walls[i].wallX - self.laseralienX +10) <= 20 and abs(self.walls[i].wallY - self.laseralienY -10) <= 20:
                    #Le mur est détruit
                    self.game.wall_detroyed(self.walls[i])
                    self.canvas.delete(self.laseralien)
                    self.noLaseralien = True
                    self.isWallHit = True
                    break

        if self.isShipHit is False and self.isWallHit is False:
            if self.laseralienY > 425:
                # Le laser est sorti de l'écran
                self.canvas.delete(self.laseralien)
                self.noLaseralien = True


            else:
                # Le laser continue sa trajectoire
                try:
                    self.laseralienY = canvas.coords(self.laseralien)[1]
                    self.laseralienX = canvas.coords(self.laseralien)[0]
                    self.canvas.after(10, self.check_laser_inter)
                except IndexError:
                    return

    def check_laser_inter(self):
        self.check_laser_alien(self.canvas, self.player)
