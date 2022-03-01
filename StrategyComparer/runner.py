from StrategyComparer.strategy_comparer import StrategyComparer

if __name__ == '__main__':
    fixed = StrategyComparer(
        n_turns=64,
        mem=3,
        tft=True,
        tf2t=True,
        stft=True,
        all_d=True,
        all_c=True,
        avg_d=True,
        avg_c=True,
        rand=True,
        custom=[
            'CDCDCDCDCCCDDDCCCDCCCCCCDDCDCCDCCCDDCCDCDCCCCCCDCCCCDCCCCCCDCCCC',  # Sample from genetic algorithm.
            'DCDDCDCCCCDDDCDDCDCDCCDDDCCDDDDDDCCCDDDDDCCCDCCCDDDDCCCCDCDCCDCC',  # Sample from hill climbing.
            'DCDDCCDDDDDDCCCDCCDCDCDCDCCCCCCCCCCCDDCDCCCCCCDDDCDCCCDCDDCCDDCC'  # Sample from tabu search.
        ],
        debug=False)
    fixed.play_strategies()
    print(fixed)
