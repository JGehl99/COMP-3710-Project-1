import math
import random
from random import randint
from GeneticAlgorithm.player import Player, v

debug = False

class Population:

    # Variables:
    # n: Number of players
    # strategy_selector: String to choose which type of strategy combo to select
    # sel_type: Holds type of selection to perform when selecting parents
    # n_parents: Holds how many parents to choose when creating offspring
    # n_children: Holds how many children should be created from n_parents
    # mutation_chance: Chance for single char to change in chromosome to reflect random mutation
    # crossover_chance: Chance for crossover to actually occur, if not, put parents back in children
    # strategy_combos: Holds list of strategy combos
    strategy_combos = ['random_strats',
                       'all_tft',
                       'even_tft_random']

    # strategy_reference: Choose random function from list if one is not supplied in params
    strategy_reference = ["tft",
                          "tf2t",
                          "stft",
                          "random_choice",
                          "all_d",
                          "all_c"]

    def __init__(self,
                 n_players=0,
                 n_turns=64,
                 strategy_selector='',
                 sel_type="tournament",
                 crossover_chance=0.99,
                 mutation_chance=0.01,
                 mem=3):

        # Set mutation chance
        self.mutation_chance = mutation_chance

        # Set crossover chance
        self.crossover_chance = crossover_chance

        # Set number of cycles
        self.n_cycles = n_turns

        match sel_type:
            case "tournament":
                self.sel_type = sel_type
            case "roulette":
                self.sel_type = sel_type
            case _:
                raise ValueError("Invalid Selection Type. Valid choices: tournament")

        # Store num Players
        self.n = n_players

        # Switch statement for type of strategy combo to use
        match strategy_selector:

            # random_strats: Choose random strategy for all Players
            case 'random_strats':
                self.players = [Player(strat=self.strategy_reference[randint(0, 5)], mem=mem) for _ in range(0, n_players)]

            # all_tft: All Players use tft strategy
            case 'all_tft':
                self.players = [Player(strat='tft') for _ in range(0, n_players, mem=mem)]

            # even_tft_random: Even split of tft and random_choice Players
            case 'even_tft_random':
                half_one = math.floor(n_players/2)
                half_two = n_players - half_one
                self.players = [Player(strat=self.strategy_reference[randint(0, 7)], mem=mem) for _ in range(0, half_one)]
                for x in range(0, half_two):
                    self.players.append(Player(strat='tft'))

            case 'random_chance':
                self.players = [Player(strat='random_choice', mem=mem) for _ in range(0, n_players)]

            # Catch all to ensure strategy_selector is valid
            case _:
                raise ValueError("Invalid Strategy Type. Valid choices: random_strats all_tft even_tft_random")

    def __str__(self):
        s = "Population n=" + str(self.n) + ":" + "\n-----------\n"
        for x in self.players:
            s = s + x.__str__() + "\n"
        return s

    # Selects 2 parents based on selection_type
    def select_parent(self):

        match self.sel_type:
            case "tournament":

                # Only choose indices where they are not the same, and where players are not using the same strat
                while True:
                    i1 = randint(0, len(self.players) - 1)
                    i2 = randint(0, len(self.players) - 1)

                    if i1 is not i2:
                        break

                if debug:
                    print("\nTournament\n------------")

                if self.players[i1].fitness <= self.players[i2].fitness:
                    if debug:
                        print(self.players[i1])
                        print(">", self.players[i2])
                    return self.players[i2]
                else:
                    if debug:
                        print(">", self.players[i1])
                        print(self.players[i2])
                    return self.players[i1]

            case "roulette":
                max_fitness = len(self.players) * self.n_cycles * v['DD']

    def selection(self):
        sel = []
        for x in range(0, 2):
            sel.append(self.select_parent())
        return sel



