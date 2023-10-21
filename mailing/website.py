from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add():
    try:
        mail = request.form["email"]
        with open("list.txt", "a") as f:
            f.write(f"{mail}\n")
        return render_template("Thankyou.html")
    except Exception as e:
        print(e)
        return redirect(url_for("index"))


# @app.route("/send", methods=["POST"])
# def send():
#     # requests.post("https://desn9002.vinkami.com/send", json={"password": "DESN9002", "subject": subject, "content": content})
#     if not request.json:
#         abort(400)
#     if request.json["password"] != "DESN9002":
#         abort(401)
#     if not request.json["subject"] or not request.json["content"]:
#         abort(402)
#     emailing.main(request.json["subject"], request.json["content"])
#     return "OK"


app.run("localhost", 80, debug=True)
