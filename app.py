from flask import Flask, render_template, jsonify
import subprocess

app = Flask(__name__)

SERVICE = "test.service"  # Change this to your systemd service name

def systemctl_cmd(action):
    try:
        result = subprocess.run(
            ["sudo", "systemctl", action, SERVICE],
            check=True, text=True, capture_output=True
        )
        return {"success": True, "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr}

@app.route("/")
def index():
    return render_template('index.html')  # Serve the frontend HTML

@app.route("/api/<action>", methods=["POST"])
def control_service(action):
    if action not in ["start", "stop", "restart", "status"]:
        return jsonify({"error": "Invalid action"}), 400
    return jsonify(systemctl_cmd(action))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
