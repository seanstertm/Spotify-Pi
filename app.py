from flask import Flask, render_template
import os
import configparser

# set up Flask app
app = Flask(__name__)

# get the root directory
dir = os.path.dirname(__file__)
# get path to options file
filename = os.path.join(dir, 'options.ini')
# set up config file
config = configparser.ConfigParser()
config.read(filename)

@app.route("/")
def home():
    return render_template('index.html')

app.run(host='0.0.0.0', port=20)