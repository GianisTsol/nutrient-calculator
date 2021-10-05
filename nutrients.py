import itertools
import time
import numpy as np


class Calculator:
    def __init__(self):
        self.foods = []
        self.nutrient_size = 0

    def load_foods(self, f):
        self.foods = []
        for i in f:
            i["nuts"] = np.float32(i["nuts"]).dot(i["mult"])
            self.foods.append(i)
        self.nutrient_size = len(self.foods[0]["nuts"])

    def get_nuts(self, combo):
        buf = np.zeros(self.nutrient_size, dtype=np.float32)
        for i in combo:
            buf = np.add(i["nuts"], buf)  # Add food nuts to buffer

        return buf

    def check_combo(self, combo, nuts):
        score = 0

        for i in zip(self.get_nuts(combo), nuts):
            if i[1] >= 1:
                score += abs(i[1] - i[0])
        return score

    def find_best(self, wants):
        foods = [i for i in self.foods for j in range(i["limit"])]
        result, best = [], -100

        for i in range(3, 10):
            for subset in itertools.combinations(foods, i):
                f = 0 - self.check_combo(subset, wants)
                if f > best:
                    result, best = subset, f
                    if best > -2:
                        return list(result)
        return list(result)

    def calculate(self, want_nuts):
        start = time.time()

        result = self.find_best(want_nuts)
        result.sort(key=lambda x: x["name"])

        return {
            "foods": result,
            "nutrients": self.get_nuts(result),
            "time": round(time.time() - start, 4),
        }
