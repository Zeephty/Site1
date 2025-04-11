from flask import Flask, render_template

app = Flask(__name__)


@app.route("/index/<title>")
@app.route("/<title>")
def repa(title):
    header = "Привет, Марс!"
    text_logo = "Mars One"
    slogan = "И на Марсе будут яблони цвести!"
    return render_template("index.html", header=header, text_logo=text_logo, slogan=slogan, title=title)


@app.route("/")
def main():
    header = "Привет, Марс!"
    text_logo = "Mars One"
    slogan = "И на Марсе будут яблони цвести!"
    return render_template("index.html", header=header, text_logo=text_logo, slogan=slogan, title="Главная")


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=8000)