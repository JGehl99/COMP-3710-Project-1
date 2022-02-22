from GeneticAlgorithm.population import Population
from GeneticAlgorithm.utils import play_cycle

if __name__ == '__main__':

    pop = Population(n_players=5, strategy_selector='random_strats')

    play_cycle(pop)

    print(pop.players[0].fitness, "\t", pop.players[1].fitness)
