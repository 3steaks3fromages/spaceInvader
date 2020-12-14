from tkinter import Label, Tk, Canvas, Button, PhotoImage
from pathlib import Path


class game:
    def __init__(self):
        self.window = Tk()

        self.newGameButton = Button(self.window, text="New Game")
        self.newGameButton.grid(column=2, row=2)

        self.quitButton = Button(self.window, text="Quit Game", command=self.window.destroy)
        self.quitButton.grid(column=2, row=3)

        self.livesLabel = Label(self.window, text="Lives : 3")
        self.livesLabel.grid(column=2, row=1)

        self.scoreLabel = Label(self.window, text="Score : 0")
        self.scoreLabel.grid(column=1, row=1)

        self.canvas = Canvas(self.window, height=400, width=600)
        self.canvas.grid(column=1, row=2, rowspan=2)
        self.imagepath = Path.cwd() / 'image' / 'background.png'
        self.image = PhotoImage(file=str(self.imagepath))
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")

        self.window.title("Space Invader")
        self.window.geometry("675x425")
        self.window.resizable(height=False, width=False)

    def start(self):

        self.window.mainloop()