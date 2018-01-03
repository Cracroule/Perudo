from math import ceil
from perudo.announce import BluffAnnounce, ExactAnnounce, RaiseAnnounce
import random


def next_superior_announce(announce, is_paradisio):
    qty = 1
    face = 2
    if announce:
        qty = announce.dice_quantity
        face = announce.dice_face
    if is_paradisio:
        return RaiseAnnounce(qty+1, face)
    if face not in (6, 1):
        return RaiseAnnounce(qty, face + 1)
    if face == 6:
        if qty % 2:
            return RaiseAnnounce(qty+1, 2)
        else:
            return RaiseAnnounce(int(qty / 2), 1)
    if face == 1:
        return RaiseAnnounce(qty * 2 + 1, 2)


class DummyReasonablePlayer(object):

    def __init__(self, name, seed=0):
        self.name = name
        self.randgen = random.Random(seed)

    def play_turn(self, my_dices, prev_announce, is_paradisio, nb_of_players, nb_of_remaining_dices, round_history):
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

        return next_superior_announce(prev_announce, is_paradisio)

