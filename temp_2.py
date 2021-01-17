#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 13:38:49 2020

@author: jordanbrassac
"""

from tkinter import Tk, PhotoImage, Canvas, Button, Label, StringVar, Entry

x0 = 100
y0 = 100
x1 = 200
y1 = 300
dx = 1
dy = 0
k = 0
x = x0
y = y0


def alien_movement():
    global dx, x, k, y, dy, x0, y0

    if x + dx > 500:
        dx = -1
    elif x - dx < 0:
        dx = 1
        dy = 5
    canevas.move(alien, dx, dy)
    dy = 0
    fenetre.after(1, alien_movement)
    x = canevas.coords(alien)[0]
    y = canevas.coords(alien)[1]
    print(x, x1, y, y1)
    if y <= y1 and x <= x1 + 5 and x >= x1 + 5:
        canevas.delete(vaisseau)


vlaser = True


def vessel(event):
    global x1, y1, vlaser

    touche = event.keysym
    if touche == 'q':
        x1 -= 20
    elif touche == 'd':
        x1 += 20
    elif touche == 'space' and vlaser == True:
        laser_creation()
    canevas.coords(vaisseau, x1 - 10, y1 - 10, x1 + 10, y1 + 10)


def laser_creation():
    global x2, y2, laser
    laser = canevas.create_oval(x1 - 3, y1 - 3, x1 + 3, y1 + 3, width=5, outline='black', fill='white')
    y2 = y1
    x2 = x1
    shot()


def shot():
    global y2, dy2, x2, alien, vlaser
    dy2 = -1
    canevas.move(laser, 0, dy2)
    vlaser = False
    print(x, y, x2, y2)
    if (abs(y - y2) <= 10 and abs(x - x2) <= 10):
        print(True)
        canevas.delete(laser)
        canevas.delete(alien)
        vlaser = True
        alien = canevas.create_oval(x0 - 10, y0 - 10, x0 + 10, y0 + 10, width=5, outline='black', fill='green')
    elif y2 < 0:
        canevas.delete(laser)
        vlaser = True
    else:

        y2 = canevas.coords(laser)[1]
        x2 = canevas.coords(laser)[0]
        canevas.after(10, shot)


fenetre = Tk()
fenetre.title("Space invader")

canevas = Canvas(fenetre, width=500, height=400)
alien = canevas.create_oval(x0 - 10, y0 - 10, x0 + 10, y0 + 10, width=5, outline='black', fill='green')
vaisseau = canevas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, width=5, outline='black', fill='blue')

alien_movement()

canevas.bind('<Key>', vessel)

canevas.focus_set()
canevas.pack(padx=5, pady=5)

boutonquitter = Button(fenetre, text='Quitter', command=fenetre.destroy)
boutonquitter.pack()

texteLabel1 = Label(fenetre, bg='white', padx=10, pady=10)

fenetre.mainloop()