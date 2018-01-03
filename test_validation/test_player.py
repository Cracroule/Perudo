import pytest
from perudo.player import DummyReasonablePlayer
from perudo.announce import BluffAnnounce, ExactAnnounce, RaiseAnnounce


@pytest.fixture()
def dummy_reasonable_player():
    return DummyReasonablePlayer("I am Dummy")


def test_play_few_turn(dummy_reasonable_player):
    player = dummy_reasonable_player
    my_dices = [4, 2, 5, 6, 1]  # whatever
    nb_of_players = 4  # whatever
    round_history = list()  # whatever
    nb_of_remaining_dices = 20
    is_paradisio = False
    prev_announce, announce = None, None
    i = 0
    list_announces = list()

    while not (isinstance(announce, BluffAnnounce) or isinstance(announce, ExactAnnounce) or i > 200):
        announce = player.play_turn(my_dices, prev_announce, is_paradisio, nb_of_players,
                                    nb_of_remaining_dices, round_history)
        list_announces.append(announce)
        i += 1
        if prev_announce and isinstance(announce, RaiseAnnounce):
            assert prev_announce < announce
            if is_paradisio:
                assert prev_announce.dice_face == announce.dice_face
        prev_announce = announce
