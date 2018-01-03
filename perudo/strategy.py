def fact(k):
    if k <= 1:
        return 1
    return fact(k-1) * k


def combi(k, n):
    if k > n:
        return 0
    l, m = max(k, n-k), min(k, n-k)
    numerator = 1
    for i in range(l+1, n+1):
        numerator *= i
    denominator = fact(m)
    return numerator / denominator


def binomial(p, k, n):
    return combi(k, n) * (p ** k) * ((1. - p) ** (n-k))


# returns probability than nb of actual remaining dices is equal to k
def proba_nb_dices_is_k(k, nb_remaining_dices, is_paco_or_paradisio, nb_faces_per_dice=6):
    p = 1. / nb_faces_per_dice if is_paco_or_paradisio else 2. / nb_faces_per_dice
    return binomial(p, k, nb_remaining_dices)


# returns probability than nb of actual remaining dices is strictly less than k
def proba_nb_dices_is_less_than_k(k, nb_remaining_dices, is_paco_or_paradisio, nb_faces_per_dice=6):
    p = 1. / nb_faces_per_dice if is_paco_or_paradisio else 2. / nb_faces_per_dice
    return sum([binomial(p, i, nb_remaining_dices) for i in range(k)])


# returns probability than nb of actual remaining dices is strictly more than k
def proba_nb_dices_is_more_than_k(k, nb_remaining_dices, is_paco_or_paradisio, nb_faces_per_dice=6):
    return 1.-proba_nb_dices_is_less_than_k(k+1, nb_remaining_dices, is_paco_or_paradisio, nb_faces_per_dice)

