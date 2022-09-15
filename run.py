from flask import Flask, jsonify, request
import json

app = Flask(__name__)


@app.route("/")
def home():
    return "Raspberry pi script is running..."


@app.route("/ping")
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)
