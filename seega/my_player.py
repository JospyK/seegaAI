"""
Created on 26 oct. 16:01 2020

@author: HaroldKS
"""

from seega.seega_state import SeegaState
from core import Player
from seega.seega_rules import SeegaRules
import math

from pprint import pprint


class AI(Player):

    in_hand = 12
    score = 0
    name= "Groupe2"

    def __init__(self, color):
        super(AI, self).__init__(color)
        self.position = color.value

    def play(self, state, remain_time):
        print(f"Player {self.position} is playing.")
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
        return SeegaRules.random_play(state, self.position)


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
        # https://pdf.sciencedirectassets.com/280203/1-s2.0-S1877050919X00162/1-s2.0-S1877050919316783/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjENr%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIAFkexBAWIb4N4SUUOLfdjIizAQbTBTmYPJqcY7AdBlFAiEAtcSjWUzkUJI4qc2KC4BVZBwgKdQDm4%2BT2Xkoy%2BhmEQUqtAMIchADGgwwNTkwMDM1NDY4NjUiDEYKkrjGPWb6hr4UlyqRAxJV1ahY%2BCJ5Fpfj%2BCTzjhQ70KZeK1wxp9v%2BySA%2Bo2M2ojsRvt72D49SxVwdP2Sqia5%2Fyw6TpUNWkCJ5BVhgqtmrFjtZ9g4oGkYAm2fA1IODiR607CMwPwQzp76zg88YojeljwFH%2BuY6Melu5zbxKRkXa1k%2FqXKA7Dy6eux2EK6jwIpTRqmOFG1zN7OhPcfLqexgHH3cnHmo4ZJgqIe3bod5vwIxc5A7M8ej00Hlx9zXLLXRf2CZ236UIs%2F5dEn1OqIuodCWomS02uQn61pIvwuB7LOv40lNUZzEbC5kPW%2BZfXlbf3HtGbhakOVXIv33XlI7UUwwUWPaQDeyBHTsj09lc0rjx4doDqskoPl8PPcQbdUhdLckiFi5Psjh8Y5kpHPeQa43zZJ5o5s%2BfI7Cgu8Ehcblpa9yjEwQMIW2Bqv1M5IJEIBDXW8qu66cAkiKE3vk0t88ZSa9cOwoMp1JF9iCbOHjdLVYbrrtaaEQCNUfCUhnqIF6DIu9UiPCFlKBgfphuYlFi7AJP%2BafytBzRtnvMPuuk4UGOusBHGLu2XjWaIUC3yRVCe9ylmhpdMn0vmR0f99YPDFfbhIg9zx0ZBaF4TxPBrorhp%2BQXPNSYYVustFSg6pLzd6oKewErFPAmNC9y0cNA4oks8s7wpKjN8EqtBGNvLe0JWMZPeTbnJGoFaQMNC29zslNlQMthKiNsK%2BhD4iEjfTbMRr6Xf8kIqd7236Lon2M9adY%2FH2Z1gvqfN1ATadThFBOzBy1kXJn2Q1X6Pw09shRDsQXZIYbpP0tUo3C8CtBOUnRUWy5iG%2BltDJuJqkjLfNt0xKnD4YSwAPYxIHfxVRmXWkU8gMktE0i0C0umg%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20210519T101934Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTYV63WXAPO%2F20210519%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=7211371b931d76beee6ab1aa41bb79ab4d15b58033808c8ef1a3deb3fea8660c&hash=973da00e3b7a41541f8371a566664bdd0c7f5b0388d9a98ddfbd77715f56c8c3&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S1877050919316783&tid=spdf-6447a68d-f066-458e-81a6-7c50038be81c&sid=ecc7d4184a5ff64bfd1909738c8e93a3b645gxrqb&type=client
        #Kt = ((N ∗ N − 1)/2) − Mt(P1)
        # ((5*5 - 1)/2) - 
        

        # pprint(vars(board))
        # pprint(self.get_player_info(self.position))

        import random
        # return random.randrange(10)

        return 12 - board.score[self.position]
        # return  board.score[self.position] - board.score[self.position * -1]
