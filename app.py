import json
from flask import Flask, render_template, request, redirect, url_for
from nutrients import Calculator

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/images"

nutrients_data = {
    "Protein": ["g", 1],
    "Fat": ["g", 1],
    "netcarbs": ["g", 1],
    "sugar": ["g", 1],
    "fiber": ["g", 1],
    "saturated fat": ["g", 1],
    "calcium": ["mg", 0.1],
    "iron": ["mg", 1],
    "potassium K": ["mg", 1],
    "magnesium": ["mg", 1],
    "Phosphorous": ["mg", 1],
    "sodium": ["g", 1],
    "zinc": ["mg", 1],
    "copper": ["mg", 1],
    "manganese": ["mg", 1],
    "selenium": ["mcg", 1],
    "Fluorid": ["mg", 1],
    "Iodine": ["mcg", 1],
    "Chromium": ["mcg", 1],
    "A RAE": ["mg", 1],
    "C": ["mg", 1],
    "ThiaminB1": ["mg", 1],
    "riboflavinB2": ["mg", 1],
    "niacinB3": ["mg", 1],
    "B5": ["mg", 1],
    "B6": ["mg", 1],
    "biotin": ["mcg", 1],
    "folateB9": ["mcg", 1],
    "Folic acid": ["mg", 1],
    "food folate": ["mg", 1],
    "folate DFE": ["mg", 1],
    "Choline": ["mg", 1],
    "B12": ["mcg", 1],
    "Retinol": ["mg", 1],
    "carotene beta": ["mg", 1],
    "carotene alpha": ["mg", 1],
    "cryptoxanthin beta": ["mg", 1],
    "A IU": ["mg", 1],
    "Lucopene": ["mg", 1],
    "Lut+Zeaxanthin": ["mg", 1],
    "E": ["mg", 1],
    "D": ["mcg", 1],
    "D IU": ["mg", 1],
    "D2": ["mg", 1],
    "D3": ["mg", 1],
    "K": ["mcg", 1],
    "Menaquinone": ["mg", 1],
    "omega3": ["mg", 1],
    "omega6": ["mg", 1],
}


sizes = [0]
nutrients = []
priorities = []

for i in nutrients_data.items():
    nutrients.append(i[0])
    sizes.append(i[1][0])
    priorities.append(i[1][1])

responses = []
foods = []


def response_to_list(r):
    buf = []
    new = {}
    for i in r.keys():
        try:
            new[int(i)] = r[i]
        except ValueError:
            pass
    for i in new.keys():
        while i >= len(buf):
            buf.append(0)
        buf[i] = int(new[i])
    return buf


with open("foods.json", "r") as f:
    foods = json.load(f)


@app.route("/")
@app.route("/index")
def index():
    return render_template(
        "index.html", tags=nutrients, sizes=sizes, foods=foods
    )


@app.route("/data", methods=["POST", "GET"])
def data():
    global responses
    form_data = json.loads(request.form["values"])
    prios = json.loads(request.form["prios"])
    prios = response_to_list(prios)
    to_except = json.loads(request.form["except"])
    if len(responses) > 60:
        responses = []
    key = len(responses)
    nuts = response_to_list(form_data)
    if len(nuts) < 1:
        return "INVALID"

    calc = Calculator()
    calc.load_foods(foods, prios)
    res = calc.calculate(nuts, except_foods=to_except)
    if len(res["foods"]) == 0:
        return str(-1)
    responses.append(res)
    query = [(i[0], i[1] - 1) for i in zip(nutrients, nuts) if i[1] != 0]
    responses[key]["query"] = query

    return str(key)


@app.route("/result", methods=["GET"])
def result():
    global responses
    data = request.args
    if int(data["id"]) == -1:
        return render_template("noresult.html")
    try:
        resp = responses[int(data["id"])]
    except (ValueError, IndexError):
        return redirect(url_for("index"))
    foods = resp["foods"]
    for i in foods:
        i["qtty"] = foods.count(i)
    foods = [i for n, i in enumerate(foods) if i not in foods[n + 1 :]]
    return render_template(
        "result.html",
        nuts=list(zip(nutrients, resp["nutrients"])),
        sizes=nutrients_data,
        foods=foods,
        query=resp["query"],
        time=resp["time"],
        likeness=resp["likeness"],
    )


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=False, use_reloader=True, host="0.0.0.0", port=5000)
