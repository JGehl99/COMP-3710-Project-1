from Looper.looper import Looper

if __name__ == '__main__':
    looper = Looper(
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
        debug=False)