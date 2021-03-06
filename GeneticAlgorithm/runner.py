from GeneticAlgorithm.genetic_algorithm import GeneticAlgorithm

if __name__ == '__main__':
    genetic = GeneticAlgorithm(
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
        debug=False)
    genetic.perform()
    print(genetic)
