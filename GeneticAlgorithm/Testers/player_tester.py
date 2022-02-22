from GeneticAlgorithm.player import Player


def play(p1, p2, n=0):

    print("\nPlay: ")

    print("\t\t\t", p1.strat_name, "\t", p2.strat_name, sep="")

    for x in range(0, n):

        # Players making their moves
        p1_move = p1.strategy()
        p2_move = p2.strategy()

        # Get results
        p1_result = p1_move + p2_move
        p2_result = p2_move + p1_move

        # Update each player's game history
        p1.update_history(p1_result)
        p2.update_history(p2_result)

        # Print info
        print("Round ", x+1, ": \t", p1_move, "\t\t", p2_move, sep="")


if __name__ == '__main__':

    player1 = Player(strat="stft")
    player2 = Player(strat="all_c")

    play(player1, player2, 10)

    # p = Player(strat="random_choice")
    # p.test_against_random()
    # print(p.get_encoding_string())
