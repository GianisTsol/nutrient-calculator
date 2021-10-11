import json
from flask import Flask, render_template, request, redirect, url_for
from nutrients import Calculator
from decouple import config
import os

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/images"

nutrients_data = {
    "Protein": "g",
    "Fat": "g",
    "netcarbs": "g",
    "sugar": "g",
    "fiber": "g",
    "saturated fat": "g",
    "calcium": "mg",
    "iron": "mg",
    "potassium K": "mg",
    "magnesium": "mg",
    "Phosphorous": "mg",
    "sodium": "g",
    "zinc": "mg",
    "copper": "mcg",
    "manganese": "mg",
    "selenium": "mcg",
    "Fluorid": "mg",
    "Iodine": "mcg",
    "Chromium": "mcg",
    "A RAE": "mg",
    "C": "mg",
    "ThiaminB1": "mg",
    "riboflavinB2": "mg",
    "niacinB3": "mg",
    "B5": "mg",
    "B6": "mg",
    "biotin": "mcg",
    "folateB9": "mcg",
    "Folic acid": "mg",
    "food folate": "mg",
    "folate DFE": "mg",
    "Choline": "mg",
    "B12": "mcg",
    "Retinol": "mg",
    "carotene beta": "mg",
    "carotene alpha": "mg",
    "cryptoxanthin beta": "mg",
    "A IU": "mg",
    "Lucopene": "mg",
    "Lut+Zeaxanthin": "mg",
    "E": "mg",
    "D": "mcg",
    "D IU": "mg",
    "D2": "mg",
    "D3": "mg",
    "K": "mcg",
    "Menaquinone": "mg",
    "omega3": "mg",
    "omega6": "mg",
}


sizes = [0]
nutrients = []


for i in nutrients_data.items():
    nutrients.append(i[0])
    sizes.append(i[1])

responses = []
foods = []

tokens = [config("DIET_KEY")]


calc = Calculator()


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
    calc.load_foods(foods)


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
    to_except = json.loads(request.form["except"])
    if len(responses) > 60:
        responses = []
    key = len(responses)
    nuts = response_to_list(form_data)
    if len(nuts) < 1:
        return "INVALID"
    responses.append(calc.calculate(nuts, except_foods=to_except))
    responses[key]["query"] = [
        (i[0], i[1] - 1) for i in zip(nutrients, nuts) if i[1] != 0
    ]
    return str(key)


@app.route("/result", methods=["GET"])
def result():
    global responses
    data = request.args
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
        foods=foods,
        query=resp["query"],
        time=resp["time"],
    )


@app.route("/addfood", methods=["POST", "GET"])
def addfood():
    filename = "demo.png"
    if request.method == "POST":
        form_data = request.form
        if form_data["auth"] in tokens:
            if "file" in request.files:
                file = request.files["file"]
                if file.filename != "":
                    file.save(
                        os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                    )
                    filename = file.filename

            n = {"name": form_data["name"], "limit": int(form_data["limit"])}
            n["nuts"] = response_to_list(form_data)
            n["image"] = filename
            foods.append(n)

            with open("foods.json", "w") as f:
                json.dump(foods, f)
            calc.load_foods(foods)

            return "gamiesai <3 alla ok to evala"
        else:
            return "No no fuck you. Unauthorized."
    else:
        return render_template("addfood.html", tags=nutrients)


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=False, use_reloader=True, host="0.0.0.0", port=5000)
