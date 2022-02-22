# (n^2)-n number of games to play where n is the # of players
def play_cycle(pop):
    for p1 in pop.players:
        for p2 in pop.players:
            if not p1 == p2:
                play_round(p1, p2)


# Play 64 rounds against the same opponent
def play_round(p1, p2):
    for x in range(0, 64):
        play_turn(p1, p2)


def play_turn(p1, p2):
    # Players making their moves
    p1_move = p1.strategy()
    p2_move = p2.strategy()

    # Get results
    p1_result = p1_move + p2_move
    p2_result = p2_move + p1_move

    match p1_result:
        case 'CC':
            p1_score = 1
        case 'CD':
            p1_score = 20
        case 'DC':
            p1_score = 0
        case 'DD':
            p1_score = 10
        case _:
            p1_score = 0

    match p2_result:
        case 'CC':
            p2_score = 1
        case 'CD':
            p2_score = 20
        case 'DC':
            p2_score = 0
        case 'DD':
            p2_score = 10
        case _:
            p2_score = 0

    # Update player's score
    p1.fitness += p1_score
    p2.fitness += p2_score

    # Update each player's game history
    p1.update_history(p1_result)
    p2.update_history(p2_result)
