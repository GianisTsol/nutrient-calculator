import json
from flask import Flask, render_template, request, redirect, url_for
from nutrients import Calculator
from decouple import config
import os


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/images"

nutrients = [
    "Protein",
    "Fat",
    "netcarbs",
    "sugar",
    "fiber",
    "saturated fat",
    "calcium",
    "iron",
    "potassium K",
    "magnesium",
    "Phosphorous",
    "sodium",
    "zinc",
    "copper",
    "manganese",
    "selenium",
    "Fluorid",
    "Iodine",
    "Chromium",
    "A RAE",
    "C",
    "ThiaminB1",
    "riboflavinB2",
    "niacinB3",
    "B5",
    "B6",
    "biotin",
    "folateB9",
    "Folic acid",
    "food folate",
    "folate DFE",
    "Choline",
    "B12",
    "Retinol",
    "carotene beta",
    "carotene alpha",
    "cryptoxanthin beta",
    "A IU",
    "Lucopene",
    "Lut+Zeaxanthin",
    "E",
    "D",
    "DIU",
    "D2",
    "D3",
    "K",
    "Menaquinone",
    "omega3",
    "omega6",
]

sizes = [
    "g",
    "g",
    "g",
    "g",
    "g",
    "g",
    "g",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
    "mg",
]

nutrients = [i.capitalize() for i in nutrients]

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
        buf[i] = new[i]
    return buf


with open("foods.json", "r") as f:
    foods = json.load(f)
    calc.load_foods(foods)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", tags=nutrients, sizes=sizes)


@app.route("/data", methods=["POST", "GET"])
def data():
    global responses
    form_data = request.form
    if len(responses) > 60:
        responses = []
    key = len(responses)
    nuts = response_to_list(form_data)
    if len(nuts) < 1:
        return "INVALID"
    responses.append(calc.calculate(nuts))
    responses[key]["query"] = [i for i in zip(nutrients, nuts) if i[1] != 0]
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
    app.run(debug=True, host="0.0.0.0", port=5000)
