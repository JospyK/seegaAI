"""
Created on 26 oct. 16:01 2020

@author: HaroldKS
"""

from seega.seega_actions import SeegaAction, SeegaActionType
from seega.seega_state import SeegaState
from core import Player
from seega.seega_rules import SeegaRules
import math
from itertools import product
from pprint import pprint


class AI(Player):

    in_hand = 12
    score = 0
    name= "Groupe2"

    def __init__(self, color):
        super(AI, self).__init__(color)
        self.position = color.value

    def play(self, state, remain_time):
        #print(f"Player {self.position} is playing.")
        #print("time remain is ", remain_time, " seconds")

        if state.phase == 1 :
            return self.best_entry_position(state)
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


    def best_entry_position(self, state):
        add = SeegaRules.random_play(state, self.position)
        if state._latest_player == self.position:
            my_previous_postion = state._latest_move.get('action').get('to')
            possible_positions = self.neighbours(state, my_previous_postion)

            if possible_positions:
                #  prioriser les bords du tableau 
                add = SeegaAction(action_type=SeegaActionType.ADD, to=possible_positions[0])
            else:
                # sinon prioriser les bords du tableau 
                add = SeegaRules.random_play(state, self.position)
            
        else:
            # it's muy turn to play. Nous allons chercher a serrer les cotés (de preference la ou a deja le plus de pion mais ce n'est obligatoire)
            # sinon prioriser les bords du tableau 
            add = SeegaRules.random_play(state, self.position) # a supprimer
            pass

        return add


    def neighbours(self, state, t):
        ranges = [(x-1, x, x+1) for x in t]
        result = list(product(*ranges))
        result.pop(len(result) // 2)
        maList=[]
        for x in result:
            if not (x[0] < 0 or x[1] < 0) and x in state.get_board().get_all_empty_cells_without_center() : 
                maList.append(x)
        return maList

    # sort les places disponibles sur les bords du tableau || prioriser les bords du tableau
    def check_edges_first(self, state, t):
        pass


    def best_action(self, state):
        actions = SeegaRules.get_player_all_cases_actions(state, self.position)
        # pprint(actions)
        move = actions[0]
        evaluation = 0
        move, evaluation = self.minimax(state, 20, -math.inf, math.inf, True)
        return move


    def minimax(self, board, depth, alpha, beta, maximizing_player):
        
        if depth == 0 or SeegaRules.is_end_game(board):
            return None, self.evaluate(board)

        children = SeegaRules.get_player_all_cases_actions(board, self.position)        
        best_move = children[0]
        
        if maximizing_player:
            
            max_eval = -math.inf        
            for child in children:
                board_copy = board
                board_copy, is_the_end = SeegaRules.make_move(board_copy, child, self.position)
                move = child
                current_eval = 0
                move, current_eval = self.minimax(board_copy, depth - 1, alpha, beta, False)
                if current_eval > max_eval:
                    max_eval = current_eval
                    best_move = child
                alpha = max(alpha, current_eval)
                if beta <= alpha:
                    break
            return best_move, max_eval

        else:
            min_eval = math.inf
            for child in children:
                board_copy = board
                board_copy, is_the_end = SeegaRules.make_move(board_copy, child, self.position)
                move = child
                current_eval = 0
                move, current_eval = self.minimax(board_copy, depth - 1, alpha, beta, True)
                if current_eval < min_eval:
                    min_eval = current_eval
                    best_move = child
                beta = min(beta, current_eval)
                if beta <= alpha:
                    break
            return best_move, min_eval

    def evaluate(self, board):

        #Kt = ((N ∗ N − 1)/2) − Mt(P1)
        #return 24 - board.score[self.position]

        import random
        return random.randrange(10)

        
        # return  board.score[self.position] - board.score[self.position * -1]


