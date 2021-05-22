"""
Created on 26 oct. 16:01 2020

@author: HaroldKS
"""

from seega.seega_actions import SeegaAction, SeegaActionType
from seega.seega_state import SeegaState
from core import Player, action
from seega.seega_rules import SeegaRules
import math
from itertools import product
from pprint import pp, pprint


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

    # def best_entry_position(self, state):
    #     add = SeegaRules.random_play(state, self.position)
    #     if state._latest_player == self.position:
    #         # pprint(self.place_near_edge(state))
    #         my_previous_postion = state._latest_move.get('action').get('to')
    #         possible_positions = self.neighbours(state, my_previous_postion)
    #         if possible_positions:
    #             #  prioriser les bords du tableau 
    #             add = self.buildSeegaAction(possible_positions)
    #             pprint(SeegaRules.is_legal_move(state, SeegaAction(action_type=SeegaActionType.ADD, to=possible_positions[0]), self.position))
    #             pprint((1 , 2))
    #             pprint(possible_positions[0])
    #             pprint(add)
    #         else:
    #             # self.place_near_edge(state)
    #             good_edges = self.place_near_edge(state)
    #             if good_edges:
    #                 add = self.buildSeegaAction(good_edges)
    #             else:
    #                 add = SeegaRules.random_play(state, self.position)     
    #     else:
    #         # it's muy turn to play. Nous allons chercher a serrer les cotés (de preference la ou a deja le plus de pion mais ce n'est obligatoire)
    #         # sinon prioriser les bords du tableau 
    #         add = SeegaRules.random_play(state, self.position)

    #     return add

    # def place_near_edge(self, state):
    #     available_positions = SeegaRules.get_player_all_cases_actions(state, self.position)
    #     available_positions_list = []
    #     for x in available_positions:
    #         available_positions_list.append(x.action.get('to'))

    #     return self.check_edges_first(available_positions_list)

    # # priorise les positions voisines dans le
    # def neighbours(self, state, t):
    #     ranges = [(x-1, x, x+1) for x in t]
    #     result = list(product(*ranges))
    #     result.pop(len(result) // 2)
    #     maList=[]
    #     for x in result:
    #         if not (x[0] < 0 or x[1] < 0) and x in state.get_board().get_all_empty_cells_without_center() : 
    #             maList.append(x)
    #     maList = sorted(maList, key=lambda tup: tup[0])
    #     return self.check_edges_first(maList)
 
    # # sort les places disponibles sur les bords du tableau || prioriser les bords du tableau
    # def check_edges_first(self, actions):
        # edges = {(0, 1), (0, 2), (0, 3), (0, 4), (1, 1), (1, 4), (2, 1), (2, 4), (3, 1), (3, 4), (4, 1), (4, 2), (4, 3), (4, 4)} 
        # good = list(set(edges).intersection(set(actions)))
        # if good is not None:
        #     return good
        # else:
        #     return actions

    def buildSeegaAction(self, couples):
        return SeegaAction(action_type=SeegaActionType.ADD, to=couples[0])


    def best_action(self, state):
        actions = SeegaRules.get_player_all_cases_actions(state, self.position)
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


# Return a number which indicates how good is the board for this IA
    # We personnally do a simple difference between scores (but this is the method that must be improved, we think)

    def evaluate(self, board):
        import random
        #return random.randrange(10)

        return random.randrange(10) + board.score[self.position] - board.score[self.position * -1]


