from math import ceil
from perudo.announce import BluffAnnounce, ExactAnnounce, RaiseAnnounce, get_next_raise_announce
from perudo.strategy import proba_nb_dices_is_k, proba_nb_dices_is_more_than_k, proba_nb_dices_is_less_than_k
import random


""" A player is an object, with:
    - a name attribute (unique !)
    - a play_turn method (returns an announce)
    - a notify_end_of_round method (does nothing, might be used to analyse other players)
    - a notify_end_of_game method (does nothing, might be used to analyse other players)
    The last two methods mights be inherited from GenericPlayer"""


class GenericPlayer(object):
    def __init__(self):
        raise NotImplementedError("I am a f*cking Generic player")

    def play_turn(self, my_dices, prev_announce, is_paradisio, remaining_dices, my_player_index, round_history):
        raise NotImplementedError("I am a f*cking Generic player, i don t know how to play")

    def notify_start_of_game(self, players_names, starting_player_index):
        pass

    def notify_end_of_game(self, winner_name, game_history):
        pass

    def notify_end_of_round(self, ending_announce, all_rolled_dices, announce_player_i,
                            ending_announce_correctness, round_history, is_paradisio_round):
        pass


# computes all probabilities, choose most probable one according to its criterias
# would be easily defeated by humans as always propose most probable issue
class ProbabilisticPlayer(GenericPlayer):
    def __init__(self, name, seed=0):
        self.name = name
        self.randgen = random.Random(seed)

    def play_turn(self, my_dices, prev_announce, is_paradisio, remaining_dices, my_player_index, round_history):
        nb_of_remaining_dices = sum([e for e in remaining_dices])
        assert remaining_dices[my_player_index] == len(my_dices)

        p_exact, p_bluff = 0, 0
        if prev_announce:
            my_same_dices_qty = my_dices.count(prev_announce.dice_face)
            missing_qty = prev_announce.dice_quantity - my_same_dices_qty
            is_paco_or_paradisio = True if is_paradisio else prev_announce.dice_face == 1
            if missing_qty >= 0:
                p_exact = proba_nb_dices_is_k(missing_qty, nb_of_remaining_dices - len(my_dices), is_paco_or_paradisio)
                p_bluff = proba_nb_dices_is_less_than_k(missing_qty, nb_of_remaining_dices - len(my_dices),
                                                        is_paco_or_paradisio)

        # get 12 following announces:
        following_announces = list()
        my_prev_announce = prev_announce
        for i in range(12):
            announce = get_next_raise_announce(my_prev_announce, is_paradisio)
            my_same_dices_qty = my_dices.count(announce.dice_face)
            missing_qty = announce.dice_quantity - my_same_dices_qty
            is_paco_or_paradisio = True if is_paradisio else announce.dice_face == 1
            if missing_qty > 0:
                p_correct_announce = 1. - proba_nb_dices_is_less_than_k(missing_qty,
                                                                        nb_of_remaining_dices - len(my_dices),
                                                                        is_paco_or_paradisio)
            else:
                p_correct_announce = 1.
            following_announces.append((announce, p_correct_announce))
            my_prev_announce = announce
        # sort obtained announces by likelyhood
        following_announces.sort(key=lambda x: x[1], reverse=True)

        # Decision here !
        p_best_anounce = following_announces[0][1]
        probabilities = [p_best_anounce, p_bluff, p_exact]
        best_index = probabilities.index(max(probabilities))
        if best_index == 0:
            return following_announces[0][0]
        if best_index == 1:
            if p_best_anounce + 0.1 >= p_bluff:
                return following_announces[0][0]
            if p_exact + 0.1 >= p_bluff:
                return ExactAnnounce(prev_announce)
            return BluffAnnounce(prev_announce)
        if p_best_anounce + 0.1 >= p_exact:
            return following_announces[0][0]
        return ExactAnnounce(prev_announce)


class DummyReasonablePlayer(GenericPlayer):

    def __init__(self, name, seed=0):
        self.name = name
        self.randgen = random.Random(seed)

    def play_turn(self, my_dices, prev_announce, is_paradisio, remaining_dices, my_player_index, round_history):
        nb_of_remaining_dices = sum([e for e in remaining_dices])
        assert remaining_dices[my_player_index] == len(my_dices)

        if prev_announce:
            announced_quantity = prev_announce.dice_quantity
            announced_face = prev_announce.dice_face
        else:
            announced_quantity = 1
            announced_face = 2

        if is_paradisio:
            my_max_quantity = int(ceil(nb_of_remaining_dices / 6. + 0.51))
        else:
            my_max_quantity = int(ceil(nb_of_remaining_dices / 3. + 0.51))

        if announced_face == 1:
            dangerous_quantity = int(ceil(my_max_quantity / 2 + 0.51))
        else:
            dangerous_quantity = my_max_quantity

        if announced_quantity >= dangerous_quantity:
            if prev_announce:
                decision = self.randgen.choice([1, 2, 2, 3, 3])
            else:
                decision = 3
            if decision == 1:
                return ExactAnnounce(prev_announce)
            elif decision == 2:
                return BluffAnnounce(prev_announce)

        return get_next_raise_announce(prev_announce, is_paradisio)

