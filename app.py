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

def write():
    with open(filename, 'w') as configfile:
        config.write(configfile)

sysbus = dbus.SystemBus()
systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')

@app.route("/")
def home():
    mode = config['MAIN']['mode']
    power = config['MAIN']['power']
    brightness = config['MAIN']['brightness']

    manager.StartUnit('ctabus.service', 'replace')

    return render_template('index.html', mode = mode, power = power, brightness = brightness)

@app.route("/cta", methods=["POST", "GET"])
def toggle_mode():
    config.set("MAIN", "mode", "cta")
    brightness = config['MAIN']['brightness']

    manager.RestartUnit('ctabus.service', 'fail')

    write()

    return render_template('index.html', mode = 'cta', power = 'on', brightness = brightness)

@app.route("/spotify", methods=["POST", "GET"])
def spotify():
    config.set("MAIN", "mode", "spotify")
    brightness = config['MAIN']['brightness']

    manager.RestartUnit('ctabus.service', 'fail')

    write()

    return render_template('index.html', mode = 'spotify', power = 'on', brightness = brightness)

@app.route("/brightness", methods=["POST", "GET"])
def brightness():
    brightness = request.form['brightness']
    config.set("MAIN", "brightness", brightness)

    mode = config['MAIN']['mode']

    manager.RestartUnit('ctabus.service', 'fail')

    write()

    return render_template('index.html', mode = mode, power = 'on', brightness = brightness)

@app.route("/poweroff", methods=['POST', "GET"])
def poweroff():
    config.set("MAIN", "power", "off")

    manager.StopUnit('ctabus.service', 'replace')

    write()

    return render_template('index.html', power = 'off')

@app.route('/poweron', methods=['POST', "GET"])
def poweron():
    config.set("MAIN", "power", "on")
    mode = config['MAIN']['mode']
    brightness = config['MAIN']['brightness']

    manager.StartUnit('ctabus.service', 'replace')

    write()

    return render_template('index.html', power = 'on', mode = mode, brightness = brightness)


app.run(host='0.0.0.0', port=80)