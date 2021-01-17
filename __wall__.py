class Wall:
    def __init__(self, game, wallX, wallY, canvas):
        self.destroyed = False
        self.wallX = wallX-20;
        self.wallY = wallY;
        self.canvas = canvas;
        self.wallSquare = canvas.create_rectangle(self.wallX, self.wallY, self.wallX+20, self.wallY-20, outline="#000", fill="#808080")
        self.game = game;