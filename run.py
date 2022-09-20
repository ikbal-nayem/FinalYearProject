from flask import Flask, jsonify, request
import json
from RPi_Action import authentication
from capture import cap

app = Flask(__name__)


@app.route("/", methods=['GET'])
def home():
    return "Raspberry pi script is running..."


@app.route("/cap", methods=['GET'])
def home():
    cap()
    return "Capturing"


@app.route("/ping", methods=['GET'])
def ping():
    return jsonify({"success": True, "message": "pong!"})


@app.route("/configure", methods=['POST'])
def configure():
    res = request.get_json()
    if res:
        with open('app-config.json', 'w') as openfile:
            openfile.write(json.dumps(res, indent=4))
        print("\033[0;36mConfigured successfully.\033[0;0m")
        return jsonify({"success": True, "message": "Configuration received"})
    return jsonify({"success": False, "message": "Configuration not found"})


@app.route("/command/<action>", methods=['GET'])
def command(action=None):
    if action:
        if action == "OPEN":
            if not authentication.isAuthorized:
                authentication.authorized()
        elif action == "ALARM":
            authentication.setAlarm()
    return jsonify({"success": False, "message": "Unknown command"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)
