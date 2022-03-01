import random
import time

from player import Player


class TabuSearcher:

    """
    n_turns: The number of turns the tabu searcher will play each of TFT, TF2T, STFT, ALL D, and ALL C each match.
    mem: The memory depth that the tabu searcher and all its opponents will have.
    n_steps: The number of steps the tabu searcher can take.
    n_tabu_size: How many lookup tables can be in the tabu list with a size of zero meaning unlimited.
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
            debug=False):

        # Ensure values are valid.
        if n_turns < 1:
            n_turns = 1
        if mem < 1:
            mem = 1
        if n_steps < 1:
            n_steps = 1
        if n_tabu_size < 0:
            n_tabu_size = 0

        # Set parameters.
        self.n_turns = n_turns
        self.mem = mem
        self.n_steps = n_steps
        self.n_tabu_size = n_tabu_size
        self.top_player = None
        self.elapsed_time = 0
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
    Get the result of the tabu search.
    """
    def __str__(self):

        # Give a message if the tabu search has not yet been performed.
        if self.top_player is None:
            return 'Tabu search has not yet been performed.'
        return f'Tabu Search\t| Memory: {self.mem}\t| Time: {self.elapsed_time}\t| Score: {self.top_player.fitness}\t| LUT: {self.top_player.lut}'

    """
    Perform tabu searcher.
    """
    def perform(self):

        # Reset parameters from any previous tabu searches.
        self.top_player = None

        # Start the timer.
        start_time = time.time()

        # The number of players there are.
        loops = 9
        if self.custom is not None:
            loops += len(self.custom)

        # Generate a random starting LUT.
        starting_lut = ''
        for x in range(0, (4 ** self.mem)):
            starting_lut += "C" if random.randint(0, 1) == 0 else "D"
        if self.debug:
            print(f'Starting LUT {starting_lut}')

        # Define the tabu list.
        tabu_list = []

        # Default the best attempt player to none.
        best_player = None

        # Loop for the given attempts.
        for step in range(0, self.n_steps):

            # If this is not our first loop, start from the previous attempt's best lookup table.
            if best_player is not None:
                starting_lut = best_player.lut

            if self.debug:
                print(f'Step {step + 1} of {self.n_steps}\t| Starting LUT: {starting_lut}.')

            # Reset the current best player for the next iteration.
            best_player = None

            # Test every possible variation of the current LUT.
            # For instance, if the LUT was CCCC...
            # We test CCCC..., DCCC..., CDCC..., CCDC..., CCCD... in search of one with a new greater score.
            for i in range(-1, len(starting_lut)):

                # This is where we create the current variation.
                # If the iteration is -1, don't make any changes as it needs to be tested as well.
                # Otherwise, swap the decision in the LUT at the current index.
                member_lut = starting_lut
                if i > -1:
                    if member_lut[i] == 'C':
                        member_lut = member_lut[:i] + 'D' + member_lut[i + 1:]
                    else:
                        member_lut = member_lut[:i] + 'C' + member_lut[i + 1:]

                # If this lookup table is in the tabu list we cannot test it so continue to the next one.
                if member_lut in tabu_list:
                    if self.debug:
                        print(f'Step {step + 1} of {self.n_steps} member {i + 2} of {len(starting_lut) + 1}\t| LUT: {member_lut} in tabu list.')
                    continue

                if self.debug:
                    print(f'Step {step + 1} of {self.n_steps} member {i + 2} of {len(starting_lut) + 1}\t| LUT: {member_lut}')

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
                    # Reset the tabu searcher every time, so it is not impacted by the history of its last match.
                    tabu_player = Player(strat='inherited', lut=member_lut, mem=self.mem)
                    if strategy == 'self':
                        other_player = Player(strat='inherited', lut=member_lut, mem=self.mem)
                    elif strategy == 'cust':
                        other_player = Player(start='inherited', lut=opponent_lut, mem=self.mem)
                    else:
                        other_player = Player(strat=strategy, mem=self.mem)

                    # Play the given number of turns.
                    for turn in range(0, self.n_turns):
                        tabu_player_move = tabu_player.strategy()
                        other_player_move = other_player.strategy()
                        tabu_player_result = tabu_player_move + other_player_move
                        other_player_result = other_player_move + tabu_player_move
                        tabu_player.update_history(tabu_player_result)
                        other_player.update_history(other_player_result)

                        # Add scores based on the results.
                        if tabu_player_result == 'CC':
                            tabu_player.fitness += 3
                        elif tabu_player_result == 'CD':
                            tabu_player.fitness += 0
                        elif tabu_player_result == 'DC':
                            tabu_player.fitness += 5
                        else:
                            tabu_player.fitness += 1

                    # Add up the cumulative score against all different opponents.
                    score += tabu_player.fitness
                    if self.debug:
                        print(f'Step {step + 1} of {self.n_steps} member {i + 2} of {len(starting_lut) + 1}\t| Strategy: {opponent} | Score: {tabu_player.fitness} | Cumulative: {score}')

                # After having played all opponents, get the average score against all of them.
                score /= dividend
                if self.debug:
                    print(f'Step {step + 1} of {self.n_steps} member {i + 2} of {len(starting_lut) + 1}\t| Average Score for {self.n_turns} Turns: {score}')

                # Get the average score per how many turns there were.
                score /= self.n_turns
                if self.debug:
                    print(f'Step {step + 1} of {self.n_steps} member {i + 2} of {len(starting_lut) + 1}\t| Average Score: {score}')

                # If this is the best attempt of this loop through set it as its best player.
                if best_player is None or score > best_player.fitness:
                    best_player = Player(strat='inherited', lut=member_lut, mem=self.mem)
                    best_player.fitness = score
                    if self.debug:
                        print(f'Step {step + 1} of {self.n_steps} member {i + 2} of {len(starting_lut) + 1}\t| Average Score {score} > Best Attempt Score')
                elif self.debug:
                    print(f'Step {step + 1} of {self.n_steps} member {i + 2} of {len(starting_lut) + 1}\t| Average Score {score} <= Best Attempt Score {best_player.fitness}')

            if best_player is None:
                continue

            # If the best player of a loop was the top player overall, set it.
            if self.top_player is None or best_player.fitness > self.top_player.fitness:
                self.top_player = best_player
                if self.debug:
                    print(f'Step {step + 1} of {self.n_steps} member {i + 2} of {len(starting_lut) + 1}\t| Best Overall Score: {score}')
            elif self.debug:
                print(f'Step {step + 1} of {self.n_steps} member {i + 2} of {len(starting_lut) + 1}\t| Average Score {score} <= Best Overall Score {self.top_player.fitness}')

            # Add the best lookup table from the previous loop to the tabu list and not exceeding its max size.
            tabu_list.append(best_player.lut)
            if len(tabu_list) > self.n_tabu_size:
                tabu_list.pop(0)

        # Get the elapsed time.
        end_time = time.time()
        self.elapsed_time = end_time - start_time
