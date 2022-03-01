from GeneticAlgorithm.genetic_algorithm import GeneticAlgorithm
from HillClimber.hill_climber import HillClimber
from TabuSearcher.tabu_searcher import TabuSearcher


class Looper:

    """
    n_turns: The number of turns each strategy will play each other.
    mem_start: The memory depth that each strategy and all its opponents will start at.
    mem_end: The memory depth that each strategy and all its opponents will end at.
    n_players: The number of agents in the genetic algorithm player pool.
    n_generations: The number of generations in the genetic algorithm there will be.
    mutation_chance: The chance any genome of the genetic algorithm count mutate.
    n_elites: The number of elites in the genetic algorithm.
    attempts: The number of random starting attempts the hill climbing algorithm will attempt to avoid local maxima.
    n_side_steps: The number of side steps a hill climber may take when reaching a plateau before giving up.
    n_tabu_steps: The number of steps the tabu searcher can take.
    n_tabu_size: How many lookup tables can be in the tabu list with a size of zero meaning unlimited.
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
            mem_start=1,
            mem_end=5,
            n_players=50,
            n_generations=1000,
            mutation_chance=0.01,
            n_elites=5,
            attempts=10,
            n_side_steps=10,
            n_tabu_steps=100,
            n_tabu_size=100,
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
        if mem_start < 1:
            mem_start = 1
        if mem_end < mem_start:
            mem_end = mem_start
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
        if attempts < 1:
            attempts = 1
        if n_side_steps < 0:
            n_side_steps = 0
        if n_tabu_steps < 1:
            n_tabu_steps = 1
        if n_tabu_size < 0:
            n_tabu_size = 0

        for mem in range(mem_start, mem_end + 1):
            genetic = GeneticAlgorithm(
                n_turns=n_turns,
                mem=mem,
                n_players=n_players,
                n_generations=n_generations,
                mutation_chance=mutation_chance,
                n_elites=n_elites,
                tft=tft,
                tf2t=tf2t,
                stft=stft,
                all_d=all_d,
                all_c=all_c,
                avg_d=avg_d,
                avg_c=avg_c,
                rand=rand,
                custom=custom,
                debug=debug)
            genetic.perform()
            print(genetic)

        for mem in range(mem_start, mem_end + 1):
            climber = HillClimber(
                n_turns=n_turns,
                mem=mem,
                attempts=attempts,
                n_steps=n_side_steps,
                tft=tft,
                tf2t=tf2t,
                stft=stft,
                all_d=all_d,
                all_c=all_c,
                avg_d=avg_d,
                avg_c=avg_c,
                rand=rand,
                custom=custom,
                debug=debug)
            climber.perform()
            print(climber)

        for mem in range(mem_start, mem_end + 1):
            tabu = TabuSearcher(
                n_turns=n_turns,
                mem=mem,
                n_steps=n_tabu_steps,
                n_tabu_size=n_tabu_size,
                tft=tft,
                tf2t=tf2t,
                stft=stft,
                all_d=all_d,
                all_c=all_c,
                avg_d=avg_d,
                avg_c=avg_c,
                rand=rand,
                custom=custom,
                debug=debug)
            tabu.perform()
            print(tabu)
