from perudo.dice import Dice
from perudo.announce import BluffAnnounce, RaiseAnnounce, ExactAnnounce


def next_living_player_index(remaining_dices, player_index):
    cur_player_index, i = player_index, 0
    while i <= len(remaining_dices):
        cur_player_index = (cur_player_index + 1) % len(remaining_dices)
        if remaining_dices[cur_player_index]:
            return cur_player_index
        i += 1
    raise Exception("no living players anymore")


def prev_living_player_index(remaining_dices, player_index):
    cur_player_index, i = player_index, 0
    while i <= len(remaining_dices):
        cur_player_index = (cur_player_index - 1) % len(remaining_dices)
        if remaining_dices[cur_player_index]:
            return cur_player_index
        i += 1
    raise Exception("no living players anymore")


class Perudo(object):

    def __init__(self, dice_per_player=5, faces_per_dice=6):
        self.dice_per_player = dice_per_player
        self.faces_per_dice = faces_per_dice
        self.dice = Dice(faces_per_dice)

    # fill dice_draws list with obtained values rolling dices for each player
    def roll_all_dices(self, remaining_dice):
        all_rolled_dices = list()
        for i in range(len(remaining_dice)):
            all_rolled_dices.append([self.dice.roll() for d in range(remaining_dice[i])])
        return all_rolled_dices

    def update_remaining_dice(self, delta, player_i, remaining_dices, paradisio_unmet):
        remaining_dices[player_i] += delta
        if remaining_dices[player_i] > self.dice_per_player:
            remaining_dices[player_i] = self.dice_per_player
        if remaining_dices[player_i] == 1 and paradisio_unmet[player_i]:
            paradisio_unmet[player_i] = False  # Paradisio !
            return True
        return False

    def play_game(self, list_of_players, starting_player_index=0):
        if len(set([e.name for e in list_of_players])) != len([e.name for e in list_of_players]):
            raise Exception("Attempt to start a game with players with same name ! please rename a player")

        player_index = starting_player_index
        remaining_dices = [self.dice_per_player] * len(list_of_players)
        paradisio_unmet = [True] * len(list_of_players)
        is_paradisio_round = False

        game_history = list()  # history of the game
        while True:
            rolled_dices = self.roll_all_dices(remaining_dices)
            # play all rounds until challenge
            res_round = self.play_round_until_challenge(list_of_players, rolled_dices, is_paradisio_round,
                                                        remaining_dices, player_index)
            announce, announce_player_i, round_history = res_round
            actual_dices_count = self.count_dices(rolled_dices, announce.challenged_announce.dice_face,
                                                  is_paradisio_round)
            # apply reward
            player_index = announce_player_i
            if isinstance(announce, BluffAnnounce):
                if actual_dices_count < announce.challenged_announce.dice_quantity:
                    delta, correct_challenge = -1, True
                    player_index = prev_living_player_index(remaining_dices, player_index)
                else:
                    delta, correct_challenge = -1, False
            else:  # so isinstance(announce, ExactAnnounce) is True
                correct_challenge = actual_dices_count == announce.challenged_announce.dice_quantity
                delta = 1 if correct_challenge else -1
            is_paradisio_round = self.update_remaining_dice(delta, player_index, remaining_dices, paradisio_unmet)
            for player in list_of_players:
                player.notify_end_of_round(announce, rolled_dices, announce_player_i, correct_challenge, round_history)

            game_history.append((round_history, rolled_dices))  # save history
            if remaining_dices[player_index]:  # dead player ? so he does not start next turn
                player_index = prev_living_player_index(remaining_dices, player_index)
            if next_living_player_index(remaining_dices, player_index) == player_index:
                for player in list_of_players:
                    player.notify_end_of_game(list_of_players[player_index].name, game_history)
                return list_of_players[player_index], game_history

    # count dices of chosen face
    @staticmethod
    def count_dices(rolled_dices, challenged_dice_face, is_paradisio_round):
        d = 0
        for player_dices in rolled_dices:
            for dice in player_dices:
                if dice == challenged_dice_face:
                    d += 1
                if dice == 1 and challenged_dice_face != 1 and not is_paradisio_round:
                    d += 1
        return d

    @staticmethod
    def play_round_until_challenge(list_of_players, rolled_dices, is_paradisio, remaining_dices,
                                   first_player_index):
        announce = None
        round_history = list()
        player_i = first_player_index
        while not (isinstance(announce, BluffAnnounce) or isinstance(announce, ExactAnnounce)):
            # play turn
            player = list_of_players[player_i]
            prev_announce = announce
            announce = player.play_turn(rolled_dices[player_i], prev_announce, is_paradisio, remaining_dices,
                                        player_i, round_history)
            if prev_announce and isinstance(announce, RaiseAnnounce):
                assert prev_announce < announce
                if is_paradisio:
                    assert prev_announce.dice_face == announce.dice_face
            round_history.append((player.name, announce))

            # next player index
            announce_player_index = player_i
            player_i = next_living_player_index(remaining_dices, player_i)

        return announce, announce_player_index, round_history
