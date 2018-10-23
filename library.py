import copy
import numpy as np
import time
import random

MOVES = {
    0: (0, 0),
    1: (0, 1),
    2: (0, 2),
    3: (1, 0),
    4: (1, 1),
    5: (1, 2),
    6: (2, 0),
    7: (2, 1),
    8: (2, 2),
}
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
    def playRandom(self):
        ij = np.where(self.board == 0)
        ij = zip(ij[0], ij[1])
        i, j = random.choice(ij)
        self.play((i,j))
    def reset(self):
        self.board = np.zeros((3,3))
    pass

class MasterTicTacToe:
    def __init__(self, board = np.zeros((3,3)), player = 1):
        self.board = board
        self.sub_boards = [[TicTacToe() for _ in range(3)] for _ in range(3)]
        self.active_sub_board = (1, 1)
        self.player = 1
    def play(self, position):
        if self.sub_boards[self.active_sub_board][position] == 0:
            self.sub_boards[self.active_sub_board][position] = self.player
            self.player = -1 * self.player
            self.active_sub_board = position
        else:
            raise ValueError('Already played there')
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

def who_win(ttt):
    # nX, nO = count(ttt.board)
    # if nX - nO > 1 or nX - nO < 0:
    #     raise ValueError('Impossible Game State')

    row_sums = np.sum(ttt.board, 1)
    col_sums = np.sum(ttt.board, 0)
    dia_sums = np.array([np.trace(ttt.board), np.fliplr(ttt.board).trace()])

    sums = np.hstack([row_sums, col_sums, dia_sums])
    if 3 in sums:
        return 1
    elif -3 in sums:
        return -1
    elif np.sum(np.isin(ttt.board, 0)) == 0:
        return None
    else:
        return 0 #no-win condition

def draw(ttt):
    if np.sum(np.isin(ttt.board, 0)) == 0 and not win(ttt.board):
        return True
   
def win_master(mttt):
    if win(mttt.board):
        return True

def playRandom(ttt):
    ij = np.where(ttt.board == 0)
    ij = zip(ij[0], ij[1])
    i, j = random.choice(ij)
    ttt.play((i,j))

def getNumGames(ttt):
    if(np.sum(np.isin(ttt.board, 0)) == 0) or who_win(ttt):
        return 1
    else:
        count = 0
        ij = np.where(ttt.board == 0)
        for i, j in zip(ij[0], ij[1]):
            new_ttt = copy.deepcopy(ttt)
            new_ttt.play((i, j))
            count += getNumGames(new_ttt)
        return count

# get winning probs before playing
def getWinningStats(ttt):
    wp = who_win(ttt)
    if wp == 1: 
        return np.array([1, 0, 0])
    elif wp == -1:
        return np.array([0, 1, 0])
    elif wp == None:
        return np.array([0, 0, 1])
    else:
        count = np.array([0, 0, 0])
        ij = np.where(ttt.board == 0)
        for i, j in zip(ij[0], ij[1]):
            new_ttt = copy.deepcopy(ttt)
            new_ttt.play((i, j))
            count += getWinningStats(new_ttt)
        return count
    
def count(tictactoe):
    nX = np.sum(np.isin(tictactoe, 1))
    nO = np.sum(np.isin(tictactoe, -1))
    return (nX, nO)

def main():
    t = TicTacToe()
    t.reset()

    t.play((0,0))
    t.play((1,1))
    # t.play((0,1))
    # t.play((1,2))
    # t.play((2,0))
    # t.play((0,2))

    print t.board
    print getNumGames(t)

def game():
    ttt = TicTacToe()
    # ttt.play((0,0))
    while True:
        # print 'Player: {} num_games: {}'.format(ttt.player, getNumGames(ttt))
        print 'Player: {} num_games (player +1 wins, player -1 wins, draw): {}'.format(ttt.player, getWinningStats(ttt))
        ttt.playRandom()
        print ttt.board
        if win(ttt.board):
            print 'Player {} won'.format(-1 * ttt.player)
            break

if __name__ == "__main__":
    main()
    game()