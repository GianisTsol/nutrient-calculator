import itertools
from difflib import SequenceMatcher
import json
from json import JSONEncoder


class Calculator:
    def __init__(self):
        self.foods = []

    def load_foods(self, f):
        self.foods = []
        for i in f:
            self.foods.append(i)

    def get_nuts(self, combo):
        buf = []
        for i in combo:
            for j in range(len(i["nuts"])):
                if len(buf) <= j:
                    buf.append(0)
                buf[j] += int(i["nuts"][j])

        return buf

    def check_combo(self, combo, nuts):
        score = 0
        if len(combo) == 0:
            score = -100000000

        for i in list(zip(self.get_nuts(combo), nuts)):
            score -= abs(int(i[1]) - i[0])
        return score

    def calculate(self, want_nuts):
        foods = self.foods
        new = []
        for i in foods:
            for j in range(0, i["limit"]):
                new.append(i)

        foods = new

        new = []
        for L in range(0, len(foods) + 1):
            for subset in itertools.combinations(foods, L):
                new.append(list(subset))

        best = -10000
        result = []
        for i in new:
            if (f := self.check_combo(i, want_nuts)) > best:
                result = i
                best = f

        result.sort(key=lambda x: x["name"])

        return {"foods": result, "nutrients": self.get_nuts(result)}
