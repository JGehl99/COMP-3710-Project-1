import random


# 4 values to represent Reward, Sucker, Temptation, and Penalty game outcomes
v = {'CC': 2, 'DC': 0, 'CD': 3, 'DD': 1, 2: 'CC', 0: 'DC', 3: 'CD', 1: 'DD'}


class Player:
    """
    strat: Strategy name as string.
    mem: The memory depth.
    lut: The lookup table to use for inherited behaviours.
    """
    def __init__(self, strat='', mem=3, lut=''):

        self.fitness = 0
        self.mem = mem
        self.lut = ''

        # Switch statement to set strategy function, and lookup table based on the strategy.
        match strat:
            case 'tft':
                for x in range(0, (4 ** self.mem)):
                    self.lut += 'C' if x % 2 == 0 else 'D'
                self.strategy = self.__tft

            case 'tf2t':
                while len(self.lut) < (4 ** self.mem):
                    self.lut += 'CCCCCDCD'
                self.lut = self.lut[0:4 ** self.mem]
                self.strategy = self.__tf2t

            case 'stft':
                for x in range(0, (4 ** self.mem)):
                    self.lut += 'C' if x % 2 == 0 else 'D'
                self.strategy = self.__stft

            case 'all_d':
                self.lut = 'D' * (4 ** self.mem)
                self.strategy = self.__all_d

            case 'all_c':
                self.lut = 'C' * (4 ** self.mem)
                self.strategy = self.__all_c

            case 'random_choice':
                self.lut = ''
                for x in range(0, (4 ** self.mem)):
                    self.lut += 'C' if random.randint(0, 1) else 'D'
                self.strategy = self.__random_choice

            case 'inherited':
                if lut == "" or len(lut) != (4 ** self.mem):
                    raise ValueError(f'Invalid Encoding String. Must only consist of Cs and Ds of have a length of {self.mem}.')
                else:
                    self.lut = lut
                self.strategy = self.__custom

            case 'avg_d':
                # THIS DOES NOT USE A LOOKUP TABLE SO THIS IS NOT REPRESENTATIVE OF THIS.
                for x in range(0, (4 ** self.mem)):
                    self.lut += 'C' if x % 2 == 0 else 'D'
                self.strategy = self.__avg_d

            case 'avg_c':
                # THIS DOES NOT USE A LOOKUP TABLE SO THIS IS NOT REPRESENTATIVE OF THIS.
                for x in range(0, (4 ** self.mem)):
                    self.lut += 'C' if x % 2 == 0 else 'D'
                self.strategy = self.__avg_c

            case _:
                raise ValueError(f'Strategy type {strat} is invalid.')

        self.strat_name = strat
        self.hist = [] * self.mem

    def __str__(self):
        return f'Fitness: {self.fitness}\t| Strategy: {self.strat_name}\t| LUT: {self.lut}'

    """
    Tit for Tat
    On first turn cooperate, every turn after always play the opponent's last move.
    """
    def __tft(self):
        if len(self.hist) == 0:
            return 'C'
        s = ''
        for x in self.hist:
            s += str(x)
        return self.lut[int(s, 4)]

    """
    Tit for 2 Tat
    On first 2 turns cooperate, then if the opponent's two previous moves are defect, then play defect.
    """
    def __tf2t(self):
        if len(self.hist) < 2:
            return 'C'
        s = ''
        for x in self.hist:
            s += str(x)
        return self.lut[int(s, 4)]

    """
    Suspicious Tit for Tat
    Defect on first turn, then every turn after that play opponent's last move.
    """
    def __stft(self):
        if len(self.hist) == 0:
            return 'D'
        s = ''
        for x in self.hist:
            s += str(x)
        return self.lut[int(s, 4)]

    """
    Only defect.
    """
    def __all_d(self):
        return 'D'

    """
    Only cooperate.
    """
    def __all_c(self):
        return 'C'

    """
    Randomly choose to defect or cooperate.
    """
    def __random_choice(self):
        return 'C' if random.randint(0, 1) else 'D'

    """
    Play what the opponent has most commonly played and defecting in a case where the opponent history is 50/50.
    """
    def __avg_d(self):
        count = 0
        for x in self.hist:
            if x == 1 or x == 3:
                count += 1
        return 'D' if count >= len(self.hist) else 'C'

    """
    Play what the opponent has most commonly played and cooperating in a case where the opponent history is 50/50.
    """
    def __avg_c(self):
        count = 0
        for x in self.hist:
            if x == 0 or x == 2:
                count += 1
        return 'C' if count >= len(self.hist) else 'D'

    """
    Use a custom lookup table.
    """
    def __custom(self):
        if len(self.hist) == 0:
            return self.lut[0]
        s = ''
        for x in self.hist:
            s += str(x)
        return self.lut[int(s, 4)]

    """
    Update the history when a turn is played while making sure the list is not full before adding a new one.
    """
    def update_history(self, str_=''):
        if len(self.hist) < self.mem:
            self.hist.append(v[str_])
        else:
            self.hist.pop(0)
            self.hist.append(v[str_])
