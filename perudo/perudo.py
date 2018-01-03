from perudo.dice import Dice
from perudo.announce import BluffAnnounce, RaiseAnnounce, ExactAnnounce


class Perudo(object):

    def __init__(self, dice_per_player=5, faces_per_dice=6):
        self.dice_per_player = dice_per_player
        self.faces_per_dice = faces_per_dice
        self.dice = Dice(faces_per_dice)

    # fill dice_draws list with obtained values rolling dices for each player
    def roll_all_dices(self, remaining_dice):
        all_dices = list()
        for i in range(len(remaining_dice)):
            all_dices.append([self.dice.roll() for d in range(remaining_dice[i])])
        return all_dices

    # count dices of chosen face
    @staticmethod
    def count_dices(rolled_dices, challenged_dice_face, is_paradisio_round):
        d = 0
        for player_dices in rolled_dices:
            for dice in player_dices:
                if dice == challenged_dice_face:
                    d += 1
                if dice == 1 and not is_paradisio_round:
                    d += 1
        return d

    @staticmethod
    def play_round_until_challenge(list_of_players, rolled_dices, is_paradisio, remaining_players,
                                   first_player_index):
        announce = None
        round_history = list()
        player_i = first_player_index
        nb_of_remaining_dices = sum([len(player_dices) for player_dices in rolled_dices])
        while not (isinstance(announce, BluffAnnounce) or isinstance(announce, ExactAnnounce)):
            # play turn
            player = list_of_players[player_i]
            prev_announce = announce
            announce = player.play_turn(rolled_dices[player_i], prev_announce, is_paradisio, len(list_of_players),
                                   nb_of_remaining_dices, round_history)
            if prev_announce and isinstance(announce, RaiseAnnounce):
                assert prev_announce < announce
                if is_paradisio:
                    assert prev_announce.dice_face == announce.dice_face
            round_history.append((player.name, announce))

            # next player index
            announce_player_index = player_i
            player_i = remaining_players[(remaining_players.index(player_i) + 1) % len(remaining_players)]

        return announce, announce_player_index, round_history

    def update_remaining_dice(self, delta, player_i, remaining_dices, paradisio_unmet):
        remaining_dices[player_i] += delta
        if remaining_dices[player_i] > self.dice_per_player:
            remaining_dices[player_i] = self.dice_per_player
        if remaining_dices[player_i] == 1 and paradisio_unmet[player_i]:
            # Paradisio !
            paradisio_unmet[player_i] = False
            return True
        return False

    def play_game(self, list_of_players, starting_player_index=0):
        player_index = starting_player_index
        remaining_dices = [self.dice_per_player] * len(list_of_players)
        paradisio_unmet = [True] * len(list_of_players)
        is_paradisio_round = False

        game_history = list()  # history of the game
        remaining_players = [i for i in range(len(remaining_dices)) if remaining_dices[i] > 0]

        while True:
            rolled_dices = self.roll_all_dices(remaining_dices)

            # play all rounds until challenge
            res_round = self.play_round_until_challenge(list_of_players, rolled_dices, is_paradisio_round,
                                                        remaining_players, player_index)
            announce, announce_player_i, round_history = res_round

            challenged_quantity = announce.challenged_announce.dice_quantity
            challenged_dice_face = announce.challenged_announce.dice_face
            actual_dices_count = self.count_dices(rolled_dices, challenged_dice_face, is_paradisio_round)

            # apply reward
            player_index = announce_player_i
            if isinstance(announce, BluffAnnounce):
                if actual_dices_count < challenged_quantity:
                    delta = -1
                    player_index = remaining_players[
                        (remaining_players.index(announce_player_i) - 1) % len(remaining_players)]
                else:
                    delta = -1
            elif isinstance(announce, ExactAnnounce):
                delta = 1 if actual_dices_count == challenged_quantity else -1

            next_player = remaining_players[(remaining_players.index(player_index) + 1) % len(remaining_players)]
            is_paradisio_round = self.update_remaining_dice(delta, player_index, remaining_dices, paradisio_unmet)

            game_history.append((round_history, rolled_dices))  # save history
            remaining_players = [i for i in range(len(remaining_dices)) if remaining_dices[i] > 0]
            if player_index not in remaining_players:  # dead player ?
                player_index = next_player
            if len(remaining_players) == 1:  # do we have a winner ?
                return list_of_players[remaining_players[0]], game_history
