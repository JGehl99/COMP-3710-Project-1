import time
from random import random, randint
from player import Player


class GeneticAlgorithm:

    """
    n_turns: The number of turns the genetic algorithm will play all other strategies.
    mem: The memory depth that the hill climber and all its opponents will have.
    n_players: The number of agents in the genetic algorithm player pool.
    n_generations: The number of generations in the genetic algorithm there will be.
    mutation_chance: The chance any genome of the genetic algorithm count mutate.
    n_elites: The number of elites in the genetic algorithm.
    tft: If tit-for-tat should be performed.
    tf2t: If tit-for-2-tat should be performed.
    stft: If suspicious-tit-for-tat should be performed.
    all_d: If only defect should be performed.
    all_c: If only cooperate should be performed.
    avg_d: If average leaning towards defect should be performed.
    avg_c: If average leaning towards cooperate should be performed.
    rand: If random should be performed.
    custom: List of any custom lookup tables to perform.
    debug: If print messages should be displayed.
    """
    def __init__(
            self,
            n_turns=64,
            mem=3,
            n_players=50,
            n_generations=1000,
            mutation_chance=0.01,
            n_elites=5,
            tft=True,
            tf2t=True,
            stft=True,
            all_d=True,
            all_c=True,
            avg_d=True,
            avg_c=True,
            rand=True,
            custom=[],
            debug=False):

        # Ensure values are valid.
        if n_turns < 1:
            n_turns = 1
        if mem < 1:
            mem = 1
        if n_players < 2:
            n_players = 2
        if n_generations < 1:
            n_generations = 1
        if mutation_chance < 0:
            mutation_chance = 0
        if n_elites < 0:
            n_elites = 0
        elif n_elites >= n_players:
            n_elites = n_players - 1

        # Set parameters.
        self.n_turns = n_turns
        self.mem = mem
        self.n_players = n_players
        self.n_generations = n_generations
        self.mutation_chance = mutation_chance
        self.n_elites = n_elites
        self.top_player = None
        self.elapsed_time = 0
        self.tft = tft
        self.tf2t = tf2t
        self.stft = stft
        self.all_d = all_d
        self.all_c = all_c
        self.avg_d = avg_d
        self.avg_c = avg_c
        self.rand = rand
        self.custom = custom
        self.debug = debug

    """
    Get the result of the genetic algorithm.
    """
    def __str__(self):

        # Give a message if the genetic algorithm has not yet been performed.
        if self.top_player is None:
            return 'Genetic algorithm has not yet been performed.'
        return f'Genetic Algorithm\t| Memory: {self.mem}\t| Time: {self.elapsed_time}\t| Score: {self.top_player.fitness}\t| LUT: {self.top_player.lut}'

    """
    Perform tabu searcher.
    """
    def perform(self):

        # Reset parameters from any previous genetic algorithms.
        self.top_player = None

        # Start the timer.
        start_time = time.time()

        # The number of opponents there are.
        loops = 9
        if self.custom is not None:
            loops += len(self.custom)

        # Randomly generate the initial starting lookup tables.
        players = []
        for i in range(0, self.n_players):
            starting_lut = ''
            for x in range(0, (4 ** self.mem)):
                starting_lut += "C" if randint(0, 1) == 0 else "D"
            if self.debug:
                print(f'Starting LUT {i + 1} of {self.n_players}: {starting_lut}')
            players.append(Player(strat='inherited', lut=starting_lut, mem=self.mem))

        # Loop for the given number of generations.
        for generation in range(0, self.n_generations):

            # Loop through all players in the genetic algorithm pool.
            for i in range(0, self.n_players):

                # Reset player fitness so it is not carried over from past rounds.
                players[i].fitness = 0

                # Face off against every type of pre-defined strategy.
                dividend = 0
                for opponent in range(0, loops):
                    if opponent == 0:
                        if not self.tft:
                            continue
                        strategy = 'tft'
                    elif opponent == 1:
                        if not self.tf2t:
                            continue
                        strategy = 'tf2t'
                    elif opponent == 2:
                        if not self.stft:
                            continue
                        strategy = 'stft'
                    elif opponent == 3:
                        if not self.all_d:
                            continue
                        strategy = 'all_d'
                    elif opponent == 4:
                        if not self.all_c:
                            continue
                        strategy = 'all_c'
                    elif opponent == 5:
                        if not self.avg_d:
                            continue
                        strategy = 'avg_d'
                    elif opponent == 6:
                        if not self.avg_c:
                            continue
                        strategy = 'avg_c'
                    elif opponent == 7:
                        if not self.rand:
                            continue
                        strategy = 'random_choice'
                    elif opponent == 8:
                        strategy = 'self'
                    else:
                        if len(self.custom[opponent - 8]) != 4 ** self.mem:
                            continue
                        strategy = 'cust'
                        opponent_lut = self.custom[opponent - 8]

                    # Since we have competed against yet another opponent, increment the dividend for getting the average.
                    dividend += 1

                    # Set up the players.
                    # Reset the genetic algorithm history every time, so it is not impacted by the history of its last match.
                    players[i].hist = [] * self.mem
                    if strategy == 'self':
                        other_player = Player(strat='inherited', lut=players[i].lut, mem=self.mem)
                    elif strategy == 'cust':
                        other_player = Player(start='inherited', lut=opponent_lut, mem=self.mem)
                    else:
                        other_player = Player(strat=strategy, mem=self.mem)

                    # Play the given number of turns.
                    for turn in range(0, self.n_turns):
                        genetic_algo_move = players[i].strategy()
                        other_player_move = other_player.strategy()
                        genetic_algo_result = genetic_algo_move + other_player_move
                        other_player_result = other_player_move + genetic_algo_move
                        players[i].update_history(genetic_algo_result)
                        other_player.update_history(other_player_result)

                        # Add scores based on the results.
                        if genetic_algo_result == 'CC':
                            players[i].fitness += 3
                        elif genetic_algo_result == 'CD':
                            players[i].fitness += 0
                        elif genetic_algo_result == 'DC':
                            players[i].fitness += 5
                        else:
                            players[i].fitness += 1

                # After having played all opponents, get the average score against all of them.
                players[i].fitness /= dividend

                # Get the average score per how many turns there were.
                players[i].fitness /= self.n_turns

                # If this is the best attempt of this loop through set it as its best player.
                if self.top_player is None or players[i].fitness > self.top_player.fitness:
                    self.top_player = Player(strat='inherited', lut=players[i].lut, mem=self.mem)
                    self.top_player.fitness = players[i].fitness
                    if self.debug:
                        print(f'Generation {generation + 1} of {self.n_generations} player {i + 1} of {self.n_players}\t| Score: {players[i].fitness} is new Best Score')
                elif self.debug:
                    print(f'Generation {generation + 1} of {self.n_generations} player {i + 1} of {self.n_players}\t| Score: {players[i].fitness} <= Best Score {self.top_player.fitness}')

            # Sort players by best fitness.
            players.sort(key=lambda p: p.fitness, reverse=True)
            if self.debug:
                print(f'Generation {generation + 1} of {self.n_generations} Results:')
                for i in range(0, self.n_players):
                    elite = ' | Elite' if i < self.n_elites else ''
                    print(f'Player {i + 1} of {self.n_players}\t| Score: {players[i].fitness}\t| LUT: {players[i].lut}{elite}')

            # Make a copy of the players so the crossover works off of these previous lookup tables.
            last_gen = players.copy()

            # Go through all players, skipping the "elites" which will remain untouched in the next generation.
            for i in range(self.n_elites, self.n_players):

                # Determine the crossover point.
                crossover_point = randint(0, len(last_gen[i].lut) - 1)

                # Get the index of the other parent to crossover with which cannot be the same index.
                j = i
                while j == i:
                    j = randint(0, self.n_players - 1)

                # Crossover the lookup table.
                players[i].lut = last_gen[i].lut[:crossover_point] + last_gen[j].lut[crossover_point:]

                # Have a chance to apply random mutations.
                for x in range(len(players[i].lut)):
                    if random() < self.mutation_chance:
                        if players[i].lut[x] == 'D':
                            players[i].lut = players[i].lut[:x] + 'C' + players[i].lut[x + 1:]
                        else:
                            players[i].lut = players[i].lut[:x] + 'D' + players[i].lut[x + 1:]

        # Get the elapsed time.
        end_time = time.time()
        self.elapsed_time = end_time - start_time
