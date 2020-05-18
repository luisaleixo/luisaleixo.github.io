# -*- Coding: UTF-8 -*-
#coding: utf-8
from multiprocessing import Process, freeze_support

from music21 import *

import generateImage
import instruments
import shapes
from flask import Flask, render_template, request, session

app = Flask(__name__)

@app.route("/")
def home():
    shapes.shapes_array = []
    return render_template("home.html")

@app.route("/" , methods=['GET', 'POST'])
def test():
    shapes.shapes_array = []
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

    freeze_support()
    app.run(debug=True)