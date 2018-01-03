import pytest
import random
from math import ceil
from perudo.player import DummyReasonablePlayer, ProbabilisticPlayer
from perudo.announce import BluffAnnounce, ExactAnnounce, RaiseAnnounce, check_announce_consistency


# when creating a new player, just add it on the below method to validate it
@pytest.fixture()
def all_kind_of_players():
    all_players = list()
    all_players.append(DummyReasonablePlayer("I am Dummy"))
    all_players.append(ProbabilisticPlayer('Einstein'))
    return all_players


@pytest.fixture()
def all_kind_of_initial_situations():
    randgen = random.Random(0)
    list_of_situations = list()
    for nb_of_remaining_dices in range(20)[2:]:
        for i in range(11)[1:]:
            my_dices = [randgen.choice((1, 2, 3, 4, 5, 6)) for i in range(min(5, nb_of_remaining_dices-1))]
            is_paradisio = True if i <= 3 else False
            min_nb_of_players = max(ceil(nb_of_remaining_dices/5), 2)
            max_nb_of_players = 4
            nb_of_players = int(min_nb_of_players + i * (max_nb_of_players - min_nb_of_players) / 10)
            situation = {'prev_announce': None, 'nb_of_remaining_dices': nb_of_remaining_dices, 'my_dices': my_dices,
                         'is_paradisio': is_paradisio, 'round_history': None, 'nb_of_players': nb_of_players}
            assert nb_of_players * 5 >= nb_of_remaining_dices
            list_of_situations.append(situation)
    return list_of_situations


def test_first_plays(all_kind_of_players, all_kind_of_initial_situations):
    for player in all_kind_of_players:
        for situation in all_kind_of_initial_situations:
            prev_announce = situation['prev_announce']
            nb_of_remaining_dices = situation['nb_of_remaining_dices']
            my_dices = situation['my_dices']
            is_paradisio = situation['is_paradisio']
            round_history = situation['round_history']
            nb_of_players = situation['nb_of_players']

            i = 0
            announce = None
            while not (isinstance(announce, BluffAnnounce) or isinstance(announce, ExactAnnounce) or i > 10):
                announce = player.play_turn(my_dices, prev_announce, is_paradisio, nb_of_players,
                                            nb_of_remaining_dices, round_history)
                check_announce_consistency(announce, prev_announce, is_paradisio)
                prev_announce = announce
                i += 1

            if isinstance(announce, BluffAnnounce) or isinstance(announce, ExactAnnounce):
                assert isinstance(announce.challenged_announce, RaiseAnnounce)