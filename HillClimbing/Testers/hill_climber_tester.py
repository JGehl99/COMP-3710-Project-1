from HillClimbing.hill_climber import HillClimber

if __name__ == '__main__':
    climber = HillClimber(
        n_turns=64,
        mem=3,
        attempts=10,
        n_steps=10,
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
    climber.climb_hill()
    print(climber)
