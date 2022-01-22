# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 13:02:49 2022

@author: PC
"""

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'que onda banda'
