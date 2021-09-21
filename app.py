import json
from flask import Flask, render_template, request
from nutrients import Calculator
from decouple import config
import os


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/images"

nutrients = [
    "Πρωτεινες",
    "Υδατανθρακες",
    "Λιπαρα",
    "Αλκοολη",
    "Ψευδάργυρος",
    "Μαγγάνιο",
    "Σελήνιο",
    "Ιώδιο",
    "Ασβέστιο",
    "Φώσφορο",
    "Μαγνήσιο",
    "Σίδηρος",
    "Χαλκός",
    "Βιταμίνη Α ,Βιταμίνη D",
    "Βιταμίνη Ε",
    "Βιταμίνη Κ",
    "Βιταμίνη C",
    "Βιταμίνη Β1 - θειαμίνη",
    "Βιταμίνη Β2 - ριβοφλαβίνη",
    "Βιταμίνη Β3 - νιασίνη",
    "Βιταμίνη Β5- παντοθενικό οξύ",
    "Βιταμίνη Β6- πυριδοξίνη",
    "Βιταμίνη Β7- βιοτίνη",
    "Βιταμίνη Β9-Φυλλικό",
    "Βιταμίνη Β12",
    "Νατριο",
    "χρωμιο",
    "καλιο",
    "θερμιδες",
    "φυτικες ινες",
    "ω-3",
    "ω-6",
]
responses = []
foods = []

tokens = [config("DIET_KEY")]


calc = Calculator()


def response_to_list(r):
    r = dict(r)
    buf = []
    new = {}
    for i in r.keys():
        try:
            int(i)
            new[i] = r[i]
        except ValueError:
            pass
    r = new
    for i in r.keys():
        while int(i) > len(buf):
            buf.append(0)
        buf.append(r[i])
    return buf


with open("foods.json", "r") as f:
    foods = json.load(f)
    calc.load_foods(foods)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", tags=nutrients)


@app.route("/data", methods=["POST", "GET"])
def data():
    global responses
    form_data = request.form
    if len(responses) > 60:
        responses = []
    key = len(responses)
    responses.append(calc.calculate(response_to_list(form_data)))
    return str(key)


@app.route("/result", methods=["GET"])
def result():
    global responses
    data = request.args
    resp = responses[int(data["id"])]
    foods = resp["foods"]
    for i in foods:
        i["qtty"] = foods.count(i)
    foods = [i for n, i in enumerate(foods) if i not in foods[n + 1 :]]

    return render_template("result.html", nuts=resp["nutrients"], foods=foods)


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
    app.run(host="0.0.0.0", port="5000")
