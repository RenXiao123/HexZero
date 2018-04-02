from numpy import random
from collections import namedtuple
from playInfo import playInfo
import constants
GRID_SIZE=constants.GRID_SIZE
evaluation = namedtuple('evaluation',['eval','best_move_r','best_move_c'])
class easyMCTS:
    def __init__(self):
        pass

    def find_empty(self,pi):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if pi.board[i][j]==0:
                    return [i,j]

    def find_random_empty(self,pi):
        m=random.randint(0,GRID_SIZE)
        n=random.randint(0,GRID_SIZE)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                ii=(i+m)%GRID_SIZE
                jj=(j+n)%GRID_SIZE
                if pi.board[ii][jj]==0:
                    return [ii,jj]
        print('haha')
        return [-1,-1] # this shouldn't happen


    #Returns a very rough evaluation of the current game state
    def monteCarlo(self,pi,breadth,depth):
        if depth==0:
            #finish with a single simulation
            return self.monteCarlo(pi,1,-1)
        mode = pi.mode
        result = 0
        for k in range(breadth):
            pi2=pi.deepcopy()
            pos=self.find_random_empty(pi)
            pi2.update(pos[0],pos[1])
            if pi2.winner !=0:
                result+=pi2.winner
            else:
                result+=self.monteCarlo(pi2,breadth,depth-1)
        #print(result/breadth)
        return result/breadth


    #breadth: number of nodes searched each level
    #depth: number of levels searched before carrying out a simple monte carlo simulation
    def treeSearch(self, pi,alpha,beta, breadth,depth):
        if depth ==0:
            #return evaluation(0,0,0)
            return evaluation(self.monteCarlo(pi,1,1),0,0)
        mode = pi.mode
        result = -mode
        best_result = -mode
        best_move=self.find_empty(pi)
        for k in range(breadth):
            r=random.randint(0, GRID_SIZE)
            c=random.randint(0, GRID_SIZE)
            if pi.board[r][c]==0:
                pi2 = pi.deepcopy()
                pi2.update(r,c)
                if pi2.winner !=0:
                    result=pi2.winner
                else:
                    result=self.treeSearch(pi2,alpha,beta,breadth,depth-1).eval
                if mode==-1:
                    if result<=best_result:
                        best_result=result
                        best_move=[r,c]
                    beta=min(beta,best_result)
                else:
                    if result>=best_result:
                        best_result=result
                        best_move=[r,c]
                    alpha=max(alpha,best_result)
                if beta <= alpha:
                    break
        return evaluation(best_result,best_move[0],best_move[1])

    def move(self,pi):
        return self.treeSearch(pi,-1,1,8,6)
