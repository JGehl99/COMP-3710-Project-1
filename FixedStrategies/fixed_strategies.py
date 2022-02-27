from GeneticAlgorithm.player import Player


class FixedStrategies:

    """
    n_turns: The number of turns the hill climber will play each of TFT, TF2T, STFT, ALL D, and ALL C each match.
    mem: The memory depth that the hill climber and all its opponents will have.
    debug: If print messages should be displayed.
    """
    def __init__(self, n_turns=64, mem=3, tft=True, tf2t=True, stft=True, all_d=True, all_c=True, random=True, debug=False):

        # Ensure values are valid.
        if n_turns < 1:
            n_turns = 1
        if mem < 1:
            mem = 1

        # Set parameters.
        self.n_turns = n_turns
        self.mem = mem
        self.tft = tft
        self.tf2t = tf2t
        self.stft = stft
        self.all_d = all_d
        self.all_c = all_c
        self.random = random
        self.score_tft = None
        self.score_tf2t = None
        self.score_stft = None
        self.score_all_d = None
        self.score_all_c = None
        self.score_random = None
        self.debug = debug

    """
    Get the results for all fixed strategies.
    """
    def __str__(self):
        s = f'Fixed strategies with {self.n_turns} turns and memory depth {self.mem}:\n'
        if self.score_tft is not None:
            s += f'TFT    | {self.score_tft}\n'
        if self.score_tf2t is not None:
            s += f'TF2T   | {self.score_tf2t}\n'
        if self.score_stft is not None:
            s += f'STFT   | {self.score_stft}\n'
        if self.score_all_d is not None:
            s += f'All D  | {self.score_all_d}\n'
        if self.score_all_c is not None:
            s += f'All C  | {self.score_all_c}\n'
        if self.score_random is not None:
            s += f'Random | {self.score_random}\n'
        return s

    """
    Test fixed strategies.
    """
    def play_strategies(self):

        # Reset parameters from the last attempt.
        self.score_tft = None
        self.score_tf2t = None
        self.score_stft = None
        self.score_all_d = None
        self.score_all_c = None
        self.score_random = None

        # Loop through every fixed strategy, skipping it if it should not be tested in this comparison.
        for p1_index in range(0, 6):
            if p1_index == 0:
                if not self.tft:
                    continue
                p1_strategy = 'tft'
            elif p1_index == 1:
                if not self.tf2t:
                    continue
                p1_strategy = 'tf2t'
            elif p1_index == 2:
                if not self.stft:
                    continue
                p1_strategy = 'stft'
            elif p1_index == 3:
                if not self.all_d:
                    continue
                p1_strategy = 'all_d'
            elif p1_index == 4:
                if not self.all_c:
                    continue
                p1_strategy = 'all_c'
            else:
                if not self.random:
                    continue
                p1_strategy = 'random_choice'

            # Loop through all opponent types once again skipping it if it should not be tested in this comparison.
            score = 0
            dividend = 0
            for p2_index in range(0, 6):
                if p2_index == 0:
                    if not self.tft:
                        continue
                    p2_strategy = 'tft'
                elif p2_index == 1:
                    if not self.tf2t:
                        continue
                    p2_strategy = 'tf2t'
                elif p2_index == 2:
                    if not self.stft:
                        continue
                    p2_strategy = 'stft'
                elif p2_index == 3:
                    if not self.all_d:
                        continue
                    p2_strategy = 'all_d'
                elif p2_index == 4:
                    if not self.all_c:
                        continue
                    p2_strategy = 'all_c'
                else:
                    if not self.random:
                        continue
                    p2_strategy = 'random_choice'
                dividend += 1

                # Setup new players every time so they are not impacted by previous histories.
                p1 = Player(strat=p1_strategy, mem=self.mem)
                p2 = Player(strat=p2_strategy, mem=self.mem)

                # Play the given number of turns.
                for turn in range(0, self.n_turns):
                    p1_move = p1.strategy()
                    p2_move = p2.strategy()
                    p1_result = p1_move + p2_move
                    p2_result = p2_move + p1_move
                    p1.update_history(p1_result)
                    p2.update_history(p2_result)

                    # Add scores based on the results.
                    if p1_result == 'CC':
                        p1.fitness += 3
                        p2.fitness += 3
                    elif p1_result == 'CD':
                        p1.fitness += 0
                        p2.fitness += 5
                    elif p1_result == 'DC':
                        p1.fitness += 5
                        p2.fitness += 0
                    else:
                        p1.fitness += 1
                        p2.fitness += 1

                # Add up the cumulative score.
                score += p1.fitness
                if self.debug:
                    print(f'{p1_strategy}: {p1.fitness / self.n_turns}\t| {p2_strategy}: {p2.fitness / self.n_turns}\t| Average: {(p1.fitness / self.n_turns + p2.fitness / self.n_turns) / 2}')

            # Get the average based on how many types are being tested.
            score /= dividend

            # Get the average relative to the number of turns that were in the match.
            score /= self.n_turns

            # Apply the score to the correct parameter.
            if p1_index == 0:
                self.score_tft = score
            elif p1_index == 1:
                self.score_tf2t = score
            elif p1_index == 2:
                self.score_stft = score
            elif p1_index == 3:
                self.score_all_d = score
            elif p1_index == 4:
                self.score_all_c = score
            else:
                self.score_random = score
