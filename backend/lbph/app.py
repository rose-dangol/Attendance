from flask import Flask
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)  # Allow React to connect

@app.route("/run-attendance", methods=["GET"])
def run_attendance():
    try:
        subprocess.run(["python", "main.py"])
        return {"status": "success", "message": "Attendance process started"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    app.run(port=5000)
