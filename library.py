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
        self.sub_boards = np.zeros([9, 3, 3])
        self.active_sub_board = 4
        self.player = 1
    def play(self, position):
        if self.sub_boards[self.active_sub_board][position] == 0:
            self.sub_boards[self.active_sub_board][position] = self.player
            
            wp = who_win(TicTacToe(board = self.sub_boards[self.active_sub_board]))
            pos = self.active_sub_board / 3, self.active_sub_board % 3
            if wp == 1:
                self.board[pos] = 1
                self.player = -1 * self.player
                return True, self.active_sub_board, 1
            elif wp == -1:
                self.board[pos] = -1
                self.player = -1 * self.player
                return True, self.active_sub_board, -1
                
            self.player = -1 * self.player
            self.active_sub_board = position[0] * 3 + position[1]
            return False, self.active_sub_board, -1 * self.player
        else:
            # raise ValueError('Already played there')
            pass
    def playRandom(self):
        position = self.active_sub_board / 3, self.active_sub_board % 3
        if not self.board[position] == 0:
            IJ = np.where(self.board == 0)
            IJ = zip(IJ[0], IJ[1])
            II, JJ = random.choice(IJ)
            self.active_sub_board = II * 3 + JJ
        ij = np.where(self.sub_boards[self.active_sub_board] == 0)
        ij = zip(ij[0], ij[1])
        i, j = random.choice(ij)
        self.play((i,j))
    def render(self):
        b = np.vstack([np.hstack([t for t in self.sub_boards[:3]]), np.hstack([t for t in self.sub_boards[3:6]]), np.hstack([t for t in self.sub_boards[6:]])])
        print b
    def reset(self):
        self.board = np.zeros((3,3))
        self.sub_boards = np.zeros([9, 3, 3])
        self.player = 1
    pass

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

def getMasterWinningStats(mttt):
    wp = who_win(mttt)
    if wp == 1: 
        return np.array([1, 0, 0])
    elif wp == -1:
        return np.array([0, 1, 0])
    elif wp == None:
        return np.array([0, 0, 1])
    else:
        count = np.array([0, 0, 0])
        ij = np.where(mttt.board == 0)
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

def mgame():
    mttt = MasterTicTacToe()
    steps = 0
    while steps < 40:
        print 'Player: {}'.format(mttt.player)
        mttt.playRandom()
        mttt.render()
        print mttt.board
        wp = who_win(mttt)
        if wp:
            print 'player', wp, 'wins'
            break
        steps += 1

if __name__ == "__main__":
    main()
    # game()
    mgame()