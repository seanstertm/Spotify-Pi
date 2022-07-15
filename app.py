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

# load website when accessed
@app.route("/")
def home():
    mode = int(config['MAIN']['mode'])
    return render_template('index.html', mode = mode, bus_text = "N/A")

# handle mode
@app.route("/mode", methods=["POST"])
def toggle_mode():
    print(request.form["mode"])
    mode = int(request.form["mode"])

    response = requests.get("http://ctabustracker.com/bustime/api/v2/getpredictions?key=Yr9nbHrDBVbxtdC4j8BTw5R3z&rt=152&stpid=12472&format=json")
    bus_json = response.json()
    bus_text = "Next busses: "
    if "error" in bus_json['bustime-response']:
        return render_template('index.html', mode = mode, bus_text = "No busses in the next 30 minutes")
    for bus in bus_json['bustime-response']['prd']:
        if bus_text != "Next busses: ":
            bus_text = bus_text + ", "
        bus_text = bus_text + bus['prdctdn'] + " mins"

    return render_template('index.html', mode = mode, bus_text = bus_text)

app.run(host='0.0.0.0', port=80)