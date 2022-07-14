from flask import Flask, render_template, request
import os
import configparser
import requests

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
    mode = int(config['MAIN']['mode'])
    return render_template('index.html', mode = mode, next_bus = "N/A")

@app.route("/mode", methods=["POST"])
def toggle_mode():
    print(request.form["mode"])
    mode = int(request.form["mode"])

    response = requests.get("http://ctabustracker.com/bustime/api/v2/getpredictions?key=Yr9nbHrDBVbxtdC4j8BTw5R3z&rt=152&stpid=12472&format=json")
    bus_json = response.json()
    next_bus = bus_json['bustime-response']['prd'][0]['prdctdn']

    return render_template('index.html', mode = mode, next_bus = next_bus)

app.run(host='0.0.0.0', port=80)