"""
Created on 26 oct. 16:01 2020

@author: HaroldKS
"""

from core import Player
from seega.seega_rules import SeegaRules
import copy
import random

class AI(Player):

    in_hand = 12
    score = 0
    depth = 0
    proposed_action = None
    all_currents_nodes_search = 0
    def evaluate_leaf(self, state):
        return SeegaRules.get_results(state)

# max function
    def max(self, state):

        maxv = -2
        clone_ai = self
        p_action = None
        
        if self.depth >= 3:
            result = self.evaluate_leaf(state)
            print(result['score'][self.position])
            if result['tie'] == True:
                mscore = result['score'][self.position]
                return (mscore, p_action)
            elif result['winner'] == self.position:
                mscore = result['score'][self.position]
                print("i win")
                return (mscore, p_action)
            elif result['winner'] == -self.position:
                mscore = result['score'][self.position]
                print("i loose")
                return (mscore, p_action)

        if state.phase == 2:
            print("current player is:", self.position)
            clone_state = copy.deepcopy(state)
            actions = SeegaRules.get_player_all_cases_actions(clone_state, self.position)
            if actions:
                for action in actions:
                    if SeegaRules.is_legal_move(clone_state, action, self.position):
                        SeegaRules.make_move(clone_state, action, clone_ai.position)
                        self.all_currents_nodes_search +=1
                        (score, re_action) = self.min(clone_state, -self.position)
                        self.depth += 1
                        if maxv < score :
                            maxv = score
                            p_action = action
                            print("cant be none")
                            self.proposed_action = p_action
                        if maxv == score :
                            self.proposed_action = random.choice([self.proposed_action, action])
                        clone_state = copy.deepcopy(state)


        return (maxv, p_action)

# min function 
    def min(self, state, player):
        minv = 13
        p_action =None

        if self.depth >= 3:
            result = self.evaluate_leaf(state)
            print(result['score'][self.position])
            if result['tie'] == True:
                mscore = result['score'][self.position]
                return (mscore, p_action)
            elif result['winner'] == self.position:
                mscore = result['score'][self.position]
                print("i win")
                return (mscore, p_action)
            elif result['winner'] == -self.position:
                mscore = result['score'][self.position]
                print("i loose")
                return (mscore, p_action)

        if state.phase == 2:
            print("Adversary player is:", player)
            clone_state = copy.deepcopy(state)
            actions = SeegaRules.get_player_all_cases_actions(clone_state, player)
            if actions:
                for action in actions:
                    p_depth = 0
                    if SeegaRules.is_legal_move(clone_state, action, player):
                        self.depth +=1
                        SeegaRules.make_move(clone_state, action, player)
                        self.all_currents_nodes_search +=1
                        (score, re_action) = self.max(clone_state)
                        if minv > score:
                            minv = score
                            p_action = action
                        clone_state = copy.deepcopy(state)
        return (minv, p_action)

    def __init__(self, color):
        super(AI, self).__init__(color)
        self.position = color.value

#  play the game
    def play(self, state, remain_time):
        print(f"Player {self.position} is playing.")
        print("time remain is ", remain_time, " seconds")
        self.depth = 0
        self.max(state)
        print(self.proposed_action)
        # action = SeegaRules.random_play(state, self.position)
        if state.phase == 2:
            return self.proposed_action
        return SeegaRules.random_play(state, self.position)

    def set_score(self, new_score):
        self.score = new_score

    def update_player_infos(self, infos):
        self.in_hand = infos['in_hand']
        self.score = infos['score']
        
    def reset_player_informations(self):
        self.in_hand = 12
        self.score = 0
