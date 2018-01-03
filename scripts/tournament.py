from perudo.perudo import Perudo
from perudo.player import DummyReasonablePlayer, ProbabilisticPlayer


def main():
    dice_per_player = 5
    faces_per_dice = 6
    perudo = Perudo(dice_per_player, faces_per_dice)

    players = [DummyReasonablePlayer(s) for s in ["Dummy1", "Dummy2", "Dummy3"]]
    players.append(ProbabilisticPlayer('Einstein'))

    nb_of_games = 1000
    games_won = dict()
    for player in players:
        games_won[player.name] = 0
    for i in range(nb_of_games):
        winner, game_history = perudo.play_game(players)
        games_won[winner.name] += 1

    print("--- tournament results ---")
    for key, val in games_won.items():
        print(key, val)

if __name__ == '__main__':
    main()
