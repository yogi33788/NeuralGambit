import json
import copy  # use it for deepcopy if needed
import math  # for math.inf
import logging

logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

# Global variables in which you need to store player strategies (this is data structure that'll be used for evaluation)
# Mapping from histories (str) to probability distribution over actions
strategy_dict_x = {}
strategy_dict_o = {}


class History:
    def __init__(self, history=None):
        """
        # self.history : Eg: [0, 4, 2, 5]
            keeps track of sequence of actions played since the beginning of the game.
            Each action is an integer between 0-8 representing the square in which the move will be played as shown
            below.
              ___ ___ ____
             |_0_|_1_|_2_|
             |_3_|_4_|_5_|
             |_6_|_7_|_8_|

        # self.board
            empty squares are represented using '0' and occupied squares are either 'x' or 'o'.
            Eg: ['x', '0', 'x', '0', 'o', 'o', '0', '0', '0']
            for board
              ___ ___ ____
             |_x_|___|_x_|
             |___|_o_|_o_|
             |___|___|___|

        # self.player: 'x' or 'o'
            Player whose turn it is at the current history/board

        :param history: list keeps track of sequence of actions played since the beginning of the game.
        """
        if history is not None:
            self.history = history
            self.board = self.get_board()
        else:
            self.history = []
            self.board = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        self.player = self.current_player()

    def current_player(self):
        """ Player function
        Get player whose turn it is at the current history/board
        :return: 'x' or 'o' or None
        """
        total_num_moves = len(self.history)
        if total_num_moves < 9:
            if total_num_moves % 2 == 0:
                return 'x'
            else:
                return 'o'
        else:
            return None

    def get_board(self):
        """ Play out the current self.history and get the board corresponding to the history in self.board.

        :return: list Eg: ['x', '0', 'x', '0', 'o', 'o', '0', '0', '0']
        """
        board = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        for i in range(len(self.history)):
            if i % 2 == 0:
                board[self.history[i]] = 'x'
            else:
                board[self.history[i]] = 'o'
        return board

    def is_win(self):
    
        # check if the board position is a win for either players
        # Feel free to implement this in anyway if needed
        row = [[0,1,2],[3,4,5],[6,7,8]]
        column = [[0,3,6],[1,4,7],[2,5,8]]
        diagonal = [[0,4,8],[6,4,2]]
        for lines in row,column,diagonal:
            for line in lines:
                if all(self.board[pos] == 'x' for pos in line):
                    return 'x'
                elif all(self.board[pos] == 'o' for pos in line):
                    return 'o'
        return None

    def is_draw(self):
        # check if the board position is a draw
        # Feel free to implement this in anyway if needed
        if self.is_win() == None:
            if '0' not in self.board:
                return True
        return False  

    def get_valid_actions(self):
        # get the empty squares from the board
        # Feel free to implement this in anyway if needed
        val = []
        for i in range(9):
            if self.board[i] == '0':
                val.append(i)
        return val

    def is_terminal_history(self):
        # check if the history is a terminal history
        # Feel free to implement this in anyway if needed
        return self.is_win() is not None or self.is_draw()

    def get_utility_given_terminal_history(self):
        # Feel free to implement this in anyway if needed
        win = self.is_win()
        if win == 'x':
            return 1
        elif win =='o':
            return -1
        else:
            return 0

    def update_history(self, action):
        # In case you need to create a deepcopy and update the history obj to get the next history object.
        # Feel free to implement this in anyway if needed
        return History(self.history + [action])


def backward_induction(history_obj):
    """
    :param history_obj: Histroy class object
    :return: best achievable utility (float) for th current history_obj
    """
    global strategy_dict_x, strategy_dict_o
    # TODO implement
    # (1) Implement backward induction for tictactoe
    # (2) Update the global variables strategy_dict_x or strategy_dict_o which are a mapping from histories to
    # probability distribution over actions.
    # (2a)These are dictionary with keys as string representation of the history list e.g. if the history list of the
    # history_obj is [0, 4, 2, 5], then the key is "0425". Each value is in turn a dictionary with keys as actions 0-8
    # (str "0", "1", ..., "8") and each value of this dictionary is a float (representing the probability of
    # choosing that action). Example: {”0452”: {”0”: 0, ”1”: 0, ”2”: 0, ”3”: 0, ”4”: 0, ”5”: 0, ”6”: 1, ”7”: 0, ”8”:
    # 0}}
    # (2b) Note, the strategy for each history in strategy_dict_x and strategy_dict_o is probability distribution over
    # actions. But since tictactoe is a PIEFG, there always exists an optimal deterministic strategy (SPNE). So your
    # policy will be something like this {"0": 1, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0} where
    # "0" was the one of the best actions for the current player/history.
    if history_obj.is_terminal_history():
        return history_obj.get_utility_given_terminal_history()
    valid_moves = history_obj.get_valid_actions()
    history_key = ''.join(map(str, history_obj.history))

    if history_obj.player == 'x':
        x_utility = -math.inf
        x_move = None
        for action in valid_moves:
            his = history_obj.update_history(action)
            uti_x = backward_induction(his)
            if uti_x > x_utility:
                x_utility = uti_x
                x_move = action
        strategy = {}
        for i in range(9):
            strategy[str(i)] = 0
        strategy[str(x_move)] = 1
        strategy_dict_x[history_key] = strategy
        return x_utility
    elif history_obj.player == 'o':
        o_utility = math.inf
        o_move = None
        for action in valid_moves:
            his = history_obj.update_history(action)
            uti_o = backward_induction(his)
            if uti_o < o_utility:
                o_utility = uti_o
                o_move = action
        strategy = {}
        for i in range(9):
            strategy[str(i)] = 0
        strategy[str(o_move)] = 1
        strategy_dict_o[history_key] = strategy
        return o_utility

    # TODO implement


def solve_tictactoe():
    backward_induction(History())
    with open('./policy_x.json', 'w') as f:
        json.dump(strategy_dict_x, f)
    with open('./policy_o.json', 'w') as f:
        json.dump(strategy_dict_o, f)
    return strategy_dict_x, strategy_dict_o


if __name__ == "__main__":
    logging.info("Start")
    solve_tictactoe()
    logging.info("End")
