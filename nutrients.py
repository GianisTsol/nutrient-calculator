import itertools
import time


class Calculator:
    def __init__(self):
        self.foods = []

    def load_foods(self, f):
        self.foods = []
        for i in f:
            for j in i["nuts"]:
                j = j * i["mult"]
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
            if float(i[1]) >= 1:
                score += abs(float(i[1]) - i[0])
        return score

    def find_best(self, wants):
        foods = [i for i in self.foods for j in range(i["limit"])]
        result, best = [], -10000

        for i in range(3, 9):
            for subset in itertools.combinations(foods, i):
                f = 0 - self.check_combo(subset, wants)
                if f > best:
                    result, best = subset, f
                    print(f)
                    if best > -1.5:
                        return list(result)
        return list(result)

    def calculate(self, want_nuts):
        start = time.time()

        result = self.find_best(want_nuts)
        result.sort(key=lambda x: x["name"])

        return {
            "foods": result,
            "nutrients": self.get_nuts(result),
            "time": round(time.time() - start, 2),
        }
