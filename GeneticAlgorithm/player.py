import random


# TODO: Allow for modifiable memory depth, currently set to 3
# TODO: To do this, the lookup tables will have to be generated on construction (or pregenerate and place in a file)
# TODO: Allow self.hist to be set to a specific length, this will determine how many
# TODO: characters there are in the lookup table. mem depth = 3 = 4*4*4 = 64 chars, mem depth = 4 = 4*4*4*4 = 256 chars

# 4 values to represent Reward, Sucker, Temptation, and Penalty game outcomes
v = {"CC": 0, "CD": 1, "DC": 2, "DD": 3, 0: "CC", 1: "CD", 2: "DC", 3: "DD"}


# noinspection PyMethodMayBeStatic
class Player:
    # Variables:

    # strategy: Reference to function from strategy.py to denote which strategy this player will use
    # strat_name: Holds strategy name as string
    # flag, flag_2: Flags used by the different strategies

    # lut: Look up table to hold encoding string
    lut = ""

    # strategy_reference: Choose random function from list if one is not supplied in params
    strategy_reference = ["tft",
                          "tf2t",
                          "stft",
                          "random_choice",
                          "all_d",
                          "all_c"]

    # fitness: Holds current fitness level
    fitness = 0

    def __init__(self, strat=""):
        self.strat_name = strat

        self.hist = [] * 3

        # Switch statement to set flags, strategy function, and lookup table based on strat
        match strat:
            case "tft":
                self.strategy = self.__tft
                self.lut = "CDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCD"
                self.flag = False
            case "tf2t":
                self.strategy = self.__tf2t
                self.lut = "CCCCCDCDCCCCCDCDCCCCCDCDCCCCCDCDCCCCCDCDCCCCCDCDCCCCCDCDCCCCCDCD"
                self.flag = False
                self.flag_2 = False
            case "stft":
                self.lut = "CDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCDCD"
                self.strategy = self.__stft
                self.flag = False
            case "random_choice":
                for x in range(0, 64):
                    self.lut += "C" if random.randint(0, 1) == 0 else "D"
                self.strategy = self.__random_choice
            case "all_d":
                self.lut = "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
                self.strategy = self.__all_d
            case "all_c":
                self.lut = "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"
                self.strategy = self.__all_c
            case _:
                raise ValueError("Invalid Strategy type. Valid choices: tft, tf2t, stft, random_choice, "
                                 "all_d, all_c")

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
        return self.lut[random.randint(0, 63)]

    # Function to prepare for next round by resetting flags and clearing fitness
    def prepare(self):
        self.flag = False
        self.flag_2 = False
        self.fitness = 0

    # Update the history when a turn is played
    # Make sure the list is not full before adding a new one
    def update_history(self, str_=""):

        if len(self.hist) < 3:
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

    # Get encoding string
    def get_encoding_string(self):
        p = self
        s = ''
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    p.update_history(v[x])
                    p.update_history(v[y])
                    p.update_history(v[z])
                    s += p.strategy()
        return s
