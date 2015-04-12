#!venv/bin/python
from flask import Flask 
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)
from routes import *

if (__name__) == '__main__':
    app.run(debug=True)
