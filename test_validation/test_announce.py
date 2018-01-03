import perudo as po
from perudo.announce import RaiseAnnounce


def test_raise_announce_arithmetic():
    nb_of_dice_faces = 6
    n = 20
    list_announces = list()
    for i in range(n)[1:]:
        for f in range(nb_of_dice_faces+1)[1:]:
            if f != 1:
                list_announces.append(RaiseAnnounce(i, f))
            else:
                if (i % 2) and i > 2:
                    list_announces.append(RaiseAnnounce(int((i-1)/2), 1))

    for i in range(len(list_announces))[1:]:
        i_prec = i-1
        assert list_announces[i_prec] < list_announces[i]
        assert list_announces[i_prec] <= list_announces[i]
        assert list_announces[i] > list_announces[i_prec]
        assert list_announces[i] >= list_announces[i_prec]
        assert list_announces[i] == list_announces[i]
        assert list_announces[i] != list_announces[i_prec]
        for j in range(len(list_announces))[i+1:]:
            assert list_announces[i] < list_announces[j]
            assert list_announces[i] <= list_announces[j]
            assert list_announces[j] > list_announces[i]
            assert list_announces[j] >= list_announces[i]


