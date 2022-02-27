import random
from GeneticAlgorithm.player import Player

# 4 values to represent Reward, Sucker, Temptation, and Penalty game outcomes
v = {"CC": 2, "DC": 0, "CD": 3, "DD": 1, 2: "CC", 0: "DC", 3: "CD", 1: "DD"}


class HillClimber:

    """
    n_turns: The number of turns the hill climber will play each of TFT, TF2T, STFT, ALL D, and ALL C each match.
    mem: The memory depth that the hill climber and all its opponents will have.
    attempts: The number of random starting attempts the hill climbing algorithm will attempt to avoid local maxima.
    n_steps: The number of side steps a hill climber may take when reaching a plateau before giving up.
    debug: If print messages should be displayed.
    """
    def __init__(self, n_turns=64, mem=3, attempts=1, n_steps=0, debug=False):

        # Ensure values are valid.
        if n_turns < 1:
            n_turns = 1
        if attempts < 1:
            attempts = 1
        if mem < 1:
            mem = 1
        if n_steps < 0:
            n_steps = 0

        # Set parameters.
        self.n_turns = n_turns
        self.mem = mem
        self.attempts = attempts
        self.n_steps = n_steps
        self.top_player = None
        self.previous_luts = []
        self.debug = debug

    """
    Get the result of the hill climbing.
    """
    def __str__(self):

        # Give a message if the hill climbing has not yet been performed.
        if self.top_player is None:
            return 'Hill climbing has not yet been performed.'
        return 'Hill climbing result: ' + self.top_player.lut + ' | Average score: ' + str(self.top_player.fitness);

    """
    Perform hill climbing.
    """
    def climb_hill(self):

        # Reset parameters from any previous hill climbs.
        self.top_player = None
        self.previous_luts = []

        # Loop for the given attempts.
        for attempt in range(0, self.attempts):

            # Reset parameters from the last attempt.
            starting_lut = ''
            top_lut = None
            side_steps = 0
            score = 0
            attempt_score = 0
            generation_player = None

            # Generate a random starting LUT.
            for x in range(0, (4 ** self.mem)):
                starting_lut += "C" if random.randint(0, 1) == 0 else "D"
            if self.debug:
                print('Attempt ' + str(attempt + 1) + ' of ' + str(self.attempts) + '\t|Starting LUT: ' + starting_lut)

            # Loop so long as we have an increasing score, or we have side steps remaining.
            keep_climbing = True
            while keep_climbing:

                # Until we find a better score, assume this hill climb should end.
                keep_climbing = False

                # Test every possible variation of the current LUT.
                # For instance, if the LUT was CCCC...
                # We test CCCC..., DCCC..., CDCC..., CCDC..., CCCD... in search of one with a new greater score.
                for i in range(-1, len(starting_lut)):

                    # If this is not the first step in this hill climb,
                    # start with the best variation of the previous step.
                    # Otherwise, start with simply the randomly generated LUT previously generated as this is the start
                    # of the hill climbing.
                    if top_lut is not None:
                        member_lut = top_lut
                    else:
                        member_lut = starting_lut

                    # This is where we create the current variation.
                    # If the iteration is -1, don't make any changes as it needs to be tested as well.
                    # Otherwise, swap the decision in the LUT at the current index.
                    if i > -1:
                        if member_lut[i] == 'C':
                            member_lut = member_lut[:i] + 'D' + member_lut[i + 1:]
                        else:
                            member_lut = member_lut[:i] + 'C' + member_lut[i + 1:]

                    # If this LUT was already tested, simply continue to the next one to not waste time.
                    if member_lut in self.previous_luts:
                        if self.debug:
                            print('Attempt ' + str(attempt + 1) + ' of ' + str(self.attempts) + ' member ' + str( i + 2) + ' of ' + str(len(starting_lut) + 1) + '\t| LUT: ' + member_lut + ' already tested.')
                        continue

                    # Add this LUT to the list of all previously tested LUTs, so we do not waste time in the future.
                    self.previous_luts.append(member_lut)

                    if self.debug:
                        print('Attempt ' + str(attempt + 1) + ' of ' + str(self.attempts) + ' member ' + str(i + 2) + ' of ' + str(len(starting_lut) + 1) + '\t| LUT: ' + member_lut)

                    # Face off against every type of pre-defined strategy.
                    score = 0
                    for opponent in range(0, 5):
                        if opponent == 0:
                            strategy = 'tft'
                        elif opponent == 1:
                            strategy = 'tf2t'
                        elif opponent == 2:
                            strategy = 'stft'
                        elif opponent == 3:
                            strategy = 'all_d'
                        else:
                            strategy = 'all_c'

                        # Set up the players.
                        # Reset the hill climber every time, so it is not impacted by the history of its last match.
                        hill_climber = Player(strat='inherited', lut=member_lut, mem=self.mem)
                        other_player = Player(strat=strategy, mem=self.mem)

                        # Play the given number of turns.
                        for turn in range(0, self.n_turns):
                            hill_climber_move = hill_climber.strategy()
                            other_player_move = other_player.strategy()
                            hill_climber_result = hill_climber_move + other_player_move
                            other_player_result = other_player_move + hill_climber_move
                            hill_climber.update_history(hill_climber_result)
                            other_player.update_history(other_player_result)
                            hill_climber.fitness += v[hill_climber_result]

                        # Add up the cumulative score against all different opponents.
                        score += hill_climber.fitness
                        if self.debug:
                            print('Attempt ' + str(attempt + 1) + ' of ' + str(self.attempts) + ' member ' + str(i + 2) + ' of ' + str(len(starting_lut) + 1) + '\t| ' + strategy + '\t| Score: ' + str(hill_climber.fitness) + '\t| Cumulative Score: ' + str(score))

                    # After having played all opponents, get the average score against all of them.
                    score /= 5
                    if self.debug:
                        print('Attempt ' + str(attempt + 1) + ' of ' + str(self.attempts) + ' member ' + str(i + 2) + ' of ' + str(len(starting_lut) + 1) + '\t| Average Score: ' + str(score))

                    # If this score is the best of this current attempt, confirm to keep climbing and store values.
                    if score > attempt_score:
                        keep_climbing = True
                        attempt_score = score
                        side_steps = 0
                        generation_player = Player(strat='inherited', lut=member_lut, mem=self.mem)
                        generation_player.fitness = score
                        if self.debug:
                            print('Attempt ' + str(attempt + 1) + ' of ' + str(self.attempts) + ' member ' + str(i + 2) + ' of ' + str(len(starting_lut) + 1) + '\t| Score ' + str(score) + ' > Best Attempt Score')

                    # Otherwise, if the score was equal to the best attempt score so far, count this as a side step.
                    # If we have enough valid side steps, count this as a promising potential approach and thus to
                    # keep climbing.
                    elif score == attempt_score:
                        side_steps += 1
                        if side_steps < self.n_steps:
                            keep_climbing = True
                        if self.debug:
                            print('Attempt ' + str(attempt + 1) + ' of ' + str(self.attempts) + ' member ' + str(i + 2) + ' of ' + str(len(starting_lut) + 1) + '\t| Score ' + str(score) + ' == Best Attempt Score ' + str(attempt_score))

                    # Otherwise, this score was less than the best attempt score.
                    else:
                        if self.debug:
                            print('Attempt ' + str(attempt + 1) + ' of ' + str(self.attempts) + ' member ' + str(i + 2) + ' of ' + str(len(starting_lut) + 1) + '\t| Score ' + str(score) + ' < Best Attempt Score ' + str(attempt_score))

                    # If the new score is the best overall score, store it.
                    if self.top_player is None or score > self.top_player.fitness:
                        self.top_player = Player(strat='inherited', lut=starting_lut, mem=self.mem)
                        self.top_player.fitness = score
                        if self.debug:
                            print('Attempt ' + str(attempt + 1) + ' of ' + str(self.attempts) + ' member ' + str(i + 2) + ' of ' + str(len(starting_lut) + 1) + '\t| Best Overall Score: ' + str(score))
                    elif self.debug:
                        print('Attempt ' + str(attempt + 1) + ' of ' + str(self.attempts) + ' member ' + str(i + 2) + ' of ' + str(len(starting_lut) + 1) + '\t| Score ' + str(score) + ' <= Best Overall Score ' + str(self.top_player.fitness))

                # Store the top LUT for this climbing attempt to start at on the next iteration.
                top_lut = generation_player.lut
