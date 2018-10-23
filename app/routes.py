from flask import render_template
from app import app
from flask import request, jsonify, json
from glob import glob
import random

app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

@app.route('/')
def index():
    return render_template('index.html')
