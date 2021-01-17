class Player:
    def __init__(self, game, window, canvas, aliens, nb_aliens):
        self.game = game
        self.aliens = aliens
        self.nbAliens = nb_aliens
        self.canvas = canvas
        self.window = window
        self.shipX = 200
        self.shipY = 350
        self.laserX = 0
        self.laserY = 0
        self.laserdY = -7
        self.noLaser = True
        self.laser = None
        self.spaceship = self.canvas.create_oval(self.shipX - 10, self.shipY - 10, self.shipX + 10, self.shipY + 10, width=5, outline='black', fill='blue')
        self.alienX = None
        self.alienY = None
        self.isAlienHit = None
        self.isWallHit = False
        self.currentScore = None

        self.set_player_for_aliens()

        self.walls = self.game.walls

    def keypress(self, event):
        key = event.keysym

        if key == 'q' and self.shipX > 20:
            self.shipX -= 10
            self.set_player_for_aliens()
        elif key == 'd' and self.shipX < 580:
            self.shipX += 10
            self.set_player_for_aliens()
        elif key == 'space' and self.noLaser is True:
            self.create_laser()
        self.canvas.coords(self.spaceship, self.shipX - 10, self.shipY - 10, self.shipX + 10, self.shipY + 10)

    def create_laser(self):
        self.laser = self.canvas.create_oval(self.shipX - 3, self.shipY - 3, self.shipX + 3, self.shipY + 3, width=3, outline='black', fill='cyan')
        self.laserX, self.laserY = self.shipX, self.shipY
        self.check_laser()

    def check_laser(self):
        # Constate l'état du laser pour vérifier s'il atteint une cible, qu'il sort de l'écran ou s'il doit continue
        self.canvas.move(self.laser, 0, self.laserdY)
        self.noLaser = False

        self.isAlienHit = False
        self.isWallHit = False
        for i in range(len(self.aliens)):
            self.alienX, self.alienY = self.aliens[i].get_coordinates()
            if abs(self.alienX - self.laserX) <= 12 and abs(self.alienY - self.laserY) <= 12:
                # Le laser est en contact avec un alien

                self.isAlienHit = True
                self.canvas.delete(self.laser)

                self.noLaser = True

                self.game.alien_killed(self.aliens[i])

                break

        for i in range(len(self.walls)):

            if self.walls[i].destroyed is False:
                if abs(self.walls[i].wallX - self.laserX + 10) <= 20 and abs(self.walls[i].wallY - self.laserY - 10) <= 20:
                    # Le mur est détruit
                    self.game.wall_detroyed(self.walls[i])
                    self.canvas.delete(self.laser)
                    self.noLaser = True
                    self.isWallHit = True
                    break

        if self.isAlienHit is False and self.isWallHit is False:
            if self.laserY < 0:
                # Le laser est sorti de l'écran
                self.canvas.delete(self.laser)
                self.noLaser = True
            else:
                # Le laser continue sa trajectoire
                self.laserY = self.canvas.coords(self.laser)[1]
                self.laserX = self.canvas.coords(self.laser)[0]
                self.canvas.after(10, self.check_laser)

    def set_player_for_aliens(self):
        # Setter pour récupérer le player dans l'objet alien
        for i in range(len(self.aliens)):
            self.aliens[i].set_player(self)