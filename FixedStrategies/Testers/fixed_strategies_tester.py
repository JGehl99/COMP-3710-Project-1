from FixedStrategies.fixed_strategies import FixedStrategies

if __name__ == '__main__':
    fixed = FixedStrategies(
        n_turns=1000,
        mem=3,
        tft=True,
        tf2t=True,
        stft=True,
        all_d=True,
        all_c=True,
        random=True,
        debug=False)
    fixed.play_strategies()
    print(fixed)
