import constants
import time

GRID_SIZE=constants.GRID_SIZE

# Game Variables
dx = [0, 1, 0, -1, -1, 1]
dy = [-1, -1, 1, 1, 0, 0]

class playInfo():

    def __init__(self):
        self.board = [[0 for r in range(GRID_SIZE)] for c in \
                                                        range(GRID_SIZE)]

        #-1: blue goes, 1: red goes
        self.mode = -1
        self.winner = 0

    def inRange(self, r,c):
        if r<0 or r>=GRID_SIZE or c<0 or c>=GRID_SIZE:
            return False
        return True

    def update(self, r,c):

        if self.board[r][c] != 0:
            return False
        self.board[r][c] = self.mode
        self.checkWinning(self.mode) #updates the winner property
        self.mode = - self.mode
        return True

    def checkWinning(self, player):

        #start = time.time()

        connection = [[0 for r in range(GRID_SIZE)] for c in \
                                                        range(GRID_SIZE)]
        flag = True
        if player == -1:
            for j in range(GRID_SIZE):
                if self.board[0][j]==-1:
                    connection[0][j]=-2

            while flag:
                flag=False
                for i in range(GRID_SIZE):
                    for j in range(GRID_SIZE):
                        if connection[i][j]==-2:
                            for k in range(6):
                                if self.inRange(i+dx[k],j+dy[k]) and self.board[i+dx[k]][j+dy[k]]==-1 and connection[i+dx[k]][j+dy[k]]==0:
                                    if i+dx[k]==GRID_SIZE-1:
                                        self.winner=-1
                                        return
                                    connection[i+dx[k]][j+dy[k]]=-2
                                    flag=True
                            connection[i][j]=-1
        elif player==1:
            for i in range(GRID_SIZE):
                if self.board[i][0]==1:
                    connection[i][0]=2

            while flag:
                flag=False
                for i in range(GRID_SIZE):
                    for j in range(GRID_SIZE):
                        if connection[i][j]==2:
                            for k in range(6):
                                if self.inRange(i+dx[k],j+dy[k]) and self.board[i+dx[k]][j+dy[k]]==1 and connection[i+dx[k]][j+dy[k]]==0:
                                    if j+dy[k]==GRID_SIZE-1:
                                        self.winner=1
                                        return
                                    connection[i+dx[k]][j+dy[k]]=2
                                    flag=True
                            connection[i][j]=1

        #end = time.time()
        #print(end - start)
        return



    def printBoard(self):
        n = GRID_SIZE
        i,j = 0,0
        print ("Current Board Display: ",end="\n")
        for i in range(1,n+1):
            for k in range(1,i):
                stdout.write(" ")
                for j in range(1,n+1):
                    print(self.board[i][j],end=" ")
                stdout.write("\n")
