import math
from random import randint
from player import Player


class Population:

    # Variables:
    # n: Number of players
    # strategy_selector: String to choose which type of strategy combo to select
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

    # Mutation chance percent between 0 and 1
    m_chance = 0

    def __init__(self, n_players=0, strategy_selector='', mutate_chance_percent=0):

        # Set mutation chance
        self.m_chance = mutate_chance_percent

        # Store num Players
        self.n = n_players

        # Switch statement for type of strategy combo to use
        match strategy_selector:

            # random_strats: Choose random strategy for all Players
            case 'random_strats':
                self.players = [Player(strat=self.strategy_reference[randint(0, 5)]) for _ in range(0, n_players)]

            # all_tft: All Players use tft strategy
            case 'all_tft':
                self.players = [Player(strat='tft') for _ in range(0, n_players)]

            # even_tft_random: Even split of tft and random_choice Players
            case 'even_tft_random':
                half_one = math.floor(n_players/2)
                half_two = n_players - half_one
                self.players = [Player(strat=self.strategy_reference[randint(0, 7)]) for _ in range(0, half_one)]
                for x in range(0, half_two):
                    self.players.append(Player(strat='tft'))

            # Catch all to ensure strategy_selector is valid
            case _:
                raise ValueError("Invalid Strategy type. Valid choices: random_strats all_tft even_tft_random ")

    # Print all players in Population
    def print_players(self):
        for p in self.players:
            print("Player: ", p.strat_name, sep="")
