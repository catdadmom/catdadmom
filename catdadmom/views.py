from flask import render_template
from catdadmom import app


@app.route('/')
def index():
    return render_template("index.html")