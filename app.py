from flask import Flask, render_template, request
import os
import configparser
import dbus

# set up Flask app
app = Flask(__name__)

# get the root directory
dir = os.path.dirname(__file__)

# get path to options file
filename = os.path.join(dir, 'options.ini')

# set up config file
config = configparser.ConfigParser()
config.read(filename)


sysbus = dbus.SystemBus()
systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')

# load website when accessed
@app.route("/")
def home():
    mode = config['MAIN']['mode']

    if mode == 'cta':
        manager.StartUnit('ctabus.service', 'replace')

    return render_template('index.html', mode = mode)

@app.route("/cta", methods=["POST"])
def toggle_mode():
    config.set("MAIN", "mode", "cta")

    manager.StartUnit('ctabus.service', 'replace')

    return render_template('index.html', mode = 'cta')

@app.route("/spotify", methods=["POST"])
def spotify():
    config.set("MAIN", "mode", "spotify")

    manager.StopUnit('ctabus.service', 'replace')

    return render_template('index.html', mode = 'spotify')


app.run(host='0.0.0.0', port=80)