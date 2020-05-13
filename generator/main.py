from flask import Flask, render_template, request, session
import generateImage
import instruments
import shapes
import json

app = Flask(__name__)

@app.route("/")
def home():

    return render_template("home.html")

@app.route("/" , methods=['GET', 'POST'])
def test():
    select = request.form.get('comp_select')

    instr = instruments.getInstrument(str(select) + ".mxl")
    session['select'] = str(select) + ".mxl"

    music = str(select) + ".mp3"

    return render_template("home.html", instruments=instr, music = music)

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.form['javascript_data']

    print(jsdata)

    this_all = shapes.all_shapes(jsdata)
    session['shapes'] = this_all

    return jsdata

@app.route("/generate")
def generate():
    store = session.get('select')
    shapes = session.get('shapes')

    image = generateImage.main(store, shapes)

    return render_template("about.html", variable = image)


@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=82)