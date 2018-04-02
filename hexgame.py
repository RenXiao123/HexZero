from __future__ import print_function
from tkinter import *
import array
from sys import stdout
from collections import namedtuple
from math import *
import constants
from playInfo import playInfo
from MCTS import MCTS

# Introduction to the game-------------------------------------------------------------------------------------------------------------
"""This is a two player Hex Game. In this game the player has to build a bridge from his side to his other side of
the hex paralellogram, players take turn alternatively,the one who builds first wins.A player can place his stone at

any empty place.As soon as an unbroken chain of stones connects two opposite sides of the board, the game ends
declaring the winner of the game. This game was invented by Piet Hein. It is a win or lose game proved by

John Nash an independent inventor of this game.
"""

#Some Implementation and Algorithm Details----------------------------------------------------------------------------------------------
"""The game is implemented as Union Find and Union Join Algorithm.

1. Intitally every node is the parent of itself.
2. A Component will have one parent . Priority of deciding the parent is done by following steps:

a. If the node at top or bottom layer of the board is not available as a parent , choose any parent that is available.
b. But if the node at top or bottom layer is available choose it , if more than one of them are available choose any.

3. In case when greater than equal to one parent is available from top layer and simultaneously from bottom layer,
bridge is formed and game is over.

"""




GRID_SIZE=constants.GRID_SIZE
IMG_SIZE = 35
XPAD = 40
YPAD = 40
WIN_HEIGHT = 2 * YPAD + GRID_SIZE * IMG_SIZE + 100
WIN_WIDTH = 2 * XPAD + (3 * GRID_SIZE - 1) * IMG_SIZE






class gameGrid():
    def __init__(self, frame):
        self.frame = frame
        self.white = PhotoImage(file="./media/white35.gif")
        self.red = PhotoImage(file="./media/red35.gif")
        self.blue = PhotoImage(file="./media/blue35.gif")
        self.drawGrid()
        self.playInfo = playInfo()

    def drawGrid(self):
        for yi in range(0, GRID_SIZE):
            xi = XPAD + yi * IMG_SIZE
            for i in range(0, GRID_SIZE):
                l = Label(self.frame, image=self.white)
                l.pack()
                l.image = self.white
                l.place(anchor=NW, x=xi, y=YPAD + yi * IMG_SIZE)
                l.bind('<Button-1>', lambda e: self.on_click(e))
                xi += 2 * IMG_SIZE

    def getCoordinates(self, widget):
        row = (widget.winfo_y() - YPAD) // IMG_SIZE
        col = (widget.winfo_x() - XPAD - row * IMG_SIZE) // (2 * IMG_SIZE)
        return row , col

    def toggleColor(self, widget):
        if self.playInfo.mode == 1:
            widget.config(image=self.red)
            widget.image = self.red
        else:
            widget.config(image=self.blue)
            widget.image = self.blue

    def display_winner(self, winner_label):
        winner_window = Tk()
        winner_window.wm_title("Winner")
        frame = Frame(winner_window, width=40, height=40)
        frame.pack()
        label = Label(frame,text = "Winner is Player : " + winner_label)
        label.pack()
        label.place(anchor=NW, x = 20, y = 20)

    def on_click(self, event):
        if event.widget.image != self.white:
            return
        self.toggleColor(event.widget)
        a, b = self.getCoordinates(event.widget)
        self.playInfo.update(a,b)
        #self.playInfo.printBoard()
        if self.playInfo.winner!=0:
            winner_label = ""
            if self.playInfo.winner == -1:
                winner_label = " -1 ( Blue ) "
            else:
                winner_label += " 1 ( Red ) "
            #self.display_winner(winner_label)
            print(winner_label)

        else:

            AI= MCTS(a,b,-self.playInfo.mode,self.playInfo.board)
            e=AI.move()
            l = Label(self.frame, image=self.red)
            l.pack()
            l.image = self.red
            l.place(anchor=NW, x=XPAD + e[0] * IMG_SIZE + 2* e[1]*IMG_SIZE, y=YPAD + e[0] * IMG_SIZE)
            print(e)
            self.playInfo.update(e[0],e[1])
            if self.playInfo.winner!=0:
                winner_label = ""
                if self.playInfo.winner == -1:
                    winner_label = " -1 ( Blue ) "
                else:
                    winner_label += " 1 ( Red ) "
                self.display_winner(winner_label)
                print(winner_label)

class gameWindow:
    def __init__(self, window):
        self.frame = Frame(window, width=WIN_WIDTH, height=WIN_HEIGHT)
        self.frame.pack()
        self.gameGrid = gameGrid(self.frame)


def main():
    window = Tk()
    window.wm_title("Hex Game")
    gameWindow(window)
    window.mainloop()


main()
