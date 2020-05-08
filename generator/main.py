from flask import Flask, render_template
import generateImage

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/generate")
def generate():
    image = generateImage.main()
    return render_template("about.html", variable = image)


@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)