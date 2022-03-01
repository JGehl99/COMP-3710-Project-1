from StrategyComparer.strategy_comparer import StrategyComparer

if __name__ == '__main__':
    fixed = StrategyComparer(
        n_turns=1000,
        mem=5,
        tft=True,
        tf2t=True,
        stft=True,
        all_d=True,
        all_c=True,
        avg_d=True,
        avg_c=True,
        rand=True,
        custom=[
            # Depth 1
            # Genetic Algorithm
            'CCCC',
            # Hill Climbing
            'CCCC',
            # Tabu Search
            'DCCC',

            # Depth 2
            # Genetic Algorithm
            'CCCCDDDCCCCCDCCD',
            # Hill Climbing
            'DCCCCDDDDCDDCCCC',
            # Tabu Search.
            'DCDCDDCCCCCDDDDD',

            # Depth 3
            # Genetic Algorithm
            'CDCDCDCDCCCDDDCCCDCCCCCCDDCDCCDCCCDDCCDCDCCCCCCDCCCCDCCCCCCDCCCC',
            # Hill Climbing
            'DCDDCDCCCCDDDCDDCDCDCCDDDCCDDDDDDCCCDDDDDCCCDCCCDDDDCCCCDCDCCDCC',
            # Tabu Search
            'DCDDCCDDDDDDCCCDCCDCDCDCDCCCCCCCCCCCDDCDCCCCCCDDDCDCCCDCDDCCDDCC',

            # Depth 4
            # Genetic Algorithm
            'CCCDCCCCDCCCCCDDDDCDCDCCDDDCDDDDCCCCDDCDDCCDDDCCCDDDDCCDDCCDDDDDDCCDDCCDCCCDCDCCCDCDDCCCDCCDDCCDDCDDCCCCCDDCDCCDCCDCCDDCDDCCDCCDDCDDDDCDCCCDDCDCDDCCCDCDDCCCDDCCDDDCCDCDDCCCCDCCDDDCCDCCDDCCCCCCDDCDDDDCCCCCCCCCDCCCCDDDDCCCDCCDCDCCCCCCCDCDDCCDDDCCCCDDDCCDDDDD',
            # Hill Climbing
            'DCCCDDDDCDCDDDDDDDCCDDDCCDCDCDDCDCDCDDDCDCCDCCDCDCCCCCDDCCCCCDDDDCCCDDDDCCCDDCCCCDCCDCCCCDDDCDCCDCDCCDDCDDCDDDDDCDDDCDDDDDCCDDDDCDCCCDCCDDDDDDCDDCCCDDDCCCDDDCDDCDDDDDCDCDDDCDDDDCDDDDDCCDDCCCDDDDDCCDDCCDDCDCDDDDCCDDCCDDCDCCCCDCDDDCCCDDCDCDCCDCDCCDCCCDDDCCCD',
            # Tabu Search
            'DCDDDDCCDDCDDDDDCCCCCDCDDDCDCDCCCCDCCCDCDDDCDCCDCDDDDCCDCDDDCCDDCDCCDCDDDCDDCDCDDCDDDDDDDDDCCDCCCDDDCDCCDDCDDCDCDDDDCDCCCDCCCDCDCCDDDDDDCDCDCCCCCCCCCCDDDDDCCCDCDDDCDDCCCDCDCDCCDCCDCDDDDCCCDDCDCDDCCCDDCDDCDCCDDDDCCDCDCDCDCDDDDDCDDCCCCCDDDDCCDCCCDDDCCCDCDDCC',

            # Depth 5
            # Genetic Algorithm
            'CDCCCDDDDCCCCCDCCDCCCCCDDCCCDCCDDDCDCDDDDDCDCCCCDCDDCDCDCDDCDDDCDDCDDCCCDCCCCDDDCCDCDDCDDCDDDDCDCDDDCDCCCDCDCDDCCCCDDCCDDCDDCDDDCDDDCDCCDCCCCCDCDCCDCDCDCDCCDCDDDCCDDDCDCCCCDCCCCCCCDCCCDCCDCDCCCDCCDCCCCCCCCDDCCDCCDCDCDCCDCCCDDDCCDDDCDCDCDCDCDCCCDDCDCDCDDCCCCCDCCDCDCCDCDDCDCCDDCDCCCDCCCDCCCDCCDDDCDDCCDCCDDCCDDDCCDCDDDDCDDDDCDDCDDDCCCCCCDCCCDCDCCCDCDCDCDCCCCCCDCCDDCCDDDCDDCCCDDCCDDDCDCDDDCDDDCDCDDCDCDCDDDDCCCDCDDDDCCCCDCDCCDDDDCDCDCCDCCDCCCDDCDDCDDCCCDDDDDCCDCDCCCCCDDCDDCDCDCCDDDCDCDDCCDDDDCDDCDCCCCCDCCCDDCDDCCCCCCDCCDDCCCDCCCCCDCCDCCCDCCCCCCCDCDDCCCCCCCCCDDCDDDCCDCDDCCCCDDDDCDCCCCCDCCDCDCDCCCCDDDCCCCDCDCCCDCDDDDCCCCDCDDDCDDCCDDDCCCDDCCDCDCCCDDCDCDDDCCDCCCCCDDDDDCDCCCCCDDCCCDCCDCCDDCCCDCCDDDCCDCCCCCCCDCDDDDCCCDDCCDDCDDDCCDCCDDDCCCCCDCDCCCCCCCCCDCCCCDDCDDCCDDDDCCDDDCDCCCCCCDDDCDDCCCDDDDCDCDCCDDDCDDDDCCCCCDCCCCCCDDCDCCCDCCCDDDDDDCDCCCCDCDDDDDCDCCDCDDCCDDDCCCCCCCCCCDDDDCCDCCDCCCCDDCDDCCDDCCDCCCDCCCCCDDCCDCCDDCCDCDDDDDDCDCDDDCDCDCCCCDCDCCCCCDCDCDDDCCCCCDDDDDDCDDCDCCCCDDDDDCCDCCDCDCDDDDCCDCCCDDCCDDCCDCCCDDCCCCDDCCCDD',
            # Hill Climbing
            'CCDDDDCDDDDCDCCCDDDCDDCCCDDCCDCCDDDCCCCCCDCDDCDDDDCCDDDCCDDDCCDDCDCDCCCCCCDDDDCCDDDDDCDDCDDDDDDCDDDCCCDDCDDCCCDCCCCCCDDDCCDCCDCDCCCDCDDDDDDDCCDCDDCDCCCCCDCDDDDDDDDDDCDDCCCDDCCDCCCDCDDCDCDCCDDCCCDDCCCDCCCCCCCDDDCCDCCDCDDCCCCCCCCCDDCDCCCCDCCDCDDCDCCCCCCCDDCCCCDDCDCCDDCCDDDCDCDCDDDDCDDDDCDCCDDCDCCCDDCDDDCCCCCCCDCDCDCDDCCCCDCDDCCCDDDDDDCDCDCCCCCCCDDDCDDDDDCDCCCDDDDCCCDCCDDDCCCCDDDDDDDCDDCDCDDCCCDDDDCCDCCDCCDCDCCCCCDCDCCDDCDDCCCDDCDCDCCCDCDCDDDCCDCDDCDDDDDDDCCCDDCCCDDDDCCCCDCDDCCCDDDDCDDCDCDDCDDDCCDCCCCCDDDDDCCDCCCCCDDDDDDCCCCDDCCCDDDCCDCDDDCCDCCDDDDDDDDCDDCDDDCDDCCDCCDDCCDDDCDDCCCCDDDDCDDDCCCDCDDCDDDDDDDDCCDCDDCDCDCCCDDCCCCCCCCDDDDCCDDCCCDDCCCDDDDDDDDDCCCDCCCCDCCCCCDCCCCDDDDCCDCCCDDDDDCDDDCDCCDCDCCDCDDCCDCDCCCDCCCCDCCCCDDDDDDCDCDCDDCDCCDDDDCCDCDDDDCDDDCCDCDDDCDDCCDCDDCCCCCDCDCDCDDDCDDCCDCDCCCCDDDDCCDCDDDCCDCCCCDDCCDCCDCDDDCCDCCDCCCDCCDDCDCDDCDDDCCCDDCCDDCDCCCCDDCCDDDCCCCDDCCCCDCCDDDDCCDCCCDCDCCDDDDCDDCDDCDDCDCCCCCCDCDCDDDCDCCDDCCDDCDCDDCCCDCDDCDDCDCDDCCCCDDDCCDCDDDCDDCCDCDCCDDDDDDDDCCDDCDDDCDCCCDDDCDDCCCCCCCCCDDD',
            # Tabu Search
            'DCCCCDCCDCDCCDCDDCDDCDDCDCCDDDDDCDDDCCDCDDDDCCDCDCCDDCCCCDCCDCDCCDCDDDCCCDCDDCCCCDCDCCCCDCCDCCCDCDCCDCDDDCCCCDDCDDCDCCCDDDCDCDCCCCCCCCDDCDCCCDCDDCDDCDDCDDCDCDCCDCCCDCDDCDDCCDDCCCDDDCCDDCCCCCCCDDCCDCDCDCCCDDDDDCCCDDCCDDDDCCCCDDCCDCCDDCCCCCCCCCCDDDDCDDCCDCCCCDDDCDDCDCDCCCCDCCCCCDCDDDCDCCDCDDCDCDDDDCDDDCDCCDDDCDDDDCCDCCDDDCCDCCCDCCDDDDCDDDCDCDCCCDCCCDDCCDDCCCDDDCDDDCCCCCCDDDCDDCCDDDDCDCCCDDDCCDDCDCDCCDDDDDDCCDDDCCCDDDDDCCDDDDCDCDCDCDCDCCCCCDCDCDCDCDCCCDCDCDCCDCCCDCCCCDDCCCCDDCCDCCCCDCDDDDCDDDDCDDDCDCCDDDCCCDDCCDCDDDDDCDCCCDDDDDCCCDDCDDCCCCCCCCDDCDCCDCCCCDCCCCCCDCCDCCCDCCCDDCCDDDCDCCDDCDDDDDDDDDDCCDDDCCDCCDCDCCCDDCCCCDDCCCDCCDDDCDCDCDDCDDCCCCDCDDDDDCDCDCDDDDCDCCCDCCDDCDCCDDDCDCCDDCDCDDCCCCCCDCCCDDCDCCCDDCDDCDCCDDCDDDCCCDDDDDDCDDDDDCCCDCCCCDDDDDCDCCCDCDDDDCDCCCCCDCDCDCCDCCCCDDCCCDCCDDCDDCCDCDCCCCDCCCDDDCCDDCCCCCCCDDCCDCDCDCDDDCCCDDDCDDCDDCCDCCCCCDDDDDCCDDDCDCCDDDCCDCCDCCCDCCCCCDDCCDCCCDCDCDCDCCDCDCCDCCDDCDDDDDCCDCCDDCDCCCCCDCDDCDCDCCDCDCDDDCDDCDDDCDCDCCDCCCDDCCCDDDCCCDCCDDDDCCCDDCDDCDCDCCCCDCCDCCDDDDDDCCCDCCDCDCDC'
        ],
        debug=False)
    fixed.play_strategies()
    print(fixed)
