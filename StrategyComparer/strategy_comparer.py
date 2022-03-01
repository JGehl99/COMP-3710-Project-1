from player import Player


class StrategyComparer:

    """
    n_turns: The number of turns each strategy will place each other.
    mem: The memory depth that each strategy and all its opponents will have.
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
            decimal_spaces=3,
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
        if mem < 1:
            mem = 1

        # Set parameters.
        self.n_turns = n_turns
        self.mem = mem
        self.decimal_spaces = decimal_spaces
        self.tft = tft
        self.tf2t = tf2t
        self.stft = stft
        self.all_d = all_d
        self.all_c = all_c
        self.avg_d = avg_d
        self.avg_c = avg_c
        self.rand = rand
        self.custom = custom
        self.score_tft = None
        self.score_tf2t = None
        self.score_stft = None
        self.score_all_d = None
        self.score_all_c = None
        self.score_avg_d = None
        self.score_avg_c = None
        self.score_random = None
        self.score_custom = []
        self.debug = debug

    """
    Get the results for all strategies.
    """
    def __str__(self):
        s = f'Results with {self.n_turns} turns and memory depth {self.mem}:\n'
        if self.score_tft is not None:
            n = self.score_tft if self.decimal_spaces < 0 else round(self.score_tft, self.decimal_spaces)
            s += f'TFT   | {n}\n'
        if self.score_tf2t is not None:
            n = self.score_tf2t if self.decimal_spaces < 0 else round(self.score_tf2t, self.decimal_spaces)
            s += f'TF2T  | {n}\n'
        if self.score_stft is not None:
            n = self.score_stft if self.decimal_spaces < 0 else round(self.score_stft, self.decimal_spaces)
            s += f'STFT  | {n}\n'
        if self.score_all_d is not None:
            n = self.score_all_d if self.decimal_spaces < 0 else round(self.score_all_d, self.decimal_spaces)
            s += f'ALL D | {n}\n'
        if self.score_all_c is not None:
            n = self.score_all_c if self.decimal_spaces < 0 else round(self.score_all_c, self.decimal_spaces)
            s += f'ALL C | {n}\n'
        if self.score_avg_d is not None:
            n = self.score_avg_d if self.decimal_spaces < 0 else round(self.score_avg_d, self.decimal_spaces)
            s += f'AVG D | {n}\n'
        if self.score_avg_c is not None:
            n = self.score_avg_c if self.decimal_spaces < 0 else round(self.score_avg_c, self.decimal_spaces)
            s += f'AVG C | {n}\n'
        if self.score_random is not None:
            n = self.score_random if self.decimal_spaces < 0 else round(self.score_random, self.decimal_spaces)
            s += f'RAND  | {n}\n'
        num = 1
        for score_custom in self.score_custom:
            n = score_custom if self.decimal_spaces < 0 else round(score_custom, self.decimal_spaces)
            s += f'C{num}    | {n}\n'
            num += 1
        return s

    """
    Run all strategies.
    """
    def perform(self):

        # Reset parameters from the last attempt.
        self.score_tft = None
        self.score_tf2t = None
        self.score_stft = None
        self.score_all_d = None
        self.score_all_c = None
        self.score_random = None
        self.score_custom = []

        # The number of players there are.
        loops = 8
        if self.custom is not None:
            loops += len(self.custom)

        # Loop through every fixed strategy, skipping it if it should not be tested in this comparison.
        for p1_index in range(0, loops):
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
            elif p1_index == 5:
                if not self.avg_d:
                    continue
                p1_strategy = 'avg_d'
            elif p1_index == 6:
                if not self.avg_c:
                    continue
                p1_strategy = 'avg_c'
            elif p1_index == 7:
                if not self.rand:
                    continue
                p1_strategy = 'random_choice'
            else:
                if len(self.custom[p1_index - 8]) != 4 ** self.mem:
                    continue
                p1_strategy = 'cust'
                p1_lut = self.custom[p1_index - 8]

            # Loop through all opponent types once again skipping it if it should not be tested in this comparison.
            score = 0
            dividend = 0
            for p2_index in range(0, loops):
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
                elif p2_index == 5:
                    if not self.avg_d:
                        continue
                    p2_strategy = 'avg_d'
                elif p2_index == 6:
                    if not self.avg_c:
                        continue
                    p2_strategy = 'avg_c'
                elif p2_index == 7:
                    if not self.rand:
                        continue
                    p2_strategy = 'random_choice'
                else:
                    if len(self.custom[p2_index - 8]) != 4 ** self.mem:
                        continue
                    p2_strategy = 'cust'
                    p2_lut = self.custom[p2_index - 8]

                # Since we have competed against yet another opponent, increment the dividend for getting the average.
                dividend += 1

                # Setup new players every time so they are not impacted by previous histories.
                if p1_strategy == 'cust':
                    p1 = Player(strat='inherited', mem=self.mem, lut=p1_lut)
                else:
                    p1 = Player(strat=p1_strategy, mem=self.mem)
                if p2_strategy == 'cust':
                    p2 = Player(strat='inherited', mem=self.mem, lut=p2_lut)
                else:
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
            elif p1_index == 5:
                self.score_avg_d = score
            elif p1_index == 6:
                self.score_avg_c = score
            elif p1_index == 7:
                self.score_random = score
            else:
                self.score_custom.append(score)
