from perudo.perudo import Perudo
from perudo.player import DummyReasonablePlayer


def main():
    dice_per_player = 5
    faces_per_dice = 6
    perudo = Perudo(dice_per_player, faces_per_dice)

    players = [DummyReasonablePlayer(s) for s in ["Dummy1", "Dummy2", "Dummy3", "Dummy4"]]

    nb_of_games = 1000
    games_won = {"Dummy1": 0, "Dummy2": 0, "Dummy3": 0, "Dummy4": 0}
    for i in range(nb_of_games):
        winner, game_history = perudo.play_game(players)
        games_won[winner.name] += 1

    print("--- tournament results ---")
    for key, val in games_won.items():
        print(key, val)

if __name__ == '__main__':
    main()