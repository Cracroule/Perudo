import pytest
from perudo.perudo import Perudo
from perudo.player import DummyReasonablePlayer
# from perudo.announce import BluffAnnounce, ExactAnnounce, RaiseAnnounce


@pytest.fixture()
def four_players():
    players = [DummyReasonablePlayer(s) for s in ["Dummy1", "Dummy2", "Dummy3", "Dummy4"]]
    return players


@pytest.fixture()
def perudo():
    dice_per_player = 5
    faces_per_dice = 6
    return Perudo(dice_per_player, faces_per_dice)


def test_roll_all_dices(perudo):
    remaining_dices = [5, 5, 5]
    obtained_dices = perudo.roll_all_dices(remaining_dices)
    for i in range(len(remaining_dices)):
        assert len(obtained_dices[i]) == remaining_dices[i]


def test_perudo_game(perudo, four_players):
    perudo.play_game(four_players)


def test_game_with_same_name_players(perudo, four_players):
    four_players[0].name = four_players[1].name
    crashed = False
    try:
        perudo.play_game(four_players)
    except NameError:
        crashed = True
    assert crashed
