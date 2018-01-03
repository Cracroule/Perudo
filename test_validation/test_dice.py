import perudo as po
from perudo.dice import Dice


# check obtained distribution looks ok
def test_dice_randomness_uniformity():
    n = 10000
    dice_nb_of_faces = 6
    dice = Dice(dice_nb_of_faces)
    d = dict()
    for i in range(n):
        r = dice.roll()
        if r in d.keys():
            d[r] += 1
        else:
            d[r] = 1
    assert len(d) == dice_nb_of_faces
    for key, val in d.items():
        assert n / (dice_nb_of_faces + 1) <= val <= n / (dice_nb_of_faces - 1)


def test_dice_randomness_consistency():
    n = 100
    dice_nb_of_faces = 6

    # check dices provide same results if used with same seed
    all_results = list()
    for d in range(10):
        dice = Dice(dice_nb_of_faces, 0)
        dice_results = list()
        for i in range(n):
            dice_results.append(dice.roll())
        all_results.append(dice_results)
    for d in range(10)[1:]:
        for i in range(n):
            assert all_results[0][i] == all_results[d][i]

    # check dices provide different results if used with different seed
    n = 10000
    dice1 = Dice(dice_nb_of_faces, seed=0)
    dice2 = Dice(dice_nb_of_faces, seed=1)
    dice1_results, dice2_results = list(), list()
    for i in range(n):
        dice1_results.append(dice1.roll())
        dice2_results.append(dice2.roll())
    correl = 0
    for i in range(n):
        if dice1_results[i] == dice2_results[i]:
            correl += 1
    correl /= float(n)
    assert 1. / (dice_nb_of_faces + 1) <= correl <= 1. / (dice_nb_of_faces - 1)
