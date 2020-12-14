#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 13:38:49 2020

@author: jordanbrassac
"""

from tkinter  import Tk, PhotoImage, Canvas, Button,Label, StringVar,Entry

dx=5
dy=0

def alien_movement():
    global dx,x
    
    
    if x+dx>500:
        dx=-5 
    elif x-dx<0:
        dx=5
        
    canevas.move(alien,dx,dy)
    fenetre.after(20,alien_movement)
    x=canevas.coords(alien)[0]

def vessel(event):
    global x1,y1
    touche=event.keysym
    if touche=='q':
        x1-=20
    elif touche=='d':
        x1+=20
    elif touche=='space':
        laser_creation()
    
    canevas.coords(vaisseau,x1-10,y1-10,x1+10,y1+10)
    
 
def laser_creation():
    global x2,y2,laser
    
    laser=canevas.create_oval(x1-3,y1-3,x1+3,y1+3,width=5,outline='black',fill='white')
    shot()
    



def shot():
    global  x2,dy2
    x2=x1
    dy2=-5
    canevas.move(laser,0,dy2)
    if x2+dy2>0:
        laser.delete
    canevas.after(20,shot)
    x2=canevas.coords(vaisseau)[0]
    
    

fenetre=Tk()
fenetre.title("Space invader")

x=0
y=100
x1=200
y1=300

canevas=Canvas(fenetre,width=500,height=400)
alien=canevas.create_oval(x-10,y-10,x+10,y+10,width=5,outline='black',fill='green')
vaisseau=canevas.create_oval(x1-10,y1-10,x1+10,y1+10,width=5,outline='black',fill='blue')

alien_movement()
canevas.bind('<Key>',vessel)
canevas.focus_set()
canevas.pack(padx=5,pady=5)

boutonquitter=Button(fenetre,text='Quitter',command=fenetre.destroy)
boutonquitter.pack()

texteLabel1 = Label(fenetre,bg='white', padx=10 , pady=10 )

fenetre.mainloop()