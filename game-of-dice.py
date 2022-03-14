import random
from collections import OrderedDict


class Player:
    def __init__(self, name):
        self.finished_game = False
        self.name = name
        self.ones_rolled = 0
        self.rank = 0
        self.score = 0

    def has_finished_game(self):
        return self.finished_game

    def get_ones_rolled(self):
        return self.ones_rolled

    def get_player_name(self):
        return self.name

    def get_rank(self):
        return self.rank

    def get_score(self):
        return self.score

    def set_finished_game(self):
        self.finished_game = True

    def set_ones_rolled(self, val):
        self.ones_rolled = val

    def set_rank(self, rank):
        self.rank = rank

    def update_score(self, points):
        self.score += points


def roll_dice_and_update_score(player, players_ranking):
    dice_roll = random.randint(1, 6)

    if dice_roll == 1:
        player.set_ones_rolled(player.get_ones_rolled() + 1)
    print(f"{player.get_player_name()} rolled {dice_roll}\n")

    player.update_score(dice_roll)
    players_ranking[player.get_player_name()] = player.get_score()

    return dice_roll


def roll_again_for_6(last_dice_roll, player, completed_participants, players_ranking, players_ranked):
    if last_dice_roll == 6:
        while last_dice_roll == 6 and not player.has_finished_game():
            input(f"{player.get_player_name()} you rolled 6 press 'r' to roll again.\n")
            last_dice_roll = roll_dice_and_update_score(player, players_ranking)

            players_ranked = check_game_finished_for_player(
                player, completed_participants, players_ranking, players_ranked
            )

    return players_ranked


def check_game_finished_for_player(player, completed_participants, players_ranking, players_ranked):
    if player.get_score() >= target:
        player.set_rank(players_ranked)
        player.set_finished_game()
        print(f"Congratulations! {player.get_player_name()} you have completed the game with rank {player.get_rank()}")
        completed_participants[player.get_player_name()] = player
        del players_ranking[player.get_player_name()]
        return players_ranked + 1
    return players_ranked


def print_current_ranking_and_scores():
    curr_rank = 1
    print("\ncurrent rankings:")
    for key in completed_participants.keys():
        print(f"player: {key}   score: {completed_participants[key].score}   rank: {completed_participants[key].rank}")
        curr_rank += 1

    current_ranking = dict(sorted(players_ranking.items(), key=lambda x: x[1], reverse=True))
    for key in current_ranking.keys():
        print(f"player: {key}   score: {players_ranking[key]}   rank: {curr_rank}")
        curr_rank += 1


if __name__ == '__main__':
    n = int(input("Enter number of players participating.\n"))
    target = int(input("Enter the target points.\n"))

    players = []
    players_ranking = dict()
    for i in range(1, n + 1):
        players.append(Player(f"Player-{i}"))
        players_ranking[f"Player-{i}"] = 0

    no_of_players_ranked = 1
    participants = random.sample(players, len(players))
    players_ranking = dict(sorted(players_ranking.items(), key=lambda x: x[1], reverse=True))
    completed_participants = OrderedDict()

    while no_of_players_ranked <= n:
        for player in participants:
            if player.has_finished_game():
                continue
            if player.get_ones_rolled() == 2:
                # skipping the turn if player has rolled two consecutive ones.
                player.set_ones_rolled(0)
                continue

            input(f"\n{player.get_player_name()} it's your turn press 'r' to roll the dice\n")

            # simulate rolling dice for the player and update the scores
            dice_roll = roll_dice_and_update_score(player, players_ranking)

            # check if player has achieved the target in the dice roll.
            no_of_players_ranked = check_game_finished_for_player(
                player, completed_participants, players_ranking, no_of_players_ranked
            )

            # check if player has rolled 6 if yes then player gets another chance to roll the dice.
            no_of_players_ranked = roll_again_for_6(
                dice_roll, player, completed_participants, players_ranking, no_of_players_ranked
            )

            # print current rankings and scores of the players
            print_current_ranking_and_scores()

    print("Game Over!")







