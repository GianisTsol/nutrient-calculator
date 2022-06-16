import json
from flask import Flask, render_template, request, redirect, url_for
from nutrients import Calculator

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/images"

sizes = {}
nutrients = []
responses = []

with open("foods.json", "r") as f:
    foods = json.load(f)


with open("order.txt", "r") as f:
    order = f.read().splitlines(keepends=False)


for i in foods:
    for j in list(i["nuts"].keys()):
        if j not in nutrients:
            nutrients.append(j)
            sizes[j] = i["nuts"][j]["unit"]
    i["image"] = i["name"].replace(" ", "") + ".jpg"
for i in nutrients:
    if i not in order:
        order.append(i)

nutrients = [i for i in order if i in nutrients]


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


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", tags=nutrients, sizes=sizes, foods=foods)


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
    calc.load_foods(foods, prios, order)
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
        i["qtty"] = foods.count(i) * 10  # TODO: serving size related
    foods = [i for n, i in enumerate(foods) if i not in foods[n + 1 :]]
    return render_template(
        "result.html",
        nuts=list(zip(nutrients, resp["nutrients"])),
        sizes=sizes,
        foods=foods,
        query=resp["query"],
        time=resp["time"],
        likeness=resp["likeness"],
    )


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=False, use_reloader=True, host="0.0.0.0", port=5000)
