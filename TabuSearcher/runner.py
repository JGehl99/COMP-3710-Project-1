from TabuSearcher.tabu_searcher import TabuSearcher

if __name__ == '__main__':
    tabu = TabuSearcher(
        n_turns=64,
        mem=3,
        n_steps=100,
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
    tabu.perform()
    print(tabu)
