from random import randint, random
from GeneticAlgorithm.player import Player


# 4 values to represent Reward, Sucker, Temptation, and Penalty game outcomes
v = {"CC": 2, "DC": 0, "CD": 3, "DD": 1, 2: "CC", 0: "DC", 3: "CD", 1: "DD"}


# (n^2)-n number of games to play where n is the # of players
def play_cycle(pop):
    for x in range(0, len(pop.players)):
        for y in range(0, len(pop.players)):
            if x is not y:
                play_round(pop.players[x], pop.players[y])


# Play 64 rounds against the same opponent
def play_round(p1, p2):
    for x in range(0, 64):
        play_game(p1, p2)
    p1.hist = [] * p1.mem
    p2.hist = [] * p2.mem


def play_game(p1, p2):
    # Players making their moves
    p1_move = p1.strategy()
    p2_move = p2.strategy()

    # print("p1 move: ", p1_move)
    # print("p2 move: ", p2_move)

    # Get results
    p1_result = p1_move + p2_move
    p2_result = p2_move + p1_move

    # print("p1 result: ", p1_result)
    # print("p2 result: ", p2_result)

    # Update player 1's score
    p1.fitness += v[p1_result]

    # print("p1 fitness: ", p1.fitness)
    # print("p1 fitness: ", p2.fitness)

    # Update each player's game history
    p1.update_history(p1_result)
    p2.update_history(p2_result)

    # print("p1 hist: ", p1.hist)
    # print("p2 hist: ", p2.hist)


def crossover(parents, mutation_chance, crossover_chance):
    crossover_point = randint(0, len(parents[0].lut) - 1)

    # Don't crossover sometimes
    if crossover_chance < random():
        return Player(strat='inherited', mem=parents[0].mem, lut=parents[0].lut), Player(strat='inherited', mem=parents[0].mem, lut=parents[0].lut)

    c1_lut = parents[0].lut[:crossover_point] + parents[1].lut[crossover_point:]
    c2_lut = parents[1].lut[:crossover_point] + parents[0].lut[crossover_point:]

    # Mutate
    for x in range(len(c1_lut)):
        if random() < mutation_chance:
            if c1_lut[x] == 'D':
                c1_lut = c1_lut[:x] + 'C' + c1_lut[x + 1:]
            else:
                c1_lut = c1_lut[:x] + 'D' + c1_lut[x + 1:]
            if c2_lut[x] == 'D':
                c2_lut = c2_lut[:x] + 'C' + c2_lut[x + 1:]
            else:
                c2_lut = c2_lut[:x] + 'D' + c2_lut[x + 1:]

    return Player(strat='inherited', mem=parents[0].mem, lut=c1_lut), Player(strat='inherited', mem=parents[0].mem, lut=c2_lut)


# Generate encoding string
def gen_encoding_string(strat):

    match strat:
        case 'tft':
            strategy = __gen_tft
        case 'tf2t':
            strategy = __gen_tf2t
        case 'stft':
            strategy = __gen_tft
        case 'all_c':
            strategy = __gen_all_c
        case 'all_d':
            strategy = __gen_all_d
        case 'random_choice':
            strategy = __gen_random_choice
        case _:
            strategy = __gen_random_choice

    s = ''
    for x in range(4):
        for y in range(4):
            for z in range(4):
                s += strategy([v[x], v[y], v[z]])
    return s


def __gen_tft(hist):

    if len(hist) == 0:
        return 'C'
    elif len(hist) == 1:
        if hist[0] == 'CD' or hist[0] == 'DD':
            return 'D'
        else:
            return 'C'
    elif len(hist) == 2:
        if hist[1] == 'CD' or hist[1] == 'DD':
            return 'D'
        else:
            return 'C'
    else:
        if hist[len(hist) - 1] == 'CD' or hist[len(hist) - 1] == 'DD':
            return 'D'
        else:
            return 'C'


def __gen_tf2t(hist):
    if len(hist) == 0:
        return 'C'
    elif len(hist) == 1:
        return 'C'
    elif len(hist) == 2:
        if (hist[0] == 'CD' or hist[0] == 'DD') and (hist[1] == 'CD' or hist[1] == 'DD'):
            return 'D'
        else:
            return 'C'
    else:
        if (hist[len(hist) - 2] == 'CD' or hist[len(hist) - 2] == 'DD') and (hist[len(hist) - 1] == 'CD' or hist[len(hist) - 1] == 'DD'):
            return 'D'
        else:
            return 'C'


def __gen_stft(hist):
    if len(hist) == 0:
        return 'D'
    elif len(hist) == 1:
        if hist[0] == 'CD' or hist[0] == 'DD':
            return 'D'
        else:
            return 'C'
    elif len(hist) == 2:
        if hist[1] == 'CD' or hist[1] == 'DD':
            return 'D'
        else:
            return 'C'
    else:
        if hist[len(hist) - 1] == 'CD' or hist[len(hist) - 1] == 'DD':
            return 'D'
        else:
            return 'C'


def __gen_all_c(_):
    return 'C'


def __gen_all_d(_):
    return 'D'


def __gen_random_choice(_):
    return "C" if randint(0, 1) == 0 else "D"
