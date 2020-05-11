from flask import Flask, render_template, request, session
import generateImage
import instruments

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/" , methods=['GET', 'POST'])
def test():
    select = request.form.get('comp_select')
    instr = instruments.getInstrument(str(select))
    session['select'] = str(select)
    return render_template("home.html", instruments=instr)

@app.route("/generate")
def generate():
    store = session.get('select')
    print(store)
    image = generateImage.main(store)
    return render_template("about.html", variable = image)


@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=80)