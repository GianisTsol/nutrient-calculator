import json
from flask import Flask, render_template, request
from nutrients import Calculator, food, Encoder
import os

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/images"

nutrients = []
responses = []
foods = []

tokens = [os.environ.get("DIET_KEY")]


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


with open("nutrients.json", "r") as f:
    nutrients = json.load(f)

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
    key = len(responses) + 1
    responses.append(calc.calculate(response_to_list(form_data)))
    print(responses)
    return str(key)


@app.route("/result", methods=["GET"])
def result():
    data = request.args
    return render_template("result.html", responses=responses, key=data["id"])


@app.route("/addfood", methods=["POST", "GET"])
def addfood():
    if request.method == "POST":
        form_data = request.form
        if form_data["auth"] in tokens:
            if "file" in form_data:
                print(form_data["file"])
            n = food(form_data["name"], int(form_data["limit"]))
            foods.append(n)
            n.set_nuts(response_to_list(form_data))
            with open("foods.json", "w") as f:
                json.dump(foods, f, cls=Encoder)
            calc.load_foods(foods)
            return "gamiesai <3"
    else:
        return render_template("addfood.html", tags=nutrients)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
