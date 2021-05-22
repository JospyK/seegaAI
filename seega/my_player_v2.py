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

    def buildSeegaAction(self, couples):
        return SeegaAction(action_type=SeegaActionType.ADD, to=couples[0])


    def best_action(self, board):

        bestMove = None
        bestMoveScore = 0
        possibleBoards = []
        moves = SeegaRules.get_player_all_cases_actions(board, self.position)

        # Générer tous les state de ce noeud
        for move in moves:
            newBoard = board
            newBoard, is_the_end = SeegaRules.make_move(newBoard, move, self.position)
            possibleBoards.append(newBoard)

        bestMove = moves[0]
        bestMoveScore = self.minimax(possibleBoards[0], float('-inf'), float('inf'), self.DEPTH, self.position)
        i = -1
        for aBoard in possibleBoards:
            i += 1
            if i > 1:
                score = self.minimax(aBoard, float('-inf'), float('inf'), self.DEPTH, self.position)
                if score > bestMoveScore:
                    bestMove = moves[i]
                    bestMoveScore = score

        w, x, y, z, color = bestMove

        return w, x, y, z



    def minimax(self, board, alpha, beta, depth, actual_player):

        if depth == 0:
            return self.evaluate(board)

        if actual_player == self.position:
            moves = SeegaRules.get_player_all_cases_actions(board, self.position)

            newBeta = beta
            for move in moves:
                next_board = board
                next_board, is_the_end = SeegaRules.make_move(next_board, move, self.position)
                newBeta = min(newBeta, self.minimax(next_board, alpha, beta, depth-1, self.position))  
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
