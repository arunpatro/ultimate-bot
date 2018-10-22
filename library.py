import copy
import numpy as np
import time

class TicTacToe:
    def __init__(self, board = np.zeros((3,3)), player = 1):
        self.board = board
        self.player = 1
    def play(self, position):
        if self.board[position] == 0:
            self.board[position] = self.player
            self.player = -1 * self.player
#             return self.board
        else:
            # raise ValueError('Already played there')
            pass
    def reset(self):
        self.board = np.zeros((3,3))
    pass

def win(tictactoe):
    nX, nO = count(tictactoe)
    if nX - nO > 1 or nX - nO < 0:
        raise ValueError('Impossible Game State')
    if np.abs(np.sum(tictactoe[0])) == 3:
        return True
    elif np.abs(np.sum(tictactoe[1])) == 3:
        return True
    elif np.abs(np.sum(tictactoe[2])) == 3:
        return True

    elif np.abs(np.sum(tictactoe[:,0])) == 3:
        return True
    elif np.abs(np.sum(tictactoe[:,1])) == 3:
        return True
    elif np.abs(np.sum(tictactoe[:,2])) == 3:
        return True

    elif np.abs(tictactoe[0,0] + tictactoe[1,1] + tictactoe[2,2]) == 3:
        return True
    
    elif np.abs(tictactoe[0,2] + tictactoe[1,1] + tictactoe[2,0]) == 3:
        return True
    else:
        return False

def getNumGames(ttt):
    if(np.sum(np.isin(ttt.board, 0)) == 0) or win(ttt.board):
        return 1
    else:
        count = 0
        for i in range(3):
            for j in range(3):
                if ttt.board[i][j] == 0:
                    new_ttt = copy.deepcopy(ttt)
                    new_ttt.play((i, j))
                    val = getNumGames(new_ttt)
                    count += val
                    
#         print 'Final Count is ', count
        return count

def count(tictactoe):
    nX = np.sum(np.isin(tictactoe, 1))
    nO = np.sum(np.isin(tictactoe, -1))
    return (nX, nO)

if __name__ == __main__:
    t = TicTacToe()
    t.reset()

    t.play((0,0))
    t.play((1,1))
    # t.play((0,1))
    # t.play((1,2))
    # t.play((2,0))
    # t.play((0,2))

    print getNumGames(t)