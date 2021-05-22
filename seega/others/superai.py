"""
Created on 26 oct. 16:01 2020

@author: HaroldKS
"""
import copy

from core import Player
from seega.seega_rules import SeegaRules

class AI(Player):

    in_hand = 12
    score = 0
    name = "SuperIA"

    def __init__(self, color):
        super(AI, self).__init__(color)
        self.position = color.value


    def minimax(self, state):
        
        if state.phase == 1:
            # premiere phase
            return SeegaRules.random_play(state, self.position)
        else:
            # phase de jeu
            state_copy = copy.deepcopy(state)
            print(state_copy.get_board().get_board_state())
            # we get current player moves
            my_possibles_actions = SeegaRules.get_player_all_cases_actions(
                state_copy,
                self.position
            )
            good_action = None
            max_score_min = -1
            max_score_min_max = 1000
            score = 0
            for my_action in my_possibles_actions:
                my_play_state, _ = SeegaRules.make_move(
                    state_copy,
                    my_action,
                    self.position
                )
                # we get current adverse moves
                ad_possibles_actions = SeegaRules.get_player_all_cases_actions(
                    my_play_state,
                    self.position * -1
                )
                
                score_min = 10000
                score_max = -1
                for ad_action in ad_possibles_actions:
                    my_play_state_cp = copy.deepcopy(my_play_state)
                    ad_play_state_cp, _ = SeegaRules.make_move(
                        my_play_state_cp,
                        ad_action,
                        self.position * 1
                    )
                    score = ad_play_state_cp.get_player_info(self.position)['score'] - (
                        ad_play_state_cp.get_player_info(-1 * self.position)['score']
                    )
                    if score > score_max:
                        score_max = score
                    elif score < score_min:
                        score_min = score

                if (score_min > max_score_min) or (score_min == max_score_min and score_max > max_score_min_max):
                    max_score_min = score_min
                    max_score_min_max = score_max
                    good_action = my_action
                    
            return good_action or SeegaRules.random_play(state, self.position)


    def play(self, state, remain_time):
        print(f"AI Player {self.position} is playing. And next player is {state.get_next_player()},  {state.get_latest_player()}")
        # print("time remain is ", remain_time, " seconds")
        print('\n'*5)
        return self.minimax(state)
        # SeegaRules.random_play(state, self.position)

    def set_score(self, new_score):
        self.score = new_score

    def update_player_infos(self, infos):
        self.in_hand = infos['in_hand']
        self.score = infos['score']
        
    def reset_player_informations(self):
        self.in_hand = 12
        self.score = 0
