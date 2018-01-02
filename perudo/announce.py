#from perudo.dice import DiceFace


class RaiseAnnounce(object):

    def __init__(self, dice_quantity, dice_face):
        self.dice_quantity = dice_quantity
        self.dice_face = dice_face

    def __str__(self):
        #return str((self.dice_quantity, str(self.dice_face)))
        return "'There is at least %i dices with a value of %i'" % (self.dice_quantity, self.dice_face)

    def __lt__(self, other):
        if self.dice_face == other.dice_face:
            return self.dice_quantity < other.dice_quantity
        if self.dice_face == 1:
            return self.dice_quantity * 2 < other.dice_quantity
        if other.dice_face == 1:
            return self.dice_quantity <= other.dice_quantity * 2
        if self.dice_quantity == other.dice_quantity:
            return self.dice_face < other.dice_face
        return self.dice_quantity < other.dice_quantity

    def __eq__(self, other):
        return self.dice_quantity == other.dice_quantity and self.dice_face == other.dice_face

    def __ne__(self, other):
        return not (self.dice_quantity == other.dice_quantity and self.dice_face == other.dice_face)

    def __gt__(self, other):
        if self.dice_face == other.dice_face:
            return self.dice_quantity > other.dice_quantity
        if self.dice_face == 1:
            return self.dice_quantity * 2 >= other.dice_quantity
        if other.dice_face == 1:
            return self.dice_quantity > other.dice_quantity * 2
        if self.dice_quantity == other.dice_quantity:
            return self.dice_face > other.dice_face
        return self.dice_quantity > other.dice_quantity

    def __ge__(self, other):
        if self.dice_face == other.dice_face:
            return self.dice_quantity >= other.dice_quantity
        if self.dice_face == 1:
            return self.dice_quantity * 2 >= other.dice_quantity
        if other.dice_face == 1:
            return self.dice_quantity > other.dice_quantity * 2
        if self.dice_quantity == other.dice_quantity:
            return self.dice_face >= other.dice_face
        return self.dice_quantity > other.dice_quantity

    def __le__(self, other):
        if self.dice_face == other.dice_face:
            return self.dice_quantity <= other.dice_quantity
        if self.dice_face == 1:
            return self.dice_quantity * 2 < other.dice_quantity
        if other.dice_face == 1:
            return self.dice_quantity <= other.dice_quantity * 2
        if self.dice_quantity == other.dice_quantity:
            return self.dice_face <= other.dice_face
        return self.dice_quantity < other.dice_quantity

    def __hash__(self):
        return hash((self.dice_quantity, self.dice_face))


class BluffAnnounce(object):
    def __init__(self, challenged_announce):
        self.challenged_announce = challenged_announce

    def __str__(self):
        return "Announce: 'Bluff !'"


class ExactAnnounce(object):
    def __init__(self, challenged_announce):
        self.challenged_announce = challenged_announce

    def __str__(self):
        return "Announce: 'ExactAnnounce !'"
