import itertools
import time
import numpy as np
from numpy import absolute as npabs
import random


class Calculator:
    def __init__(self):
        self.foods = []
        self.nutrient_size = 0
        self.priorities = np.array([])
        self.factors = []

    def load_foods(self, f, p):
        self.foods = []
        self.priorities = np.int64(p)
        for i in f:
            i["nuts"] = np.float32(i["nuts"]).dot(i["mult"])
            self.foods.append(i)
        self.nutrient_size = len(self.foods[0]["nuts"])

    def get_nuts(self, combo):
        return sum([i["nuts"] for i in combo])

    def check_combo(self, combo, nuts):
        """Returns difference of combo from user resquested values."""
        return sum(npabs(combo - nuts))

    def find_best(self, wants):
        foods = [
            i
            for i in self.foods
            for j in range(i["limit"])
            if self.foods.index(i) not in self.exc
        ]
        indexes = np.where(wants > 1)
        wants = wants[indexes]

        factors = wants.copy() / self.priorities[indexes]

        print(factors.shape)
        print(wants.shape)

        wants /= wants / self.priorities[indexes]

        nullfood = {
            "nuts": np.float32([0 for i in range(len(foods[0]["nuts"]))])
        }
        result = [nullfood]

        best_food = None
        best_score = np.inf
        combo_score = self.check_combo(
            self.get_nuts(result)[indexes] / factors, wants
        )

        while 1:
            for i in foods:
                new_combo = result + [i]
                new_combo_score = self.check_combo(
                    self.get_nuts(new_combo)[indexes] / factors,
                    wants,
                )
                if new_combo_score < combo_score:
                    if best_score > new_combo_score:
                        best_score = new_combo_score
                        best_food = i
            if best_food is not None:
                result.append(best_food)
                combo_score = self.check_combo(
                    self.get_nuts(result)[indexes] / factors,
                    wants,
                )
                del foods[foods.index(best_food)]
                best_food = None
                best_score = np.inf
            else:
                break
        del result[0]  # remove nullfood
        return combo_score, result

    def calculate(self, wants, except_foods=[]):
        self.exc = except_foods
        start = time.time()

        wants = np.int64(wants).astype(np.float32)

        score, result = self.find_best(wants)

        result.sort(key=lambda x: x["name"])

        return {
            "foods": result,
            "nutrients": self.get_nuts(result),
            "time": round(time.time() - start, 4),
            "likeness": score,
        }
