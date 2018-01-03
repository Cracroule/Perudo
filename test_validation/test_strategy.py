from perudo.strategy import binomial, fact, combi, proba_nb_dices_is_k, \
    proba_nb_dices_is_less_than_k, proba_nb_dices_is_more_than_k

eps = 10e-6


def test_fact():
    prod = 1
    for i in range(15)[1:]:
        prod = prod * i
        assert fact(i) == prod


def test_combi():
    assert combi(3, 5) == 10
    assert combi(2, 5) == 10
    assert combi(5, 5) == 1
    assert combi(0, 5) == 1
    assert combi(1, 5) == 5
    assert combi(4, 5) == 5
    assert combi(3, 6) == 20
    assert combi(2, 6) == 15
    assert combi(7, 6) == 0  # <- important to get consistent behavior !


def test_estimated_probabilities():
    nb_remaining_dices = 10
    is_paradisio_or_paco = False
    for k in range(nb_remaining_dices+1):
        p_less = proba_nb_dices_is_less_than_k(k, nb_remaining_dices, is_paradisio_or_paco)
        p_exact = proba_nb_dices_is_k(k, nb_remaining_dices, is_paradisio_or_paco)
        p_more = proba_nb_dices_is_more_than_k(k, nb_remaining_dices, is_paradisio_or_paco)
        assert p_less + p_exact + p_more == 1


def play_binomial():
    nb_of_dices = 10
    p_sum = 0.
    for i in range(nb_of_dices):
        p = binomial(1. / 6, i, nb_of_dices)
        p_sum += p
        print('P( X =', i, ') =', round(p, 4), '     P( X >', i, ') =', round(1-p_sum, 4))
