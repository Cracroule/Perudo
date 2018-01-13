import sys
from perudo.announce import BluffAnnounce, ExactAnnounce, RaiseAnnounce, get_next_raise_announce
from perudo.player import DummyReasonablePlayer, ProbabilisticPlayer, GenericPlayer
from perudo.perudo import Perudo


class HumanPlayer(GenericPlayer):

    def __init__(self, name, seed=0):
        self.name = name
        self.cache = dict()

    def play_turn(self, my_dices, prev_announce, is_paradisio, remaining_dices, my_player_index, round_history):
        paradisio_str = '' if not is_paradisio else "   it's PARADISIO !"
        print('')
        print("It's your turn ! your dices are:", my_dices, paradisio_str)
        s = '  '
        for i in range(len(remaining_dices)):
            p_name = self.cache['players_names'][i]
            if p_name != self.name:
                s = s + p_name + ' has ' + str(remaining_dices[i]) + ' dices left     '
        print(s)
        if len(round_history):
            print("  So far, the below announces are the most recent ones;")
            for player_name, announce in round_history[-len(self.cache['players_names']):]:
                print('  ', player_name, '-->', announce)
        else:
            print("  You are the very fist one to announce")
        while True:
            r_b_e = input('What do you want to do ? raise (r), bluff (b), exact (e) : ')
            if r_b_e not in ('r', 'b', 'e'):
                print("please announce 'r' or 'b' or 'e'")
            else:
                if not len(round_history) and r_b_e in ('b', 'e'):
                    print("you can t call exact or bluff when starting round")
                elif r_b_e == 'b':
                    print('you called bluff !')
                    return BluffAnnounce(prev_announce)
                elif r_b_e == 'e':
                    print('you called exact !')
                    return ExactAnnounce(prev_announce)
                elif r_b_e == 'r':
                    qty = int(input("how many dices do you want to announce? : "))
                    dice_value = int(input("for which dice face value ? : "))
                    print("your announce is 'There is at least %i dices with a value of %i'" % (qty, dice_value))
                    return RaiseAnnounce(qty, dice_value)

    def notify_start_of_game(self, list_of_players_names, starting_player_index):
        print("A new perudo game has started !   the contestants are:", list_of_players_names)
        print(list_of_players_names[starting_player_index], "will starts first")
        self.cache['players_names'] = list_of_players_names

    def notify_end_of_game(self, winner_name, game_history):
        print()
        print('#####################################')
        print("###      %s won this game     !!! ###" % winner_name)
        print('#####################################')
        print()

    def notify_end_of_round(self, ending_announce, all_rolled_dices, announce_player_i,
                            ending_announce_correctness, round_history, is_paradisio_round):
        print("")
        print("A round just ended! The last announces were;")
        for player_name, announce in round_history[-len(self.cache['players_names']):]:
            print('  ', player_name, '-->', announce)
        print("The dices were the following:")
        total_dice_qty = 0
        for i in range(len(all_rolled_dices)):
            p_dice = all_rolled_dices[i]
            paco_str = ''
            if is_paradisio_round or ending_announce.challenged_announce.dice_face == 1:
                called_dice_qty = p_dice.count(ending_announce.challenged_announce.dice_face)
            else:
                called_dice_qty = p_dice.count(ending_announce.challenged_announce.dice_face)
                paco_qty = p_dice.count(1)
                paco_str += '+ %i pacos =  %i' % (paco_qty, called_dice_qty + paco_qty)
            print(self.cache['players_names'][i], ':', p_dice, ' -> contains %i' % called_dice_qty, paco_str)
            total_dice_qty += called_dice_qty
        if ending_announce_correctness:
            print('  for a total of %i, so the last challenge was correct' % total_dice_qty)
            if isinstance(ending_announce, BluffAnnounce):
                input('  %s lost a dice      (press any key to continue)' % round_history[-2][0])
            else:
                input('  %s earned a dice      (press any key to continue)' % round_history[-1][0])
        else:
            print('for a total of %i, so the last challenge was not correct' % total_dice_qty)
            input('  %s lost a dice      (press any key to continue)' % round_history[-1][0])
            # if isinstance(ending_announce, BluffAnnounce):
            #     input('  %s lost a dice      (press any key to continue)' % round_history[-1][0])
            # else:
            #     input('  %s earned a dice      (press any key to continue)' % round_history[-1][0])


def main():
    dice_per_player = 5
    faces_per_dice = 6
    perudo = Perudo(dice_per_player, faces_per_dice)
    players = list()
    players.append(ProbabilisticPlayer('Einstein'))
    players.append(DummyReasonablePlayer('Dummy1'))
    players.append(HumanPlayer('You'))

    perudo.play_game(players)


if __name__ == '__main__':
    main()
