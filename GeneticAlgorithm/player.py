import random


# 4 values to represent Reward, Sucker, Temptation, and Penalty game outcomes
v = {"CC": 2, "DC": 0, "CD": 3, "DD": 1, 2: "CC", 0: "DC", 3: "CD", 1: "DD"}


# noinspection PyMethodMayBeStatic
class Player:
    # Variables:

    # strategy: Reference to function from strategy.py to denote which strategy this player will use
    # strat_name: Holds strategy name as string
    # flag, flag_2: Flags used by the different strategies
    # lut: Look up table to hold encoding string
    # strategy_reference: Choose random function from list if one is not supplied in params
    strategy_reference = ["tft",
                          "tf2t",
                          "stft",
                          "random_choice",
                          "all_d",
                          "all_c"]

    def __init__(self, strat="", mem=3, lut=""):

        # fitness: Holds current fitness level
        self.fitness = 0

        self.lut = lut

        self.mem = mem

        # Switch statement to set strategy function, and lookup table based on strat
        match strat:
            case "tft":
                #self.lut = "CDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCD"
                for x in range(0, (4 ** self.mem)):
                    self.lut += "C" if x % 2 == 0 else "D"
                self.strategy = self.__tft

            case "tf2t":
                #self.lut = "CCCCCDCDCCCCCDCDCCCCCDCDCCCCCDCDCCCCCDCDCCCCCDCDCCCCCDCDCCCCCDCD"
                while len(self.lut) < (4 ** self.mem):
                    self.lut += "CCCCCDCD"
                self.lut = self.lut[0:4 ** self.mem]
                self.strategy = self.__tf2t

            case "stft":
                #self.lut = "CDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCD"
                for x in range(0, (4 ** self.mem)):
                    self.lut += "C" if x % 2 == 0 else "D"
                self.strategy = self.__stft

            case "all_d":
                self.lut = "D" * (4 ** self.mem)
                self.strategy = self.__all_d

            case "all_c":
                self.lut = "C" * (4 ** self.mem)
                self.strategy = self.__all_c

            case "random_choice":
                self.lut = ''
                for x in range(0, (4 ** self.mem)):
                    self.lut += "C" if random.randint(0, 1) == 0 else "D"
                self.strategy = self.__random_choice

            case "inherited":
                # Checking validity of lut value
                if lut == "" or len(lut) != (4 ** self.mem):
                    raise ValueError(
                        "Invalid Encoding String. Must be proper length and only consist of Cs and Ds: " + str(self.mem))
                else:
                    self.lut = lut

                self.strategy = self.__custom

            case _:
                raise ValueError("Invalid Strategy type. Valid choices: tft, tf2t, stft, random_choice, "
                                 "all_d, all_c")

        self.strat_name = strat
        self.hist = [] * self.mem

    def __str__(self):
        return "Player: {x:<8}, {y:<16}, {z:<72}".format(x=self.fitness, y=self.strat_name, z=self.lut)

    # Tit for Tat: On first turn cooperate, every turn after always play the opponent's last move
    def __tft(self):
        s = ''

        if len(self.hist) == 0:
            return 'C'

        for x in self.hist:
            s += str(x)

        return self.lut[int(s, 4)]

    # Tit for 2 Tat: On first 2 turns cooperate, then if the opponent's two previous moves are defect, then play defect
    def __tf2t(self):
        s = ''

        if len(self.hist) < 2:
            return 'C'

        for x in self.hist:
            s += str(x)

        return self.lut[int(s, 4)]

    # Suspicious Tit for Tat: Defect on first turn, then every turn after that play opponent's last move
    def __stft(self):
        s = ''

        if len(self.hist) == 0:
            return 'D'

        for x in self.hist:
            s += str(x)

        return self.lut[int(s, 4)]

    # Only defect
    def __all_d(self):
        s = ''

        if len(self.hist) == 0:
            return self.lut[0]

        for x in self.hist:
            s += str(x)

        return self.lut[int(s, 4)]

    # Only cooperate
    def __all_c(self):
        s = ''

        if len(self.hist) == 0:
            return self.lut[0]

        for x in self.hist:
            s += str(x)

        return self.lut[int(s, 4)]

    # Choose randomly from lut
    def __random_choice(self):
        return self.lut[random.randint(0, (4 ** self.mem) - 1)]

    # Custom
    def __custom(self):
        s = ''

        if len(self.hist) == 0:
            return self.lut[0]

        for x in self.hist:
            s += str(x)

        return self.lut[int(s, 4)]

    # Update the history when a turn is played
    # Make sure the list is not full before adding a new one
    def update_history(self, str_=""):

        if len(self.hist) < self.mem:
            self.hist.append(v[str_])
        else:
            self.hist.pop(0)
            self.hist.append(v[str_])

    # Checks every combination of memory depth 3
    def test_against_random(self):
        p = self
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    s = p.strategy()
                    s += "C" if random.randint(0, 1) == 0 else "D"
                    print("Res: ", s)
                    p.update_history(s)
