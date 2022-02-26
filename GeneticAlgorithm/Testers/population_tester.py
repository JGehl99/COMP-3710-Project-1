from GeneticAlgorithm.population import Population
from GeneticAlgorithm.utils import play_cycle, crossover

debug = False

if __name__ == '__main__':

    pop = Population(n_players=20,
                     n_turns=64,
                     strategy_selector='random_strats',
                     sel_type="tournament",
                     crossover_chance=0.99,
                     mutation_chance=0.01,
                     mem=3)
    n_gens = 200

    for x in range(0, n_gens):

        if debug:
            print("\n-----------------------------------------")
            print("Generation", x + 1)
            print("-----------------------------------------")

        children = []

        play_cycle(pop)

        if debug:
            print(pop)

        while len(children) < len(pop.players):

            candidate_parents = pop.selection()

            if debug:
                print("\nCandidate Parents: \n------------------")
                [print(x) for x in candidate_parents]

            new_children = crossover(candidate_parents, pop.mutation_chance, pop.crossover_chance)

            if debug:
                print("\nNew Children: \n----------------")
            for y in new_children:
                if debug:
                    print(y)
                children.append(y)

        if debug:
            print("\nChildren: \n----------------")
            [print(z) for z in children]

        pop.players = children

    print("\n\n\nFinal Generation:", n_gens, "\n---------------")
    play_cycle(pop)
    [print(x) for x in pop.players]



