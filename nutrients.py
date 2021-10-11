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
        return sum([i["nuts"] for i in combo])

    def check_combo(self, combo, nuts):
        """Returns difference of combo from user resquested values."""
        return sum(combo - nuts)

    def find_best(self, wants):
        foods = [
            i
            for i in self.foods
            for j in range(i["limit"])
            if self.foods.index(i) not in self.exc
        ]

        result, best = [], np.float32(-10.0)
        indexes = np.where(wants >= 1.0)
        wants = wants[indexes]

        for i in range(3, 10):
            for subset in itertools.combinations(foods, i):
                f = self.check_combo(self.get_nuts(subset)[indexes], wants)
                if f > best:
                    result, best = subset, f
                    if best > -2:
                        break
        return list(result)

    def calculate(self, wants, except_foods=[], force_foods=[]):
        self.exc = except_foods
        self.incl = force_foods
        start = time.time()

        wants = np.float32(wants)

        result = self.find_best(wants)
        result.sort(key=lambda x: x["name"])

        return {
            "foods": result,
            "nutrients": self.get_nuts(result),
            "time": round(time.time() - start, 4),
        }
