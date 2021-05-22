from seega.seega_actions import SeegaAction, SeegaActionType
from seega.seega_state import SeegaState
from core import Player, action
from seega.seega_rules import SeegaRules
import math
from itertools import product
from pprint import pp, pprint
import copy


class AI(Player):

    in_hand = 12
    score = 0
    name= "Groupe2"
    DEPTH=1

    def __init__(self, color):
        super(AI, self).__init__(color)
        self.position = color.value

    def play(self, state, remain_time):
        #print(f"Player {self.position} is playing.")
        #print("time remain is ", remain_time, " seconds")

        if state.phase == 1 :
            return self.best_entry_position_v2(state)
        else: 
            return self.best_action(state)
                
        
    def set_score(self, new_score):
        self.score = new_score


    def update_player_infos(self, infos):
        self.in_hand = infos['in_hand']
        self.score = infos['score']


    def reset_player_informations(self):
        self.in_hand = 12
        self.score = 0

    # Toute la partie 1 se gere ici ;) 
    def best_entry_position_v2(self, state):
        for i in range(4):
            for j in range(4):
                if SeegaRules.is_legal_move(state, self.buildSeegaAction([(i, 0)]), self.position):
                    return self.buildSeegaAction([(i, 0)])
                if SeegaRules.is_legal_move(state, self.buildSeegaAction([(0, j)]), self.position):
                    return self.buildSeegaAction([(0, j)])
                if SeegaRules.is_legal_move(state, self.buildSeegaAction([(i, 4)]), self.position):
                    return self.buildSeegaAction([(i, 4)])
                if SeegaRules.is_legal_move(state, self.buildSeegaAction([(4, j)]), self.position):
                    return self.buildSeegaAction([(4, j)])
        return SeegaRules.random_play(state, self.position)

    # creer une instance de l'objet SeegaAction.
    # il prend en parametre un couple
    # Pourrait etre utilisé dans plein de cas.
    def buildSeegaAction(self, couples):
        return SeegaAction(action_type=SeegaActionType.ADD, to=couples[0])

    # Pour jouer notre meilleur coup quand ce sera notre tour
    def best_action(self, board):
        best_move = None
        best_move_score = 0
        availables_state = []
        moves = SeegaRules.get_player_all_cases_actions(board, self.position)

        # Générer tous les states de ce noeud
        for move in moves:
            newBoard = board
            newBoard, is_the_end = SeegaRules.make_move(newBoard, move, self.position)
            availables_state.append(newBoard)

        best_move = moves[0]
        best_move_score = self.minimax(availables_state[0], float('-inf'), float('inf'), self.DEPTH, self.position)
        i = -1
        for stt in availables_state:
            i += 1
            if i > 1:
                score = self.minimax(stt, float('-inf'), float('inf'), self.DEPTH, self.position)
                if score > best_move_score:
                    best_move = moves[i]
                    best_move_score = score
        return best_move


    # implementation de alpha beta
    def minimax(self, board, alpha, beta, depth, actual_player):

        if depth == 0 or SeegaRules.is_end_game(board):
            return self.evaluate(board)

        if actual_player == self.position:
            moves = SeegaRules.get_player_all_cases_actions(board, self.position)

            newBeta = beta
            for move in moves:
                next_board = board
                next_board, is_the_end = SeegaRules.make_move(next_board, move, self.position)
                newBeta = min(newBeta, self.minimax(next_board, alpha, beta, depth - 1, self.position))  
                if newBeta <= alpha:
                    break
            return newBeta
        else:
            moves = SeegaRules.get_player_all_cases_actions(board, self.position)
            newAlpha = alpha
            for move in moves:
                next_board = board
                next_board, is_the_end = SeegaRules.make_move(next_board, move, self.position)
                newAlpha = max(newAlpha, self.minimax(next_board, alpha, beta, depth - 1, self.position)) 
                if beta <= newAlpha:
                    break
            return newAlpha


    def evaluate(self, board):
        return board.score[self.position] - board.score[self.position * -1]
