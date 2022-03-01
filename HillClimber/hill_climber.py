import random
import time

from player import Player


class HillClimber:

    """
    n_turns: The number of turns the hill climber will play all other strategies.
    mem: The memory depth that the hill climber and all its opponents will have.
    attempts: The number of random starting attempts the hill climbing algorithm will attempt to avoid local maxima.
    n_steps: The number of side steps a hill climber may take when reaching a plateau before giving up.
    tft: If tit-for-tat should be performed.
    tf2t: If tit-for-2-tat should be performed.
    stft: If suspicious-tit-for-tat should be performed.
    all_d: If only defect should be performed.
    all_c: If only cooperate should be performed.
    avg_d: If average leaning towards defect should be performed.
    avg_c: If average leaning towards cooperate should be performed.
    rand: If random should be performed.
    custom: List of any custom lookup tables to perform.
    debug: If print messages should be displayed.
    """
    def __init__(
            self,
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
            debug=False):

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
        self.elapsed_time = 0
        self.previous_luts = []
        self.tft = tft
        self.tf2t = tf2t
        self.stft = stft
        self.all_d = all_d
        self.all_c = all_c
        self.avg_d = avg_d
        self.avg_c = avg_c
        self.rand = rand
        self.custom = custom
        self.debug = debug

    """
    Get the result of the hill climbing.
    """
    def __str__(self):

        # Give a message if the hill climbing has not yet been performed.
        if self.top_player is None:
            return 'Hill climbing has not yet been performed.'
        return f'Hill Climb\t| Memory: {self.mem}\t| Time: {self.elapsed_time}\t| Score: {self.top_player.fitness}\t| LUT: {self.top_player.lut}'

    """
    Perform hill climbing.
    """
    def perform(self):

        # Reset parameters from any previous hill climbs.
        self.top_player = None
        self.previous_luts = []

        # Start the timer.
        start_time = time.time()

        # The number of players there are.
        loops = 9
        if self.custom is not None:
            loops += len(self.custom)

        # Loop for the given attempts.
        for attempt in range(0, self.attempts):

            # Reset parameters from the last attempt.
            starting_lut = ''
            top_lut = None
            side_steps = 0
            attempt_score = 0
            generation_player = None

            # Generate a random starting LUT.
            for x in range(0, (4 ** self.mem)):
                starting_lut += "C" if random.randint(0, 1) == 0 else "D"
            if self.debug:
                print(f'Attempt {attempt + 1} of {self.attempts}\t| Starting LUT {starting_lut}')

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
                            print(f'Attempt {attempt + 1} of {self.attempts} member {i + 2} of {len(starting_lut) + 1}\t| LUT: {member_lut} already tested.')
                        continue

                    # Add this LUT to the list of all previously tested LUTs, so we do not waste time in the future.
                    self.previous_luts.append(member_lut)

                    if self.debug:
                        print(f'Attempt {attempt + 1} of {self.attempts} member {i + 2} of {len(starting_lut) + 1}\t| LUT: {member_lut}')

                    # Face off against every type of pre-defined strategy.
                    score = 0
                    dividend = 0
                    for opponent in range(0, loops):
                        if opponent == 0:
                            if not self.tft:
                                continue
                            strategy = 'tft'
                        elif opponent == 1:
                            if not self.tf2t:
                                continue
                            strategy = 'tf2t'
                        elif opponent == 2:
                            if not self.stft:
                                continue
                            strategy = 'stft'
                        elif opponent == 3:
                            if not self.all_d:
                                continue
                            strategy = 'all_d'
                        elif opponent == 4:
                            if not self.all_c:
                                continue
                            strategy = 'all_c'
                        elif opponent == 5:
                            if not self.avg_d:
                                continue
                            strategy = 'avg_d'
                        elif opponent == 6:
                            if not self.avg_c:
                                continue
                            strategy = 'avg_c'
                        elif opponent == 7:
                            if not self.rand:
                                continue
                            strategy = 'random_choice'
                        elif opponent == 8:
                            strategy = 'self'
                        else:
                            if len(self.custom[opponent - 8]) != 4 ** self.mem:
                                continue
                            strategy = 'cust'
                            opponent_lut = self.custom[opponent - 8]

                        # Since we have competed against yet another opponent, increment the dividend for getting the average.
                        dividend += 1

                        # Set up the players.
                        # Reset the hill climber every time, so it is not impacted by the history of its last match.
                        hill_climber = Player(strat='inherited', lut=member_lut, mem=self.mem)
                        if strategy == 'self':
                            other_player = Player(strat='inherited', lut=member_lut, mem=self.mem)
                        elif strategy == 'cust':
                            other_player = Player(start='inherited', lut=opponent_lut, mem=self.mem)
                        else:
                            other_player = Player(strat=strategy, mem=self.mem)

                        # Play the given number of turns.
                        for turn in range(0, self.n_turns):
                            hill_climber_move = hill_climber.strategy()
                            other_player_move = other_player.strategy()
                            hill_climber_result = hill_climber_move + other_player_move
                            other_player_result = other_player_move + hill_climber_move
                            hill_climber.update_history(hill_climber_result)
                            other_player.update_history(other_player_result)

                            # Add scores based on the results.
                            if hill_climber_result == 'CC':
                                hill_climber.fitness += 3
                            elif hill_climber_result == 'CD':
                                hill_climber.fitness += 0
                            elif hill_climber_result == 'DC':
                                hill_climber.fitness += 5
                            else:
                                hill_climber.fitness += 1

                        # Add up the cumulative score against all different opponents.
                        score += hill_climber.fitness
                        if self.debug:
                            print(f'Attempt {attempt + 1} of {self.attempts} member {i + 2} of {len(starting_lut) + 1}\t| {strategy}\t| Score: {hill_climber.fitness}\t| Cumulative: {score}')

                    # After having played all opponents, get the average score against all of them.
                    score /= dividend
                    if self.debug:
                        print(f'Attempt {attempt + 1} of {self.attempts} member {i + 2} of {len(starting_lut) + 1}\t| Average Score for {self.n_turns} Turns: {score}')

                    # Get the average score per how many turns there were.
                    score /= self.n_turns
                    if self.debug:
                        print(f'Attempt {attempt + 1} of {self.attempts} member {i + 2} of {len(starting_lut) + 1}\t| Average Score: {score}')

                    # If this score is the best of this current attempt, confirm to keep climbing and store values.
                    if generation_player is None or score > attempt_score:
                        keep_climbing = True
                        attempt_score = score
                        side_steps = 0
                        generation_player = Player(strat='inherited', lut=member_lut, mem=self.mem)
                        generation_player.fitness = score
                        if self.debug:
                            print(f'Attempt {attempt + 1} of {self.attempts} member {i + 2} of {len(starting_lut) + 1}\t| Average Score {score} > Best Attempt Score')

                    # Otherwise, if the score was equal to the best attempt score so far, count this as a side step.
                    # If we have enough valid side steps, count this as a promising potential approach and thus to
                    # keep climbing.
                    elif score == attempt_score:
                        if not keep_climbing:
                            side_steps += 1
                            if side_steps < self.n_steps:
                                keep_climbing = True
                        if self.debug:
                            print(f'Attempt {attempt + 1} of {self.attempts} member {i + 2} of {len(starting_lut) + 1}\t| Average Score {score} == Best Attempt Score {attempt_score} | Steps: {side_steps} / {self.n_steps}')

                    # Otherwise, this score was less than the best attempt score.
                    else:
                        if self.debug:
                            print(f'Attempt {attempt + 1} of {self.attempts} member {i + 2} of {len(starting_lut) + 1}\t| Average Score {score} < Best Attempt Score {attempt_score}')

                    # If the new score is the best overall score, store it.
                    if self.top_player is None or score > self.top_player.fitness:
                        self.top_player = Player(strat='inherited', lut=starting_lut, mem=self.mem)
                        self.top_player.fitness = score
                        if self.debug:
                            print(f'Attempt {attempt + 1} of {self.attempts} member {i + 2} of {len(starting_lut) + 1}\t| Best Overall Score: {score}')
                    elif self.debug:
                        print(f'Attempt {attempt + 1} of {self.attempts} member {i + 2} of {len(starting_lut) + 1}\t| Average Score {score} <= Best Overall Score {self.top_player.fitness}')

                # Store the top LUT for this climbing attempt to start at on the next iteration.
                if generation_player is not None:
                    top_lut = generation_player.lut
                else:
                    top_lut = starting_lut

        # Get the elapsed time.
        end_time = time.time()
        self.elapsed_time = end_time - start_time
