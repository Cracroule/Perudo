import random


class Dice(object):

    def __init__(self, nb_of_faces, seed=0):
        self.all_faces = range(nb_of_faces + 1)[1:]
        self.randgen = random.Random(seed)

    def __str__(self):
        return 'I am a dice with %d faces' % (len(self.all_faces))

    def roll(self):
        return self.randgen.choice(self.all_faces)
