from HillClimbing.hill_climber import HillClimber

if __name__ == '__main__':
    climber = HillClimber(
        n_turns=64,
        mem=3,
        attempts=10,
        n_steps=10,
        debug=True)
    climber.climb_hill()
    print(climber)
