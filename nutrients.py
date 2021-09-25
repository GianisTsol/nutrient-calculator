import itertools
from functools import lru_cache
from dataclasses import dataclass


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
                buf[j] += float(i["nuts"][j])

        return buf

    def check_combo(self, combo, nuts):
        score = 0

        for i in zip(self.get_nuts(combo), nuts):
            if int(i[1]) >= 1:
                score += abs(float(i[1]) - i[0])
        return score

    def calculate(self, want_nuts):
        foods = self.foods

        new = []
        for i in foods:
            for j in range(i["limit"]):
                new.append(i)
        foods = new

        best = -10000
        result = []

        for i in range(3, 9):
            for subset in itertools.combinations(foods, i):
                f = 0 - self.check_combo(subset, want_nuts)
                if f > best:
                    result = subset
                    best = f
                    if best == 0.0:
                        break

        result = list(result)
        result.sort(key=lambda x: x["name"])
        print(result)

        return {"foods": result, "nutrients": self.get_nuts(result)}
